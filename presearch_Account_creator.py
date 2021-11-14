# system libraries
import os
import sys
import urllib

# recaptcha libraries
import pydub
import speech_recognition as sr
# selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json
import time
# custom patch libraries
from patch import download_latest_chromedriver, webdriver_folder_name


def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)


def getRandomWords():
    response_API = requests.get(
        'https://random-word-api.herokuapp.com//word?number=100')
    # print(response_API.status_code)
    data = response_API.text
    parse_json = json.loads(data)
    return parse_json


if __name__ == "__main__":
    # download latest chromedriver, please ensure that your chrome is up to date
    while True:
        try:
            # create chrome driver
            path_to_chromedriver = os.path.normpath(
                os.path.join(os.getcwd(), webdriver_folder_name, 'chromedriver.exe'))
            driver = webdriver.Chrome(path_to_chromedriver)
            delay()
            # go to referral website
            driver.get("https://presearch.org/signup?rid=2656285")
            # go to register page
            driver.find_element_by_xpath(
                '//*[@id="main"]/div[1]/div[2]/div/a').click()

            randomWords = getRandomWords()
            i = 0
            for words in randomWords:
                email = words + i + "mail.com"
                password = words[::-1] + i
                driver.find_element_by_xpath(
                    '//*[@id="register-form"]/form/div[1]/input').send_keys(email)

            break
        except Exception:
            # patch chromedriver if not available or outdated
            try:
                driver
            except NameError:
                is_patched = download_latest_chromedriver()
            else:
                is_patched = download_latest_chromedriver(
                    driver.capabilities['version'])
            if not is_patched:
                sys.exit(
                    "[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:"
                    "https://chromedriver.chromium.org/downloads")
