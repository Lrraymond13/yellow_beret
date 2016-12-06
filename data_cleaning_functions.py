import os
from fuzzywuzzy import fuzz
import funcy
import pandas as pd
import numpy as np
import re
import string

from dev import MEDSCHOOL_FILENAME, STD_DIR


def trans_remov_punc(to_change, change_to):
    # removes specified punctuation using string maketrans (very fast, C lookups)
    #returns partially evaluated fnc
    trantab = string.maketrans(to_change, change_to)
    return funcy.func_partial(lambda x: x.translate(trantab))


def standardize_whitespace(pub_str):
    # remove extra whitespace in a string
    return ' '.join(filter(None, pub_str.split(' ')))


def remove_punc(pub_str):
    # function to remove punctuation
    # make sure string isn't unicode
    pub_str = str(pub_str)
    nonelst = ' '*len(string.punctuation)
    fn = trans_remov_punc(string.punctuation, nonelst)
    new_str = fn(pub_str)
    nonelst = ' '*len(string.digits)
    fn = trans_remov_punc(string.digits, nonelst)
    new_str2 = fn(new_str)
    # standardize spaces
    return standardize_whitespace(new_str2)


def clean_names(name):
    # clean names, remove unicode, remove punctuation, uppercase, remove excess spaces
    # if name is missing, return null
    if pd.isnull(name) or name is None or name == '':
        return np.nan
    try:
        # try to get rid of the annoying blank spaces in .dta files
        l_str = name[0]
    except IndexError:
        print name
        return np.nan
    # uppercase
    # need to cast because str may be in unicode
    upp = str(name).upper()
    return remove_punc(upp)


def has_suffix(raw_last_name):
    # a boolean fnc to identify which rows may have a suffix
    if pd.isnull(raw_last_name):
        return False
    last_lst = raw_last_name.split(' ')
    if len(last_lst) == 1:
        # if no white spaces in last name, only 1 word, so no suffix
        return False
    suffixes = ['JR', 'SR', 'I', 'II', 'III', 'IV', 'V', 'VI', 'JR.', 'SR.']
    # want to differentiate between suffix (JR, SR, I, II, III, IV, V)
    # between last names with multiple parts (ex. st john)
    # check if last word in list
    return (last_lst[-1] in suffixes)


def get_suffix(clean_last_name):
    # this assumes the fnc will only be applied to rows id as those with a suffix
    # remove last word from last name
    return clean_last_name.split(' ')[-1]


def remove_suffix_from_last_name(last_name_raw):
    # return only last name if last name has a suffix
    non_suffix = last_name_raw.split(' ')[:-1]
    return ' '.join(non_suffix)


def has_award(raw_name, awards_keywords):
    # if the first name has honor or award it it, return True
    if pd.isnull(raw_name):
        return False
    return any(map(lambda x: x in raw_name, awards_keywords))


def is_year_range(raw_str):
    # check if a year range coded into 1972-73
    if pd.isnull(raw_str):
        return False
    if re.search(r'\d{4}-\d{2,4}', raw_str) is not None:
        return True


def long_form_date(dt_str):
    # change date string to be YYYY-YYYY instead of YYYY-YY
    if pd.isnull(dt_str):
        return dt_str
    m = re.match(r'(\d{4})-(\d{2})', dt_str)
    if m:
        g = m.groups()
        return '{0}-19{1}'.format(g[0], g[1])
    m = re.match(r'(\d{4})', dt_str)
    if m:
        return dt_str
    return np.nan


def str_sim(row, row1_name, row2_name):
    str1 = row[row1_name]
    str2 = row[row2_name]
    if pd.isnull(str1) and pd.isnull(str2):
        return 0
    if isinstance(str1, float) or isinstance(str2, float):
        return 0
    clean_str1 = clean_names(str1)
    clean_str2 = clean_names(str2)
    try:
        # use partial ratio because important to note if one string inside another
        return fuzz.partial_ratio(clean_str1, clean_str2)
    except TypeError:
        print clean_str2, clean_str1, str2, str1


def replace_last_name(last_name, mispellings_dict):
    if last_name in mispellings_dict:
        return mispellings_dict[last_name]
    return last_name


def correct_mispellings(pub_str, to_remove, to_replace):
    # function to remove punctuation
    if pd.isnull(pub_str):
        return np.nan
    # to_remove = ['TERRECE', 'FRED', 'LAURENCE',
    #              'CUONO', 'DEFRENZE', 'JEFFERY', 'FINKLEMAN', 'SHERRAD', 'ANSCHNETZ', 'MARC', 'JENSON', 'KASTI',
    #              'ADELBERT', 'RITCHARD', 'MANSFORD', 'DEFRENZO', 'DROBIN', 'HAMES', 'KREUZ', 'JERROLD', 'MANEUSI',
    #              'UNGARO']
    # to_replace = ['TERRENCE', 'FREDERICK', 'LAWRENCE',
    #               'CUOMO', 'DEFRONZO', 'JEFFREY', 'FINKELMAN', 'SHERRARD', 'ANSCHUETZ', 'MARCUS', 'JENSEN', 'KASTL',
    #               'ALBERT', 'RITCHARD', 'MANIFORD', 'DEFRONZO', 'DROBIS', 'JAMES', 'KRUEZ', 'JERROD', 'MANCUSI',
    #               'UNGARO']

    word_pairs = zip(to_remove, to_replace)
    # list of words to replace
    words_in_str = filter(lambda (x, y): x == pub_str, word_pairs)
    trans_word = pub_str
    for to_remove_wrd, to_replace_wrd in words_in_str:
        trans_word = trans_word.replace(to_remove_wrd, to_replace_wrd)
    # standardize spaces
    return standardize_whitespace(trans_word)


def long_form_date(dt_str):
    # change string dates to be YYYY-YYYY instead of YYYY-YY
    if pd.isnull(dt_str):
        return dt_str
    # first try to match a full four year date
    m = re.match(r'(\d{4})-(\d{4})', dt_str)
    if m:
        g = m.groups()
        return '{0}-{1}'.format(g[0], g[1])
    # otherise, check for a 1998-90 form date
    m = re.match(r'(\d{4})-(\d{2})', dt_str)
    if m:
        g = m.groups()
        return '{0}-19{1}'.format(g[0], g[1])
    m = re.match(r'(\d{4})', dt_str)
    if m:
        g = m.groups()
        return '{0}'.format(g[0])
    # otherwise this is a weird edge case
    print dt_str
    return np.nan


# college name standardization fnc
def clean_std_college_name(college_raw, to_remove, to_replace):
    # need to change 'college to university' unless Boston college or BU remove ANDS, AT, THE expand UCLA to UCAL, UC Davis etc.
    # remove random 1961 at the end of strings, (anything after university unless univ is the first word)
    if pd.isnull(college_raw):
        return np.nan
    trans_word = correct_mispellings(college_raw, to_remove, to_replace)
    # after replacing the mispellings and removing and/at, remove everything after college/university
    if 'BOSTON' in trans_word:
        # then this string is BC or BU, so just return string
        return trans_word
    split_wrd = ' UNIVERSITY'
    if 'COLLEGE' in trans_word:
        split_wrd = ' COLLEGE'
    base_word = trans_word.split(split_wrd)[0]
    return standardize_whitespace(base_word)


def construct_medschool_mapping(filename=MEDSCHOOL_FILENAME):
    name_key = pd.read_excel(os.path.join(STD_DIR, filename))
    return name_key.set_index('RAW_STRING')


def _locate_str(df, raw_str, colname, matching_fnc):
    if pd.isnull(raw_str):
        return np.nan
    try:
        val = df.loc[raw_str, colname]
        if isinstance(str, val):
            return val
        return val[0]
    except (KeyError, TypeError) as e:
        # do string sim match
        mask = df.index.map(matching_fnc)
        if mask.any():
            return df.loc[mask, colname][0]
        return np.nan


def _clean_med_school(raw_str, mapping=None):
    # note mapping should be a pandas df
    # with index as str values to search and medical school columns as std. name
    # for speed, mapping should not be none
    if mapping is None:
        mapping = construct_medschool_mapping()
    # check for Medical college of virginia and SUNY BUFFALO
    if pd.isnull(raw_str):
        return raw_str
    # cast unicode to ascii and skip spaces
    raw_str = clean_names(str(raw_str).strip().upper())
    is_sim = lambda x: str(x) in raw_str
    # check if its already clean
    is_clean = mapping[mapping['MEDICAL_SCHOOL']==raw_str].shape[0]
    if is_clean > 0:
        return raw_str
    val = _locate_str(mapping, raw_str, 'MEDICAL_SCHOOL', is_sim)
    if pd.isnull(val):
        print raw_str
        return raw_str
    return val


def _medschool_foreign(raw_str, mapping=None):
    if pd.isnull(raw_str):
        return 0
    # cast unicode to ascii and skip spaces
    raw_str = clean_names(str(raw_str).strip().upper())
    is_sim = lambda x: x in raw_str
    cleaned = mapping[mapping['MEDICAL_SCHOOL']==raw_str]
    if cleaned.shape[0] > 0:
        return cleaned['IS_FOREIGN'][0]
    val = _locate_str(mapping, raw_str, 'IS_FOREIGN', is_sim)
    if pd.isnull(val):
        return 0
    return int(val)


DEFAULT_MAPPING = construct_medschool_mapping()
clean_med_school = funcy.rpartial(_clean_med_school, DEFAULT_MAPPING)
is_foreign_med_school = funcy.rpartial(_medschool_foreign, DEFAULT_MAPPING)
