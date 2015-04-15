# -*- coding: utf-8 -*-
from selenium import webdriver
import datetime
import time
import sys
import config as cfg

def inputText(driver, s, v):
    driver.find_element_by_css_selector(s).send_keys(v)

def click(driver, s):
    driver.find_element_by_css_selector(s).click()

def clickValue(driver, s):
    click(driver, "[value*='" + s + "']")
    # click(driver, "[value*='" + s + "']")

def select(driver, name, value):
    driver.find_element_by_css_selector("select[name=" + name + "]>option[value='" + value + "']").click()

# try:
#     (tmp, username, password) = (sys.argv)
# except ValueError:
#     print("usage: $ python scrape.py [username] [password]")
#     exit()

driver = webdriver.Firefox()
url = 'https://marco.ms.dendai.ac.jp/PTDU79130R/AX0101.aspx?mode=timeout'

# login page
driver.get(url)

inputText(driver, "#TextBox_UserID", cfg.user['name'])
inputText(driver, "#TextBox_Password", cfg.user['passwd'] + "\n")

driver.execute_script('javascript:location.href="/PTDU79130R/AX1301.aspx?targeturl=https://marco.ms.dendai.ac.jp/ReportServer/Pages/ReportViewer.aspx?%2fPTDU79130R%2freport_GSY0205&params=USER_ID&rs:Command=Render&system=rs";')

target_day = cfg.START_DAY

datas = []
datas.append('')
for i in range(cfg.REPEAT):
    datestr = target_day.strftime("%Y/%m/%d")
    driver.execute_script('javascript:document.getElementById("ReportViewerControl_ctl04_ctl05_txtValue").value="' + datestr + '"')
    click(driver, "#ReportViewerControl_ctl04_ctl00")
    time.sleep(4)
    while True:
        try:
            trs = driver.find_elements_by_css_selector("table table table table [valign=top]")
            break
        except Exception:
            time.sleep(1)
            continue
    for tr in trs:
        tds = tr.find_elements_by_css_selector('td')
        try:
            day, timestamp, name, code = [e.text for e in tds]
            if day[0] is not '2':
                continue
            data = ','.join([day, timestamp, name, code])
            print(data)
            datas.append(data)
        except Exception:
            pass
    target_day = target_day + datetime.timedelta(1)
# 


f = open("./out.csv", "a")
try:
    f.write("\n".join(datas))
finally:
    f.close()
