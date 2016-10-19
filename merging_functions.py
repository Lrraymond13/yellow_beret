import difflib
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
import funcy


def create_str_merge(row):
    non_nulls = row[~pd.isnull(row)]
    if len(non_nulls)>0:
        return ' '.join(non_nulls.values)
    return np.nan


# for the people who match, consolidate the columns
def consolidate_col(series):
    nonnulls = series.dropna().unique()
    if nonnulls.shape[0] == 0:
        return np.nan
    if isinstance(nonnulls[0], str):
        return sorted(nonnulls, key=len, reverse=True)[0]
    return sorted(nonnulls, reverse=True)[0]


def get_closest_matches(x, df_index):
    if pd.isnull(x):
        return np.nan
    matches = difflib.get_close_matches(x, df_index)
    if len(matches) > 0:
        return matches[0]
    return np.nan


def df_get_closest_matches(df1, df2, merge_col, suffixes=None):
    def wrapper_get_closest_matches(x, df_index):
        if pd.isnull(x):
            return np.nan
        matches = difflib.get_close_matches(x, df_index)
        if len(matches) > 0:
            return matches[0]
        return np.nan

    if not suffixes:
        suffixes = ['_1', '_2']

    # uses difflib to get closest matches
    df1_new = df1.set_index(merge_col)
    df2_new = df2.set_index(merge_col)
    df2_new.index = df2_new.index.map(lambda x: wrapper_get_closest_matches(x, df1_new.index))
    return df2_new.join(df1_new, lsuffix=suffixes[1], rsuffix=suffixes[0])


def get_name_str_sim(row):
    str1, str2 = row.values
    if pd.isnull(str1) or pd.isnull(str2):
        return np.nan
    return fuzz.partial_ratio(str1, str2)


def get_dt_sim(row):
    dt1, dt2 = row.values
    if pd.isnull(dt1) or pd.isnull(dt2):
        return np.nan
    return abs(dt1 - dt2)


def check_match(row):
    # address and application year match
    if row['clean_last_name_sim'] < .9:
        return 0
    if not pd.isnull(row['clean_first_name_sim']) and row['clean_first_name_sim'] < .5:
        return 0
    if row['application_year_sim'] == 0 and row['address_sim'] > 60:
        return 1
    # if matching application year and med schools match
    if row['application_year_sim'] == 0 and row['medical_school_sim'] > 80:
        return 1
    # first and middle names match or first
    if row['application_year_sim'] == 0 and row['clean_first_name_sim'] > 80:
        return 1
    return 0


# add in string similarity functions
def add_similarity_features(df, fnc_dict, is_match_fnc, suffixes=None):
    # dictionary keys should be col name, value should be sim function
    if not suffixes:
        suffixes = ['_1', '_2']
    for key, fnc_val in fnc_dict.iteritems():
        sim_colname = '{}_sim'.format(key)
        col1 = '{}{}'.format(key, suffixes[0])
        col2 = '{}{}'.format(key, suffixes[1])
        df[sim_colname] = df[[col1, col2]].apply(fnc_val, axis=1)
    df['is_match'] = 0
    df.loc[:, 'is_match'] = df.apply(is_match_fnc, axis=1)
    return df


def make_str_lsts_to_numbers(str_series):
    lst = str_series.apply(lambda x: map(int, x.split('_')))
    return funcy.flatten(lst)


def filter_one_match_per_group_simple(df, dedupe_col, sim_cols, ascending=False):
    # to merge cols should be a dict the names of the extra cols to merge in
    # values should be col names to rename
    # sim cols should be name of the columns to use as features
    # sim mask should be mask that accounts as actual mask
    # dedupe col is name of col to dedupe on

    def count_matches(id_list_arr):
        # for each id, make sure matched on 1x in data set
        # should be applied with rolling apply so takes in a dataframe and must return single value
        # unpack already matched ids from string
        current_id1 = id_list_arr[-1]
        other_matches = id_list_arr[:-1]
        is_dup = np.any(other_matches[:] == current_id1)
        if is_dup:
            return True
        return False

    # for each uuid, check for duplicates and choose best match based on sim cols
    # order of the sim cols should be with most important first
    dup_flag = '{}_duplicate'.format(dedupe_col)
    df[dup_flag] = 0
    df.loc[:, dup_flag] = df[
        dedupe_col].expanding(center=False, min_periods=0).apply(func=count_matches)

    df_matches = df[df['is_match'] == 1].sort_values([dedupe_col] + sim_cols, ascending=ascending)
    return df_matches.drop_duplicates([dedupe_col], keep='first')


def filter_one_match_per_group(df, dedupe_col, to_merge_col_dict, sim_cols):
    # to merge cols should be a dict the names of the extra cols to merge in
    # values should be col names to rename
    # sim cols should be name of the columns to use as features
    # sim mask should be mask that accounts as actual mask
    # dedupe col is name of col to dedupe on

    def count_matches(id_list_arr):
        # for each id, make sure matched on 1x in data set
        # should be applied with rolling apply so takes in a dataframe and must return single value
        # unpack already matched ids from string
        current_id1 = id_list_arr[-1]
        other_matches = id_list_arr[:-1]
        is_dup = np.any(other_matches[:] == current_id1)
        if is_dup:
            return True
        return False

    # for each uuid, check for duplicates and choose best match based on sim cols
    # order of the sim cols should be with most important first
    dup_flag = '{}_duplicate'.format(dedupe_col)
    df[dup_flag] = 0
    df.loc[:, dup_flag] = df[
        dedupe_col].expanding(center=False, min_periods=0).apply(func=count_matches)

    df_matches = df[df['is_match'] == 1].sort_values([dedupe_col] + sim_cols, ascending=False)
    dups_mask = df_matches.duplicated([dedupe_col], keep='last')
    # THIS IS HARD CODED IN!!!!
    sims_mask = (
        (df_matches['medical_school_sim'] == 100) & (
            df_matches['address_sim'] > 80) & (df_matches[dup_flag] == 1))

    # filter out matches that should be appended as additional matches
    dups = df_matches.loc[((dups_mask) & (sims_mask)), [dedupe_col] + to_merge_col_dict.keys()]
    dups2 = dups.rename(columns=to_merge_col_dict)
    print dups2
    df_unique = df_matches.drop_duplicates(dedupe_col, keep='first')
    # merge in additional cols
    df_unique2 = pd.merge(left=df_unique, right=dups2, on=dedupe_col, how='left')
    return df_unique2


def get_nonmatched(df, matched_ids, id_colname):
    unmatched = df[~df[id_colname].isin(matched_ids)]
    print unmatched.shape
    return unmatched


def consolidate_merge_cols(df, suffixes, not_to_consolidate, consolidate_fnc=consolidate_col):
    dup_cols = [
        c.split(suffixes[0])[0] for c in df.columns if c.endswith(
            suffixes[0])]
    # remove columns we don't want to consolidate
    dup_cols2 = funcy.remove(lambda x: x in not_to_consolidate, dup_cols)
    print dup_cols2
    for c in dup_cols2:
        c1 = '{}{}'.format(c, suffixes[0])
        c2 = '{}{}'.format(c, suffixes[1])

        df.loc[:, c] = df[[c1, c2]].apply(consolidate_fnc, axis=1)

    to_drop_cols = funcy.flatten(['{}{}'.format(x, suff) for suff in suffixes for x in dup_cols2])
    # drop columns
    return df.drop(to_drop_cols, axis=1)


def get_unique_vals(row):
    unique_years = np.sort(row.dropna().unique())
    return pd.Series(unique_years)