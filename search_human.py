import funcy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

BIO_URL = 'http://libraries.mit.edu/get/brc'
COMMON_NONMEDICAL_OCCS = ('Philanthropist', 'Writer', 'Artist', 'Actor', 'Actress', 'Politician',
                          'Investment banker', 'Financier', 'Physicist', 'Novelist',
                          'Car dealer', 'Rock singer', 'Baseball player', 'Engineer', 'Executive', 'Educator')

class Driver():
    "web driver to search for people by name"

    def __init__(self, url=BIO_URL):
        self.driver = webdriver.Firefox()
        self.url = url
        print self.url

    def get_person_results(self, text_name):
        # navigate to the search bar
        # text name should entered as last, first (middle)
        search = self.driver.find_element_by_class_name('search')
        search.send_keys(text_name)
        search.click()
        search.submit()
        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_class_name('result_count'))
            res = self.driver.find_element_by_class_name('result_count')
            res2 = res.find_element_by_class_name('total_results')
            return int(res2.text)
        except (NoSuchElementException, TimeoutException) as t:
            print 'No results found for {}'.format(text_name)
            return None

    def filter_results_str(self, str, last_name):
        # str generally comes in like Adler, Solomon Stanley Scientist May 26, 1945
        #may also hae a string with just occupation
        # Philanthropist June 23, 1894, November 14, 1975
        # first, check that string startswith last name
        if not str.startswith(last_name.title()):
            return False
        # try to parse occupation as -4 item
        ls_str = str.split(' ')
        if len(ls_str) < 4:
            # this string probably only contains names
            return True
        occ1 = ls_str[-4]
        has_digit = any(i.isdigit() for i in occ1)
        if has_digit:
            # then this person must have a death date, so try again
            occ1 = ls_str[-7]
        if occ1 in COMMON_NONMEDICAL_OCCS:
            return False
        # lots of other reasons this may miss people, but rather scrape too many than too few
        return True

    def parse_results(self, last_name):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_id('results'))
            res = self.driver.find_element_by_id('results')
            res2 = res.find_element_by_tag_name('tbody')
            list_res = funcy.remove(lambda x: x.startswith('See '), res2.text.split('\n'))
            # check for scientists, surgeons, doctors and other ists
            possible_matches = filter(lambda x: self.filter_results_str(x, last_name), list_res)
            print possible_matches
            return possible_matches
        except (NoSuchElementException, TimeoutException) as t:
            print 'Results page error {}'.format(last_name)
            return None

    def select_link(self, name, last_name):
        try:
            print 'Selecting link for {}'.format(name)
            # first, click on entry of the person
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_partial_link_text(name))
            res = self.driver.find_element_by_partial_link_text(name)
            res.click()
            # then navigate to their biography page
            WebDriverWait(self.driver, 15).until(
                lambda x: x.find_element_by_class_name('Biographies'))
            res = self.driver.find_element_by_partial_link_text(last_name)
            res.click()
            # check to make sure results include biographies
        except (NoSuchElementException, TimeoutException) as e:
            print 'selecting link error {}'.format(name)

    def handle_multiple_results_text(self, res_str):
        # get name portion
        try:
            # if there are no digits in the res_str, then res_strin only contains a name
            has_digit = any(i.isdigit() for i in res_str)
            if has_digit:
                link_text = ' '.join(res_str.split(' ')[:-4])
            else:
                link_text = res_str
            print link_text
            last_name = res_str.split(',')[0]
            print 'generated link selection text {} last name {}'.format(link_text, last_name)
            self.select_link(link_text, last_name)
        except (NoSuchElementException, TimeoutException) as e:
            print 'handle multiple results failure {}'.format(res_str)

    def download_person_results(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_id('BiographiesDetailsPage'))
            t = self.driver.find_element_by_id('regionBiographyDisplay')
            txt = self.driver.find_element_by_class_name('document-text')
            return {'biography': t.text, 'full_text': txt.text}
        except (NoSuchElementException, TimeoutException) as e:
            print 'text scrape error'
            return None

    def download_multi_results(self, res_txt):
        self.handle_multiple_results_text(res_txt)
        r = self.download_person_results()
        # this calls some javascript to go back 2x to main search results
        self.driver.execute_script("window.history.go(-1)")
        self.driver.execute_script("window.history.go(-1)")
        WebDriverWait(self.driver, 5).until(
            lambda x: x.find_element_by_id('advancedSearch'))
        return r

    def search(self, first_name, last_name):
        # return to home
        self.driver.get(self.url)
        name = ', '.join([last_name.title(), first_name.title()])
        num_res = self.get_person_results(name)
        # if no results, return and continue
        print num_res
        if num_res is None:
            txt = []
        if num_res == 1:
            print last_name
            # for 1 entry, we are using last name as a partial link search because don't know entry
            self.select_link(last_name.title(), last_name.title())
            txt = [self.download_person_results()]
        elif num_res > 1:
            # multiple results, note how many results returned and download all bios
            print 'Multiple results'
            possibles = self.parse_results(last_name)
            print possibles
            # handle case where all possibles are unrelated
            if possibles is not None and len(possibles) > 0:
                txt = map(self.download_multi_results, possibles)
                # return shape is num results, name searched and list of text results
                txt = zip(possibles, txt)
            else:
                txt = None
        return (num_res, name, txt)


