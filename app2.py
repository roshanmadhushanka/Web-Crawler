from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import config
import time
import os
from threading import Thread
from io_my import CSVWriter
from bs4 import BeautifulSoup
from io_my import FileHandler
import time

driver = None


class myThread(Thread):
    def __init__(self, company_list, num):
        Thread.__init__(self)
        self.num = num
        self.company_list = company_list
        self.driver = None

    def run(self):
        # threadLock.acquire()
        self.login(self.company_list, self.num)
        # threadLock.release()

    def waitTillLoad(self, element, method='id'):
        """
        Wait till loading a particular element
        :param delay: Number of seconds to delay
        :param element:
        :return:
        """

        count = 0
        max_count = 60
        while count < max_count:
            try:
                if method == 'id':
                    self.driver.find_element_by_id(element)
                elif method == 'xpath':
                    self.driver.find_element_by_xpath(element)
                return True
            except NoSuchElementException:
                time.sleep(1)
                count += 1
        return False

    def communicationDetails(self, ul):
        data = {}
        li_list = ul.findAll(name='li', attrs={'class': 'last noDispl'})
        for li in li_list:
            table_list = li.findAll(name='table')
            for table in table_list:
                tr_list = table.findAll(name='tr')
                for tr in tr_list:
                    td_list = tr.findAll(name='td')
                    data[td_list[0].text] = td_list[1].text.replace(",", "?")
        return data


    def addressDetails(self, ul):
        data = {}
        li_list = ul.findAll(name='li', attrs={'class': 'last noDispl'})
        for li in li_list:
            table_list = li.findAll(name='table')
            for table in table_list:
                tr_list = table.findAll(name='tr')
                for tr in tr_list:
                    td_list = tr.findAll(name='td')
                    data[td_list[0].text] = td_list[1].text.replace(",", "?")
        return data

    def registerInformation(self, ul):
        data = {}
        li_list = ul.findAll(name='li', attrs={'class': 'last noDispl'})
        for li in li_list:
            table_list = li.findAll(name='table')
            for table in table_list:
                tr_list = table.findAll(name='tr')
                for tr in tr_list:
                    td_list = tr.findAll(name='td')
                    if td_list[0].text=='Rechtsform (kurz)':
                        data[td_list[0].text] = td_list[1].text.replace(",", "?")
        return data

    def branchDetails(self, ul):
        data = {}
        li_list = ul.findAll(name='li', attrs={'class': 'last noDispl'})
        for li in li_list:
            table_list = li.findAll(name='table')
            for table in table_list:
                tr_list = table.findAll(name='tr')
                for tr in tr_list:
                    td_list = tr.findAll(name='td')
                    if td_list[0].text == 'Hauptbranche WZ 2008':
                        data[td_list[0].text] = td_list[1].text.replace(",", "?")
        return data

    def managementDetails(self, ul):
        li_list = ul.findAll(name='li', attrs={'class': 'last noDispl'})
        top_management_str = ""
        for li in li_list:
            table_list = li.findAll(name='table')
            top_management_found = False
            terminate = False
            for table in table_list:
                tr_list = table.findAll(name='tr')
                for tr in tr_list:
                    td_list = tr.findAll(name='td')
                    for td in td_list:
                        if 'Top-Management' in td.text:
                            top_management_found = True
                            continue

                        if top_management_found and len(td_list) == 4:
                            text = td.text.strip()
                            if text == "":
                                text = "N/A"
                            top_management_str += text
                        else:
                            terminate = True
                            continue
                        top_management_str += '|'
                    top_management_str += '!'

                    if terminate and len(td_list) == 1:
                        break

        top_management_str = top_management_str.replace(",", "?")
        if top_management_str.startswith("!!"):
            top_management_str = top_management_str[2:]

        if top_management_str.endswith("!!"):
            top_management_str = top_management_str[:-2]
        elif top_management_str.endswith("!"):
            top_management_str = top_management_str[:-1]

        data = {'Top-Management': top_management_str}
        return data

    def login(self, company_list, num):
        """
        Login to the http://www.hoppenstedt-firmendatenbank.de/
        :return:
        """

        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True

        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        path = os.getcwd() + '\\driver\\geckodriver' + str(self.num) + '.exe'
        self.driver = webdriver.Firefox(executable_path=config.GECKO_DRIVER_PATH, firefox_profile=profile,
                                   capabilities=firefox_capabilities)

        self.driver.set_window_size(1124, 850)

        # Load URL
        self.driver.get('http://www.hoppenstedt-firmendatenbank.de/')

        # User name
        name = self.driver.find_element_by_id('user')
        time.sleep(1)
        name.send_keys('michael.hohenester')

        # User password
        password = self.driver.find_element_by_id('pass')
        time.sleep(1)
        password.send_keys('Ewu3Rut2')

        # Submit
        submit = self.driver.find_element_by_xpath('//*[@id="login"]/p/button')
        submit.click()

        # Wait till load the page
        self.waitTillLoad('listenNavigation')

        company_file = CSVWriter('company' + str(self.num) + '.csv')
        count = 0
        for company in company_list:
            while True:
                try:
                    self.driver.get(company)
                    break
                except WebDriverException:
                    print("Except")
                    time.sleep(1)

            communication_data = {}
            address_data = {}
            register_data = {}
            branch_data = {}
            management_data = {}

            error_log = FileHandler('error' + str(self.num))

            load = self.waitTillLoad(element='//*[@id="bigLeftBox1"]/div[3]/ul[1]/li[2]/h5', method='xpath')

            if not load:
                error_log.append(company)
                print('\x1b[6;30;42m' + company + '\x1b[0m')
                continue

            soup = BeautifulSoup(self.driver.page_source, "lxml")
            ul_list = soup.findAll(name='ul', attrs={'class': 'tableLists'})
            for ul in ul_list:
                li_list = ul.findAll(name='li', attrs={'class': 'middle'})
                for li in li_list:
                    h5_list = li.findAll(name='h5')
                    for h5 in h5_list:
                        if h5.text == 'Kommunikation':
                            communication_data = self.communicationDetails(ul)
                        elif h5.text == 'Adresse':
                            address_data = self.addressDetails(ul)
                        elif h5.text == 'Registerinformationen':
                            register_data = self.registerInformation(ul)
                        elif h5.text == 'Branche':
                            branch_data = self.branchDetails(ul)
                        elif 'Management' in h5.text:
                            management_data = self.managementDetails(ul)

            data_map = {}
            data_map.update(communication_data)
            data_map.update(address_data)
            data_map.update(register_data)
            data_map.update(branch_data)
            data_map.update(management_data)

            print(count)
            count += 1
            company_file.append(data_map)


def loadCompanyList():
    file_handler = FileHandler('company_list')
    return file_handler.read()


def execute():
    n_threads = 5
    company_list = loadCompanyList()

    size = len(company_list)
    chunk_size = int(size / n_threads)
    chunk_list = []
    for i in range(n_threads):
        chunk_list.append(company_list[i*chunk_size:(i+1)*chunk_size])
    chunk_list.append(company_list[n_threads*chunk_size:])

    try:
        for i in range(len(chunk_list)):
            thread = myThread(chunk_list[i], i+1)
            thread.start()
            time.sleep(60)

    except Exception as e:
        print(e)


execute()