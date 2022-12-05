from altunityrunner import *
from datetime import timedelta
from selenium import webdriver
import time
import test_data


def before_scenario(context, scenario):
    """ This runs before each scenario. """
    test_data.init()
    test_data.time_start = time.time()
    start_session()


def after_scenario(context, scenario):
    end_session()
    test_data.time_end = time.time()
    time_taken = timedelta(seconds=test_data.time_end - test_data.time_start)
    print("\n" + '\033[94m' + "  Total Test Time: " + str(time_taken) + '\033[0m')


def end_session():
    if test_data.altUnityDriver != None:
        test_data.altUnityDriver.stop()
        AltUnityPortForwarding.remove_forward_android()


def start_session():
    caps = {}
    caps['platformName'] = "Android"
    caps['appium:deviceName'] = "Android GoogleAPI Emulator"
    caps['appium:deviceOrientation'] = "portrait"
    caps['appium:platformVersion'] = "12.0"
    caps['appium:automationName'] = "UiAutomator2"
    caps['appium:app'] = "storage:filename=trashcat.apk"
    caps['sauce:options'] = {}
    caps['sauce:options']['build'] = '<your build id>'
    caps['sauce:options']['name'] = '<your test name>'
    username = test_data.from_env("SAUCE_USERNAME")
    access_key = test_data.from_env("SAUCE_ACCESS_KEY")
    url = f'https://{username}:{access_key}@ondemand.us-west-1.saucelabs.com:443/wd/hub';
    driver = webdriver.Remote(url, caps)
    AltUnityPortForwarding.forward_android()
    test_data.altUnityDriver = AltUnityDriver()
