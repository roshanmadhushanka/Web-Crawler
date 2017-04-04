from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import config
import time
import pandas as pd
from io_my import CSVWriter
from bs4 import BeautifulSoup
from io_my import FileHandler

driver = None
company_list = None


def loadDriver():
    """
    Load headless browser driver

    :return: Operation state
    """

    global driver

    try:

        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True

        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        driver = webdriver.Firefox(executable_path=config.GECKO_DRIVER_PATH, firefox_profile=profile, capabilities=firefox_capabilities)

        driver.set_window_size(1124, 850)

    except WebDriverException:
        print("Web driver error")
        return False


def waitTillLoad(element, method='id'):
    """
    Wait till loading a particular element
    :param delay: Number of seconds to delay
    :param element:
    :return:
    """
    global driver

    while True:
        try:
            if method == 'id':
                driver.find_element_by_id(element)
            elif method == 'xpath':
                driver.find_element_by_xpath(element)
            break
        except NoSuchElementException:
            time.sleep(1)

# def waitTillLoad(element, method='id'):
#     """
#     Wait till loading a particular element
#     :param delay: Number of seconds to delay
#     :param element:
#     :return:
#     """
#
#     global driver
#     count = 0
#     max_count = 10
#     while count < max_count:
#         try:
#             if method == 'id':
#                 driver.find_element_by_id(element)
#             elif method == 'xpath':
#                 driver.find_element_by_xpath(element)
#             return True
#         except NoSuchElementException:
#             time.sleep(1)
#             count += 1
#     return False


def communicationDetails(ul):
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


def addressDetails(ul):
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


def registerInformation(ul):
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


def branchDetails(ul):
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


def managementDetails(ul):
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


def login():
    """
    Login to the http://www.hoppenstedt-firmendatenbank.de/
    :return:
    """

    global driver, company_list

    # Load URL
    driver.get('http://www.hoppenstedt-firmendatenbank.de/')

    # User name
    name = driver.find_element_by_id('user')
    time.sleep(1)
    name.send_keys('michael.hohenester')

    # User password
    password = driver.find_element_by_id('pass')
    time.sleep(1)
    password.send_keys('Ewu3Rut2')

    # Submit
    submit = driver.find_element_by_xpath('//*[@id="login"]/p/button')
    submit.click()

    # Wait till load the page
    waitTillLoad('listenNavigation')

    count = 0
    company_file = CSVWriter('data.csv')

    for company in company_list[count:]:
        while True:
            try:
                driver.get(company)
                break
            except WebDriverException:
                time.sleep(1)

        communication_data = {}
        address_data = {}
        register_data = {}
        branch_data = {}
        management_data = {}

        # error_log = FileHandler('error')
        #
        # load = waitTillLoad(element='//*[@id="bigLeftBox1"]/div[3]/ul[1]/li[2]/h5', method='xpath')
        #
        # if not load:
        #     error_log.append(company)
        #     print('\x1b[6;30;42m' + company + '\x1b[0m')
        #     continue
        waitTillLoad(element='//*[@id="bigLeftBox1"]/div[3]/ul[1]/li[2]/h5', method='xpath')
        soup = BeautifulSoup(driver.page_source, "lxml")
        ul_list = soup.findAll(name='ul', attrs={'class': 'tableLists'})
        for ul in ul_list:
            li_list = ul.findAll(name='li', attrs={'class': 'middle'})
            for li in li_list:
                h5_list = li.findAll(name='h5')
                for h5 in h5_list:
                    if h5.text == 'Kommunikation':
                        communication_data = communicationDetails(ul)
                    elif h5.text == 'Adresse':
                        address_data = addressDetails(ul)
                    elif h5.text == 'Registerinformationen':
                        register_data = registerInformation(ul)
                    elif h5.text == 'Branche':
                        branch_data = branchDetails(ul)
                    elif 'Management' in h5.text:
                        management_data = managementDetails(ul)

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
    global company_list
    loadDriver()
    company_list = loadCompanyList()
    login()

execute()