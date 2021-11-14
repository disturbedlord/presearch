# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 10:01:10 2020

@author: OHyic
"""

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
from selenium.webdriver.chrome.options import Options


def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)


def timeDelay(x):
    time.sleep(x)


username = 'testtest@test.com'
password = 'qwerty123'


def getRandomWords():
    response_API = requests.get(
        'https://random-word-api.herokuapp.com//word?number=100')
    # print(response_API.status_code)
    data = response_API.text
    parse_json = json.loads(data)
    return parse_json


def captcha2(siteKey):
    call2Captcha = requests.get(
        "http://2captcha.com/in.php?key=3d0ea8c5ec7605361b2178ad1cf81d61&method=userrecaptcha&googlekey=" + siteKey + "&pageurl=https://presearch.org/login&json=1")
    data = call2Captcha.json()
    requestId = data["request"]
    print(requestId)
    googleResponseCode = ""
    while(1):
        timeDelay(15)
        call2Captcha = requests.get(
            "http://2captcha.com/res.php?key=3d0ea8c5ec7605361b2178ad1cf81d61&action=get&json=1&id=" + requestId)
        data = call2Captcha.json()
        print(data)
        res = data["status"]
        if(res == 1):
            googleResponseCode = data["request"]
            break

    gRecaptchResponseElement = driver.find_element_by_id(
        "g-recaptcha-response")
    driver.execute_script(
        "arguments[0].innerHTML = arguments[1]", gRecaptchResponseElement, googleResponseCode)
    # wait for the Recaptcha to close
    timeDelay(5)
    # Click on Login Btn
    driver.find_element_by_xpath(
        '//*[@id="login-form"]/form/div[3]/div[3]/button').click()


def getDataSiteKey():
    data = driver.find_element_by_xpath(
        '//*[@id="login-form"]/form/div[3]/div[2]/div')
    return data.get_attribute("data-sitekey")


if __name__ == "__main__":
    # download latest chromedriver, please ensure that your chrome is up to date
    while True:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")

            # create chrome driver
            path_to_chromedriver = os.path.normpath(
                os.path.join(os.getcwd(), webdriver_folder_name, 'chromedriver.exe'))
            driver = webdriver.Chrome(
                path_to_chromedriver, options=chrome_options)
            delay()
            # go to website
            driver.get("https://presearch.org/login")
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

        # solveCaptcha()

    driver.find_element_by_xpath(
        '//*[@id="login-form"]/form/div[1]/input').send_keys(username)
    driver.find_element_by_xpath(
        '//*[@id="login-form"]/form/div[2]/div/input').send_keys(password)

    siteKey = getDataSiteKey()
    captcha2(siteKey)
    # input()
    delay(15)
    close = driver.find_element_by_xpath('/html/body/div[3]/button').click()

    data = getRandomWords()
    i = 0
    while(i < 100):
        searchBar = driver.find_element_by_id('search').send_keys(data[i])
        driver.find_element_by_xpath(
            '//*[@id="search-input"]/div/span/button').click()
        delay(15)
        timeDelay(5)
        html = driver.find_element_by_tag_name('html')
        driver.execute_script("window.scrollTo(0, 50)")
        timeDelay(1)
        driver.execute_script("window.scrollTo(0, 150)")
        timeDelay(2)
        driver.execute_script("window.scrollTo(0, 300)")
        timeDelay(3)

        driver.get("https://presearch.org")
        i += 1
    driver.close()
