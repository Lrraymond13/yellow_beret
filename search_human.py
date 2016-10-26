import funcy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

BIO_URL = 'http://libraries.mit.edu/get/brc'


class Driver():
    "web driver to search for people by name"

    def __init__(self, url=None):
        self.driver = webdriver.Firefox()
        self.url = BIO_URL if url is None else url
        self.driver.get(url)

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

    def parse_results(self, last_name):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_id('results'))
            res = self.driver.find_element_by_id('results')
            res2 = res.find_element_by_tag_name('tbody')
            list_res = funcy.remove(lambda x: x.startswith('See '), res2.text.split('\n'))
            # check for scientists
            possible_matches = filter(lambda x: 'Scientist' in x or 'Doctor' in x or x.endswith('ist'), list_res)
            # make sure all matches start with last name
            propcase_name = last_name.title()
            return funcy.filter(lambda x: x.startswith(propcase_name), possible_matches)
        except (NoSuchElementException, TimeoutException) as t:
            print 'Results page error {}'.format(last_name)
            return None
        
    def select_link(self, name, last_name):
        try:
            print name
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
            link_text = ' '.join(res_str.split(' ')[:-4])
            last_name = res_str.split(',')[0]
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
            txt = map(self.download_multi_results, possibles)
            # return shape is num results, name searched and list of text results
            txt = zip(possibles, txt)
        return (num_res, name, txt)


