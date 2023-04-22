from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
import pandas as pd
import os, re

#### Config ####
usr = ""
pwd = ""
time_scroll = 1  # second

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver_for_mac")

def main():
    #### open website and login ####
    driver = webdriver.Chrome(executable_path=DRIVER_BIN)
    driver.get("http://www.facebook.org")
    assert "Facebook" in driver.title
    elem = driver.find_element_by_id("email")
    elem.send_keys(usr)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    elem = driver.find_element_by_class_name("_3ixn")
    elem.click()

    #### open list_group ####
    df = pd.read_csv("list_group.csv")

    #### go to each group ####
    for id, name in zip(df.id, df.name):
        # print(item)
        print("Start fetching...." + str(id))

        driver.get("https://www.facebook.com/groups/"+str(id))
        time.sleep(5)
        elem = driver.find_element_by_class_name("_3ixn")
        elem.click()
        time.sleep(5)

        ##### SCROLL LOAD #####
        time_out = time.time() + time_scroll
        while True:
            if time.time() > time_out:
                print("scroll time out")
                break
            else:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

        ##### OPEN SEE MORE ####
        print("open see more")
        driver.execute_script(
            "var elems = document.getElementsByClassName('see_more_link');for(var i= 0;i<elems.length;i++){elems[i].click();}");
        time.sleep(10)

        ##### OPEN VIEW MORE COMMENT ####
        print("open view more comment")
        driver.execute_script(
            "var elems = document.getElementsByClassName('_4sxc _42ft');for(var i= 0;i<elems.length;i++){elems[i].click();}");
        time.sleep(10)

        ##### Scrape & Cut only tel (raw)
        html = driver.page_source
        # ele = driver.find_elements()
        raw_tel = []
        # 0912345678
        raw_tel.append(re.findall(r"\s[0][689]\d{8}", html))
        #0912345678
        raw_tel.append(re.findall(r"[0][689]\d{8}\s", html))
        #091-2345678
        raw_tel.append(re.findall(r"[0][689][0-9]-\d{7}\s", html))
        # 091-2345678
        raw_tel.append(re.findall(r"\s[0][689][0-9]-\d{7}", html))
        #091-234-5678
        raw_tel.append(re.findall(r"[0][689][0-9]-\d{3}-\d{4}\s", html))
        # 091-234-5678
        raw_tel.append(re.findall(r"\s[0][689][0-9]-\d{3}-\d{4}", html))
        #d091-2345678
        raw_tel.append(re.findall(r"[A-Za-zก-๙][0][689]\d{8}", html))
        #091-2345678d
        raw_tel.append(re.findall(r"[0][689]\d{8}[A-Za-zก-๙]", html))
        #d091-2345678d
        raw_tel.append(re.findall(r"[A-Za-zก-๙][0][689]\d{8}[A-Za-zก-๙]", html))
        print(raw_tel)

        ##### screen raw to data
        tels = []
        for i in range(len(raw_tel)):
            # print(i)
            for x in raw_tel[i]:
                # x.replace('ก-๙', 'e')
                s = re.sub('[ ก-๙a-zA-Z\-]+', '', x)
                tels.append(s)

        if not os.path.isdir('data/'+name):
            # print('new directry has been created')
            os.makedirs('data/'+name)

        ##### Save tel phone & remove repeat#####
        mydfpd = pd.DataFrame(list(dict.fromkeys(tels)))
        mydfpd.to_csv("data/" + name + "/" + str(datetime.date.today()) + ".csv", index=None, header=None)

if __name__ == '__main__':
    main()
