# -*- coding: utf-8 -*-
"""
Created on Mar 16 2019
@author: ggwp
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd
import os,re

usr = ""
pwd = ""

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver_for_mac")

driver = webdriver.Chrome(executable_path = DRIVER_BIN)
# driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver_for_mac")
    # .Firefox(executable_path='E:\\geckodriver.exe')

# or you can use Chrome(executable_path="/usr/bin/chromedriver_for_mac")

driver.get("http://www.facebook.org")
assert "Facebook" in driver.title
elem = driver.find_element_by_id("email")
elem.send_keys(usr)
elem = driver.find_element_by_id("pass")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)
elem = driver.find_element_by_class_name("_3ixn")
elem.click()
time.sleep(7)
# Enter the the facebook group link

driver.get("https://www.facebook.com/groups/1602756856644550")
time.sleep(5)
elem = driver.find_element_by_class_name("_3ixn")
elem.click()

print("start")
i = 0;
last_height = driver.execute_script("return document.body.scrollHeight")
print("lasthi ", last_height)
while True:
    ele = driver.find_elements_by_xpath("//div[@class='_60ri fsl fwb fcb']/a")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("scollto window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(15)
    new_height = driver.execute_script("return document.body.scrollHeight")
    print("new ",new_height)
    names = []
    links = []

    #last
    if new_height == last_height:
        for values in ele:
            names.append(values.text)
            links.append(values.get_attribute('href'))
            print(values.text)

            print(values.get_attribute('href'))
            i = i + 1

        print(i)

        break

    else:
        last_height = new_height

print(names)
print(links)
res = ["test", links]
mydfpd = pd.DataFrame(res)
# SAVE FILE TO SPESIFIC DESTINATION

mydfpd.to_csv('ciphernew.csv', index=False, header=False)