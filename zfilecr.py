# import sys
# print(sys.path)

from selenium import webdriver
from datetime import datetime
import re


class SeashellFilecr:
    def __init__(self, lastlink):
        self.lastlink = lastlink
        self.done = False

    def process(self):

        # driver = webdriver.PhantomJS(service_args=['--load-images=no'])
        # drv = webdriver.PhantomJS(service_args=['--load-images=no'])

        # from selenium.webdriver.firefox.options import Options
        # options = Options()
        # options.headless=True
        # driver = webdriver.Firefox(options=options)
        # drv = webdriver.Firefox(options)

        options = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option("prefs", prefs)
        options.headless=True
        # options.add_argument("--headless")
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-gpu')
        driver = webdriver.Chrome()
        drv = webdriver.Chrome(options=options)

        driver.implicitly_wait(10)
        drv.implicitly_wait(10)

        f = open('urls-Filecr.txt', 'w', encoding="utf-8")
        i = 1
        while not self.done:
            self.done = True
            start_i = "https://filecr.com/elearning/?page=" + str(i)
            print(start_i)
            driver.get(start_i)

            check_count=0

            while check_count < 12:

                elems = driver.find_elements_by_class_name("product-item")
                check_count= len(elems)

            j = 0
            for elem in elems:
                # print(elem.get_attribute("href"))
                # self.processitem(drv, elem)
                j = j + 1

                aelem = elem.find_element_by_tag_name("a")
                if aelem.get_attribute("href") == self.lastlink:
                    self.done = True
                    break

                #print(elem.text)
                # f.write('*' * 50 + '\n')
                # f.write('Todo ')
                # f.write(elem.text)
                # f.write('\n')
                # f.write(elem.get_attribute("href"))
                # f.write('\n' + '*' * 50 + '\n')
                # self.processitem(drv, elem, f)
                print(aelem.get_attribute("href"))
                f.write(aelem.get_attribute("href"))
                f.write('\n')
                self.done = False
            i += 1
            if i == 43:
                self.done = True

        f.close()
        drv.close()
        driver.close()






z = SeashellFilecr("https://filecr.com/elearning/applemagazine/")
z.process()

