# -*- coding: utf-8
from bs4 import BeautifulSoup
import urllib
import requests
from collections import OrderedDict
import time
import datetime

# import sys
import config as cfg

"""
bs4 と request を使ったスクレイプ
"""

def to_curl(r):
    req = r.request
    command = "curl -X {method} -H '{headers}' -d '{data}' '{uri}'"
    method = req.method
    uri = req.url
    data = req.body
    headers = ["{0}: {1}".format(k, v) for k, v in req.headers.items()]
    headers = "' -H '".join(headers)
    return command.format(method=method, headers=headers, data=data, uri=uri)


def r_dump(r, s):
    print('==== Requests ====')
    for k, v in r.request.headers.items():
        print("%s: %s" % (k, v))
    print()
    print('==== DataBody ====')
    for p in r.request.body.split('&'):
        k, v = p.split('=')
        print("%s: %s" % (k, urllib.parse.unquote(v)))
    print()
    print('==== Cookie ====')
    for k, v in s.cookies.items():
        print("%s: %s" % (k, v))
    print()
    print('==== body ====')
    print(r.text[:10:] if len(r.text) != 0 else 'emp')


s = requests.Session()

headers = {
    'Host': 'marco.ms.dendai.ac.jp',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
    'Referer': 'https://marco.ms.dendai.ac.jp/',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'ja,en-US;q=0.8,en;q=0.6',
}


# 不動なURLである保証がない
r = s.get('https://marco.ms.dendai.ac.jp/PTDU79130R/AX0101.aspx')
soup = BeautifulSoup(r.text)

params = OrderedDict([
    ('__EVENTTARGET', ''),
    ('__EVENTARGUMENT', ''),
    ('__VIEWSTATE', soup.find('input', id='__VIEWSTATE')['value']),
    ('__EVENTVALIDATION', soup.find('input', id='__EVENTVALIDATION')['value']),
    ('TextBox_UserID', cfg.user['name']),
    ('TextBox_Password', cfg.user['passwd']),
    ('Button_Login', 'ログイン'),
])

print(params)
r = s.post('https://marco.ms.dendai.ac.jp/PTDU79130R/AX0101.aspx', data=params, headers=headers)
print(to_curl(r))

soup = BeautifulSoup(r.text)
print(soup.text)
target_day = cfg.START_DAY

# datas = []
# datas.append('')
# for i in range(cfg.REPEAT):
#     datestr = target_day.strftime("%Y/%m/%d")
#     driver.execute_script('javascript:document.getElementById("ReportViewerCont\
# rol_ctl04_ctl05_txtValue").value="' + datestr + '"')
#     click(driver, "#ReportViewerControl_ctl04_ctl00")
#     time.sleep(4)
#     while True:
#         try:
#             selector = "table table table table [valign=top]"
#             trs = driver.find_elements_by_css_selector(selector)
#             break
#         except Exception:
#             time.sleep(1)
#             continue
#     for tr in trs:
#         tds = tr.find_elements_by_css_selector('td')
#         try:
#             day, timestamp, name, code = [e.text for e in tds]
#             if day[0] is not '2':
#                 continue
#             data = ','.join([day, timestamp, name, code])
#             print(data)
#             datas.append(data)
#         except Exception:
#             pass
#     target_day = target_day + datetime.timedelta(1)
#
# f = open("./out.csv", "a")
# try:
#     f.write("\n".join(datas))
# finally:
#     f.close()
