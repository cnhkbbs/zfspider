# zfspider
正方教务成绩爬虫
# 使用
## 文件结构
```
spider.py 爬虫主程序(返回未处理的网页，并保存为 用户名+.text)
cookfood.py 结果整理程序(返回处理完成的html字符串，以供服务端调用)
```
## 步骤
- 设置spider.py的配置项
```
gnmkdm = 'N123456'    gnmkdm值
host_list = ['http://127.0.0.1', 'http://127.0.0.1']  教务网服务器地址
```
- 设置账号密码姓名
```
if __name__ == '__main__':
    zf_spider('123456789', 'password', '张三')
```
- 使用cookfood.py处理结果
# 代码预览

```
# -*- coding:utf-8 -*-
# --------------------
# 20230520
# by sboxm
# --------------------
from bs4 import BeautifulSoup as bf
import requests
import ddddocr
import datetime
import urllib.parse

gnmkdm = 'N123456'
host_list = ['http://127.0.0.1', 'http://127.0.0.1']
headers = [{
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"},
           {
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42"},
           {
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"},
           {
               "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"},
           {
               "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36"}]


def print_INFO(message):
    print('[' + datetime.datetime.now().strftime('%H:%M:%S') + ']' + message)


def print_ERROR(error):
    print('[' + datetime.datetime.now().strftime('%H:%M:%S') + ']' + "\033[1;31m" + error + " \033[0m")


# 验证码处理
def CheckCode(url, head):
    img_url = url + 'CheckCode.aspx'
    try:
        checkcode_img = requests.get(img_url, headers=head, stream=True).content
    except requests.exceptions:
        return False
    with open('checkdoce.png', 'wb') as img:
        img.write(checkcode_img)
    ocr = ddddocr.DdddOcr(show_ad=False)
    checkcode = ocr.classification(checkcode_img)
    return checkcode


def zf_spider(username, password, name, host=0, header=0):
    # 创建会话
    session = requests.Session()
    try:
        login_page = session.get(host_list[host], headers=headers[header])
    except requests.exceptions:
        return {'massage': 'request error', 'status': False}
    if login_page.status_code != 200:
        print_ERROR('访问被拒绝')
        return {'massage': '501Error', 'status': False}

    # 响应处理
    basic_url = login_page.url[0:49]
    print_INFO('响应url:' + basic_url)
    page_soup = bf(login_page.text, 'html.parser')
    viewstate = page_soup.find('input', {'name': '__VIEWSTATE'})['value']
    print_INFO('获取到的viewstate:' + viewstate)

    # 获取验证码
    checkcode = CheckCode(basic_url, headers[header])
    if not checkcode:
        print_ERROR('验证码识别出错')
        return {'massage': 'get checkcode false', 'status': False}
    else:
        print_INFO('获取到的验证码:' + str(checkcode))
    pass

    # 模拟登录请求
    login_header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0", "Connection": "keep-alive", "Content-Length": "191",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": host_list[host][7:],
        "Origin": host_list[host],
        "Referer": basic_url + "default2.aspx",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": headers[header]["User-Agent"]
    }
    login_data = {
        "__VIEWSTATE": viewstate,
        "txtUserName": username,
        "TextBox2": password,
        "txtSecretCode": checkcode,
        "RadioButtonList1": "%D1%A7%C9%FA",
        "Button1": "",
        "lbLanguage": "",
        "hidPdrs": "",
        "hidsc": ""
    }
    try:
        try_login = requests.session().post(basic_url + "default2.aspx", data=login_data, headers=login_header)
    except requests.exceptions:
        return {'massage': 'request error', 'status': False}
    if try_login.status_code != 200:
        print_ERROR('尝试登录失败')
        return {'massage': 'request forbidden', 'status': False}
    else:
        print_INFO('尝试登录成功')

    # 获取新的VIEWSTATE
    new_header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Host": host_list[host][7:],
        "Referer": basic_url + "xs_main.aspx?xh=" + username,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": headers[header]["User-Agent"]
    }
    try:
        new_resp = requests.session().get(
            basic_url + "xscjcx.aspx?xh=" + username + "&xm=" + urllib.parse.quote(name) + "&gnmkdm="+gnmkdm,
            headers=new_header)
    except requests.exceptions:
        return {'massage': 'request error', 'status': False}
    if new_resp.status_code != 200:
        print_ERROR('获取新VIEWSTATE失败')
        return {'massage': 'get new viewstate failed', 'status': False}
    else:
        print_INFO('获取VIEWSTATE成功')
    new_page_soup = bf(new_resp.text, 'html.parser')
    new_viewstate = new_page_soup.find('input', {'name': '__VIEWSTATE'})['value']
    # 尝试获取成绩
    score_header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0", "Connection": "keep-alive", "Content-Length": "191",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": host_list[host][7:],
        "Origin": host_list[host],
        "Referer": basic_url + "xscjcx.aspx?xh=" + username + "&xm=" + urllib.parse.quote(name) + "&gnmkdm="+gnmkdm,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": headers[header]["User-Agent"]
    }
    score_data = {
        'btn_zcj': '%C0%FA%C4%EA%B3%C9%BC%A8',
        'ddlXN': '',
        'ddlXQ': '',
        '__EVENTVALIDATION': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': new_viewstate,
        'hidLanguage': '',
        'ddl_kcxz': ''
    }
    # 发送查询请求
    try:
        score = requests.session().post(
            basic_url + "xscjcx.aspx?xh=" + username + "&xm=" + urllib.parse.quote(name) + "&gnmkdm="+gnmkdm,
            data=score_data, headers=score_header)
    except requests.exceptions:
        return {'massage': 'request error', 'status': False}
    if score.status_code != 200:
        print_ERROR('查询失败')
        return {'massage': 'getting scores failed', 'status': False}
    else:
        print_INFO('查询成功')
    with open('scores/' + username + '.txt', 'w', encoding='utf-8') as save:
        save.write(score.text)
    return {'massage': 'succeed', 'status': True}


if __name__ == '__main__':
    zf_spider('123456789', 'password', '张三')
```
