import os
import sys
import inspect
from nose.tools import with_setup
from appium import webdriver
from sauceclient import SauceClient

browsers = [{
    'deviceName':        'iPhone 5',
    'appiumVersion':     '1.4.11',
    'platformName':      'iOS',
    'platformVersion':   '8.4',
    'app':               'https://s3.amazonaws.com/appium/TestApp8.4.app.zip',
    'browserName':       '',
    'deviceOrientation': 'portrait'
}, {
    'deviceName':        'iPhone 6',
    'appiumVersion':     '1.4.11',
    'platformName':      'iOS',
    'platformVersion':   '8.4',
    'app':               'https://s3.amazonaws.com/appium/TestApp8.4.app.zip',
    'browserName':       '',
    'deviceOrientation': 'portrait'
}]

username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']

def launchBrowser(caps):
    caps['name'] = inspect.stack()[1][3]
    return webdriver.Remote(
            command_executor = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (username, access_key),
            desired_capabilities = caps);

def teardown_func():
    global driver
    driver.quit()
    sauce_client = SauceClient(username, access_key)
    status = sys.exc_info() == (None, None, None)
    sauce_client.jobs.update_job(driver.session_id, passed=status)

# Will generate a test for each browser and os configuration
def test_generator():
    for browser in browsers:
        yield compute_sum, browser

@with_setup(None, teardown_func)
def compute_sum(browser):
    global driver
    driver = launchBrowser(browser)
    # insert values
    field_one = driver.find_element_by_accessibility_id("TextField1")
    field_one.send_keys("12")

    field_two = driver.find_elements_by_class_name("UIATextField")[1]
    field_two.send_keys("8")

    # trigger computation by using the button
    driver.find_element_by_accessibility_id("ComputeSumButton").click();

    # is sum equal?
    sum = driver.find_element_by_class_name("UIAStaticText").text;
    assert int(sum) == 20, "ERROR MESSAGE"

