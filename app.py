from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import config
import time
from bs4 import BeautifulSoup
from io_my import FileHandler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = None


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


def login():
    """
    Login to the http://www.hoppenstedt-firmendatenbank.de/
    :return:
    """

    global driver

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

    # Firm
    driver.get('http://www.hoppenstedt-firmendatenbank.de/suche/firmen.html')

    # Query
    waitTillLoad('//*[@id="sortable"]/li[5]/input[4]', method='xpath')
    haupt = driver.find_element_by_xpath('//*[@id="sortable"]/li[5]/input[4]')
    time.sleep(1)
    # haupt.send_keys('C , J , M , B , A , D , E , F , G , H , I , K , L')
    haupt.send_keys('A , B , C , D , E , F , G , H , I , J , K , L , M, N')

    waitTillLoad('//*[@id="sortable"]/li[6]/input[4]', method='xpath')
    besch = driver.find_element_by_xpath('//*[@id="sortable"]/li[6]/input[4]')
    time.sleep(1)
    besch.send_keys("'5' .. '250'")

    waitTillLoad('//*[@id="sortable"]/li[7]/input[4]', method='xpath')
    umasatz = driver.find_element_by_xpath('//*[@id="sortable"]/li[7]/input[4]')
    time.sleep(1)
    umasatz.send_keys("'1' .. '50'")

    # Filter Search
    search = driver.find_element_by_id('startSearchBtn_1')
    search.click()

    waitTillLoad('//*[@id="seachForm"]/div[5]/ul/li[3]/a', 'xpath')

    # Go to result page
    result = driver.find_element_by_xpath('//*[@id="seachForm"]/div[5]/ul/li[3]/a')
    result.click()

    soup = BeautifulSoup(driver.page_source, "lxml")

    td_id_list = ['t_1', 't_2', 't_3', 't_5', 't_6', 't_7', 't_8', 't_9', 't_10', 't_11', 't_12', 't_13', 't_14',
                  't_15', 't_16', 't_17', 't_18', 't_19', 't_20']

    link_list = []
    file_handler = FileHandler('company_list')
    count = 1
    while True:
        try:
            waitTillLoad('businessList', method='id')
            table_result = soup.findAll(name='table', attrs={'id': 'businessList'})

            for table in table_result:
                for row in table.findAll(name='a', attrs={'class': 'black'}):
                    link = 'http://www.hoppenstedt-firmendatenbank.de' + row['href']
                    if link not in link_list:
                        link_list.append(link)
                        print(count, ":", link)
                        file_handler.append(link)
                        count += 1

            waitTillLoad('//*[@id="stepSnextBot"]', method='xpath')
            next = driver.find_element_by_xpath('//*[@id="stepSnextBot"]')
            next.click()

            waitTillLoad('businessList', method='id')
            soup = BeautifulSoup(driver.page_source, "lxml")
        except NoSuchElementException:
            break
        except StaleElementReferenceException:
            time.sleep(1)


def execute():
    """
    Main execution flow
    :return:
    """

    # Load web driver
    state = loadDriver()
    if state is False:
        logging.critical(msg='Error in loading web driver')
        return

    login()

execute()





