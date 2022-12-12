from altunityrunner import *
from datetime import timedelta
from selenium import webdriver
import os
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
    disconnect_session = f"java -jar {test_data.sauce_jar} disconnect --sessionId {test_data.sauce_session_id}"
    os.system(disconnect_session)
    os.system("adb disconnect localhost:7001")


def start_session():
    caps = {}
    caps['platformName'] = 'Android'
    caps['appium:app'] = 'storage:filename=trashcat.apk'
    caps['appium:deviceName'] = 'Samsung_Galaxy_S8_POC144'
    caps['appium:automationName'] = 'UiAutomator2'
    caps['sauce:options'] = {}
    caps['sauce:options']['build'] = '<your build id>'
    caps['sauce:options']['name'] = '<your test name>'
    username = test_data.from_env("SAUCE_USERNAME")
    access_key = test_data.from_env("SAUCE_ACCESS_KEY")
    url = f'https://{username}:{access_key}@ondemand.us-west-1.saucelabs.com:443/wd/hub'
    print("Starting Appium WebDriver...")
    test_data.driver = webdriver.Remote(url, caps)
    print("Session ID: " + test_data.driver.session_id)
    print("Connecting to Sauce Labs session...")
    test_data.sauce_jar = test_data.from_env("SAUCE_VUSB_JAR")
    start_vusb = f"java -jar {test_data.sauce_jar} server --datacenter US"
    os.popen(start_vusb)
    get_sessions = f"java -jar {test_data.sauce_jar} sessions --username {username} --accessKey {access_key}"
    sessions = os.popen(get_sessions).read()
    test_data.sauce_session_id = sessions.split("\n")[2].split()[0]
    connect_session = f"java -jar {test_data.sauce_jar} connect --sessionId {test_data.sauce_session_id} --username {username} --accessKey {access_key}"
    os.system(connect_session)
    os.system("adb connect localhost:7001")
    print("Sauce Session ID: " + test_data.sauce_session_id)
    print("Forwaring port for AltUnity...")
    AltUnityPortForwarding.forward_android()
    test_data.altUnityDriver = AltUnityDriver()
    print("Forwarded.")
