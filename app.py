from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import logging
import config
import time

driver = None


def loadDriver():
    """
    Load headless browser driver

    :return: Operation state
    """

    global driver
    try:
        # driver = webdriver.PhantomJS(config.PHANTOM_DRIVER_PATH)
        driver = webdriver.Firefox(executable_path=config.GECKO_DRIVER_PATH)
        return True
    except WebDriverException:
        return False


def login():
    """
    Login to the http://www.hoppenstedt-firmendatenbank.de/
    :return:
    """

    global driver
    # Load URL
    driver.get('http://www.hoppenstedt-firmendatenbank.de/')

    # User name
    name = driver.find_element_by_xpath('//*[@id="user"]')
    name.clear()
    name.send_keys('michael.hohenester')

    # User password
    password = driver.find_element_by_xpath('//*[@id="pass"]')
    password.clear()
    password.send_keys('Ewu3Rut2')

    # Submit
    submit = driver.find_element_by_xpath('//*[@id="login"]/p/button')
    submit.click()

    try:
        logout_element = driver.find_element_by_xpath("captcha_data.solution")
    except NoSuchElementException:
        pass


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





