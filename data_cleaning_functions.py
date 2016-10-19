import difflib
from fuzzywuzzy import fuzz
import funcy
import pandas as pd
import numpy as np
import re
import string


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
    suffixes = ['JR', 'SR', 'I', 'II', 'III', 'IV', 'V', 'VI']
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
    # if AT or AND or THE, remove
    # to_remove = [
    #     ' AND ', ' AT ', 'THE ', ' COLLGE', 'UNIVERISTY', 'UNIVERWSITY', 'MASSACHUSSETTS', 'JOHN ', 'DE PAUW', 'ASBURY',
    #     'DREXEL INSTITUTE OF TECHNOLOGY', 'A B BROWN UNIVERSITY', 'DARTMOUTH MEDICAL SCHOOL', 'RENSSELAER UNIVERSITY',
    #     'RENSSELAER POLYTECHNICAL INSTITUTE', ' STE', 'COLLEGE OF HOLY CROSS', 'HOLLY CROSS', 'JOHNSS ', 'BERKLEY',
    #     'UC ', 'PITTSBURRGH', 'WESLYN', 'WILLAMS', 'GEORGIA TECH', 'NEW YORK UNIVERSITY UNIV',
    #     'UNIVERSITY OF MICHIGAN IS A', 'OHIO', 'STATE UNIVERSITY OF NEW YORK AT BUFFALO']
    # to_replace = [
    #     ' ', ' ', ' ', ' COLLEGE', 'UNIVERSITY', 'UNIVERSITY', 'MASSACHUSETTS', 'JOHNS ', 'DEPAUW', 'ASHBURY',
    #     'DREXEL UNIVERSITY', 'BROWN UNIVERSITY', 'DARTMOUTH', 'RENSSELAER POLYTECHNIC INSTITUTE',
    #     'RENSSELAER POLYTECHNIC INSTITUTE', ' STATE', 'HOLY CROSS', 'HOLY CROSS', 'JOHNS ',
    #     ' BERKELEY', 'UNIVERSITY OF CALIFORNIA ', 'PITTSBURGH', 'WESLEYAN', 'WILLIAMS',
    #     'GEORGIA INSTITUTE OF TECHNOLOGY', 'NEW YORK', 'UNIVERSITY OF MICHIGAN', 'OHIO STATE', 'SUNY BUFFALO']
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


def clean_med_school(raw_str):
    if pd.isnull(raw_str) or raw_str == 'OTHER':
        return np.nan
    # check for Medical college of virginia and SUNY BUFFALO
    if raw_str.startswith('SUNY '):
        return 'SUNY'
    special_cases = [
                    ('DOWNSTATE', 'SUNY DOWNSTATE'), ('UPSTATE', 'SUNY UPSTATE'), ('BUFFALO', 'SUNY BUFFALO'),
                    ('BROOKLYN', 'SUNY BROOKLYN'),
                    ('MOUNT SINAI', 'ICAHN SCHOOL OF MEDICINE'),
                     ('MT SINAI', 'ICAHN SCHOOL OF MEDICINE'),
                     ('UNIVERSITY OF MO', 'MISSOURI'),
                     ('UNIVERSITY OF VA', 'VIRGINIA'),
                     ('UNIVERSITY OF ALA', 'ALABAMA'),
                     ('NORTH CAROLINA', 'NORTH CAROLINA'), ('CHAPEL HILL', 'NORTH CAROLINA'),
                     ('UNIVERSITY OF N C', 'NORTH CAROLINA'),
                     # THe chicago med school not the same as uchicago
                     ('THE CHICAGO MEDICAL SCHOOL',  'ROSALIND FRANKLIN'), ('ROSALIND FRANKLIN',  'ROSALIND FRANKLIN'),
                     # UMiami also known as Leonard Miller School
                     ('MIAMI', 'MIAMI'),
                     ('TEXAS SOUTHWESTERN', 'TEXAS SOUTHWESTERN'),
                     # UMDJ and Rutgers now the same school
                     ('COLLEGE OF MEDICINE AND DENTISTRY OF NEW JERSEY', 'RUTGERS'), ('UMDNJ NEW JERSEY', 'RUTGERS'),
                     ('GEORGE WASHINGTON', 'GEORGE WASHINGTON'),
                     # spellings for UW St Louis
                     ('ST LOUIS', 'WASHINGTON'), ('SAINT LOUIS', 'WASHINGTON'), ('WASHINGTON UNIVERSITY', 'WASHINGTON'),
                     ('UNIVERSITY OF MINNESOTA', 'MINNESOTA'),
                     ('KECK', 'USC KECK'),  ('SOUTHERN CALIFORNIA', 'USC KECK'),
                     ('OF SOUTH CAROLINA', 'SOUTH CAROLINA'),
                     ('N Y U', 'NYU'), ('NEW YORK UNIVERSITY', 'NYU'), ('NEW YORK MEDICAL COLLEGE', 'NYU'),
                     ('COLLEGE OF P S', 'COLUMBIA'), ('COLLEGE OF PHYSICIANS', 'COLUMBIA'),
                     ('WEILL', 'CORNELL'),
                     ('BAYLOR', 'BAYLOR'), ('JEFFERSON', 'JEFFERSON MEDICAL'), ('PRITZKER', 'UNIVERSITY OF CHICAGO'),
                     ('MARQUETTE', 'WISCONSIN'),
                     ('PERELMAN SCHOOL', 'PENNSLYVANIA'),
                     ('UNIVERSITY OF PENNSLYVANIA', 'PENNSLYVANIA'),
                     ('UNIVERSITY OF PENN', 'PENNSLYVANIA'),
                     ('BOWMAN GRAY', 'WAKE FOREST'), ('OREGON HEALTH', 'OREGON'),
                     ('HERSHEY ', 'PENNSLYVANIA STATE'),
                     ('IOWA ', 'IOWA'),  (' IOWA', 'IOWA'),
                     ('UNIVERSITY OF CHICAGO', 'CHICAGO'),
                     ('OF TOLEDO', 'TOLEDO'),
                     ('CWRU', 'CASE WESTERN'), ('WESTERN RESERVE', 'CASE WESTERN'),
                     ('U W SCHOOL OF MEDICINE', 'WASHINGTON'), ('SEATTLE', 'WASHINGTON'),
                     # SUNY Med Schools
                     ('STATE UNIVERSITY OF NEW', 'SUNY'), ('N Y DOWNSTATE', 'SUNY DOWNSTATE'), ('JACOBS SCHOOL', 'SUNY'),
                     ('NEW YORK STATE', 'SUNY'), ('STATE OF NEW YORK', 'SUNY'), ('DOWNSTATE MEDICAL CENTER', 'SUNY DOWNSTATE'),
                     ('UPSTATE MEDICAL', 'SUNY UPSTATE'), ('DOWNSTATE S U N Y', 'SUNY DOWNSTATE'),
                     # University of california cases
                     ('U C DAVIS', 'UC DAVIS'),
                     ('LOS ANGELES', 'UCLA'),  ('SAN FRANCISCO', 'UCSF'), ('SAN DIEGO', 'UCSD'), ('UNIVERSITY OF CAL', 'UC'),
                     ('U C S F MEDICAL', 'UCSF'), ('CALIFORNIA DAVIS', 'UC DAVIS'), ('UCD UNIVERSITY OF CALIFORNIA', 'UC DAVIS'),
                     # arbitrarily assign unassign UCAL
                     ('UNIVERSITY CALIFORNIA', 'UCSF'), ('UNIVERSITY OF CALIFORNIA SCHOOL OF MEDICINE', 'UCSF'),
                     # other/none/missing
                     ('None', np.nan), ('UNKNOWN', np.nan)]
    # check for UNIVERISITY OF BLAH pattern
    for check, to_return in special_cases:
        if check in raw_str:
            return to_return
    # try university of Blah School of medicine
    m = re.search(r'^UNIVERSITY OF (\D+) SCHOOL OF MEDIC', raw_str)
    if m:
        return m.groups()[0]
    m = re.search(r'^UNIVERSITY OF (\D+) COLLEGE OF MEDICINE', raw_str)
    if m:
        return m.groups()[0]
    m = re.search(r'^UNIVERSITY OF (\D+)', raw_str)
    if m:
        return m.groups()[0]
    # Try the Yale University Medical ... pattern
    m = re.search(r'^(\D+)\s+UNIVERSITY', raw_str)
    if m:
        return m.groups()[0]
    # Search for college of medidcine
    m = re.search(r'^([A-Z]+) COLLEGE OF MEDICINE', raw_str)
    if m:
        return m.groups()[0]
    # Search for Medical college of
    m = re.search(r'^MEDICAL COLLEGE OF ([A-Z]+)', raw_str)
    if m:
        return m.groups()[0]
    # BLAH MEDICAL SCHOOL/COLLEGE
    m = re.search(r'^(\D+)\s* MEDICAL', raw_str)
    if m:
        return m.groups()[0]
    # BLAH SCHOOL OF MEDICINE
    m = re.search(r'(\D+)\s*\bSCHOOL\b|(\D+)\s*\bCOLLEGE\b', raw_str)
    if m:
        return m.groups()[0]
    # if string doesn't match existing pattern, try medical school pattern
    else:
        return raw_str


def clean_med_school_old(raw_med_school):
    # cleanup med school string so we can do useful string comparison on it
    # if contains COLUMBIA, return COLUMBIA
    # remove
    if pd.isnull(raw_med_school):
        return raw_med_school


    raw_med_school = raw_med_school.upper()
    if raw_med_school == 'OTHER':
        return np.nan
    if raw_med_school.startswith('UNIVERSITY OF MINNESOTA'):
        return 'UNIVERSITY OF MINNESOTA'
    if raw_med_school.startswith('LOUISIANA STATE'):
        return 'LOUISIANA STATE'
    # after replacing the mispellings and removing and/at, remove everything after college/university
    if 'BOSTON UNIVERSITY' in raw_med_school:
        # then this string is BC or BU, so just return string
        return 'BOSTON UNIVERSITY'

    to_remove = [
        ' AND ', ' AT ', 'THE ', 'STATE UNIVERSITY OF NEW YORK',
        'STATE UNIVERSITY OF NEW YORK AT BUFFALO',
        'STATE UNIVERSITY OF N Y', 'N Y UNIVERSITY', 'WASH ', 'MICH ', 'FO ',
        ' COLLGE', 'UNIVERISTY', 'UNIVERWSITY', 'BERKLEY', 'NEW YORK UNIVERSITY UNIV',
        'STATE UNIVERSITY OF NEW YORK AT BUFFALO', 'UCSF', 'UCD', 'UNIVERSITY OF CALIFORNIA SF', 'NYU',
        'MEDICAL_SCHOOL',
        ' UNIVERSITY SCHOOL OF MEDICINE', ' UNIVERSITY SCHOOL OF MED',
        ' UNIVERSITY OF MEDICINE', ' COLLEGE OF MEDICINE', ' SCHOOL OF MEDICINE', 'MEDICAL COLLEGE OF ',
        ' MEDICAL SCHOOL', ' HEALTH SCIENCES CENTER', ' PRITZKER', ' MEDICAL']

    to_replace = [
        ' ', ' ', ' ', 'SUNY',
        'SUNY BUFFALO', 'SUNY', 'NEW YORK UNIVERSITY',
        'WASHINGTON ', 'MICHIGAN ', 'OF ',
        ' COLLEGE', 'UNIVERSITY', 'UNIVERSITY', 'UNIVERSITY OF CALIFORNIA BERKELEY',
        'NEW YORK UNIVERSITY', 'SUNY BUFFALO', 'UNIVERSITY OF CALIFORNIA SAN FRANCISCO',
        'UNIVERSITY OF CALIFORNIA DAVIS', 'UNIVERSITY OF CALIFORNIA SAN FRANCISCO', 'NEW YORK UNIVERSITY',
        ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    trans_word = correct_mispellings(raw_med_school, to_remove, to_replace)
    if 'COLUMBIA' in trans_word or (
                    'PHYSICIANS' in trans_word and 'SURGEONS' in trans_word) or 'P S ' in trans_word:
        return 'COLUMBIA'
    if 'CORNELL ' in trans_word:
        return 'CORNELL'
    if 'ALBERT EINSTEIN' in trans_word:
        return 'ALBERT EINSTEIN'
    if 'THOMAS JEFFERSON' in trans_word:
        return 'THOMAS JEFFERSON'
    if 'CHICAGO' in trans_word:
        return 'UNIVERSITY OF CHICAGO'
    if 'STANFORD' in trans_word:
        return 'STANFORD'
    # search for various SUNY
    # search for various UC schools
    if trans_word.find('SCHOOL ') == 0:
        return trans_word
    split_wrd = ' UNIVERSITY'
    if 'COLLEGE' in trans_word:
        split_wrd = ' COLLEGE'
    base_word = trans_word.split(split_wrd)[0]
    return standardize_whitespace(base_word)