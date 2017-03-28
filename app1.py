from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import config
import time
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


def communicationDetails(ul):
    li_list = ul.findAll(name='li', attrs={'class': 'last noDispl'})
    for li in li_list:
        table_list = li.findAll(name='table')
        for table in table_list:
            tr_list = table.findAll(name='tr')
            for tr in tr_list:
                td_list = tr.findAll(name='td')
                print(td_list[0].text, td_list[1].text)


def addressDetails(ul):
    print("Address")


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

    # Company list
    for company in company_list:
        driver.get(company)
        waitTillLoad(element='//*[@id="useQuckSearch"]/h3', method='xpath')
        soup = BeautifulSoup(driver.page_source, "lxml")

        ul_list = soup.findAll(name='ul', attrs={'class': 'tableLists'})
        for ul in ul_list:
            li_list = ul.findAll(name='li', attrs={'class': 'middle'})
            for li in li_list:
                h5_list = li.findAll(name='h5')
                for h5 in h5_list:
                    if h5.text == 'Kommunikation':
                        communicationDetails(ul)
                    elif h5.text == 'Adresse':
                        addressDetails(ul)

        break
        time.sleep(3)


def loadCompanyList():
    file_handler = FileHandler('company_list')
    return file_handler.read()


def execute():
    global company_list
    loadDriver()
    company_list = loadCompanyList()
    login()

execute()