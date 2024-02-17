#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import base64
import sys

# Get the arguments passed to the script
args = sys.argv

# Check if arguments were passed
if len(args) < 3:
    print("error")
    sys.exit(1)


# set Chrome options to run headless
options = Options()
options.add_argument("--headless")
options.add_argument("--start-maximized") #open Browser in maximized mode
options.add_argument("--no-sandbox") #bypass OS security model
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

# set up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# navigate to the login page
driver.get("https://portal.librus.pl/konto-librus/login?redirectTo=https%3A%2F%2Fportal.librus.pl%2Frodzina%2Fwidget&redirectCrc=9893cce82e0d4d73259da200baa80fe4e1acaea1d513abb2e9653dc9e065dbe2")

# enter the username and password
username_input = driver.find_element(By.NAME, "email")
username_input.send_keys(base64.b64decode(args[1]).decode('utf-8'))
password_input = driver.find_element(By.NAME, "password")
password_input.send_keys(base64.b64decode(args[2]).decode('utf-8'))

# submit the login form
password_input.send_keys(Keys.RETURN)


# get Token
driver.get("https://portal.librus.pl/api/v3/SynergiaAccounts")
json_data = driver.execute_script("return fetch(arguments[0]).then(response => response.json());", driver.current_url)

# close the driver
driver.quit()


print(json_data["accounts"][0]["accessToken"])
