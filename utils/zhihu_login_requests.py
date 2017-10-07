# -*- coding: utf-8 -*-

__author__ = 'peipei'

import requests
import re
from urllib.request import urlopen
import io
from PIL import Image
import time

try:
    import coolielib
except:
    import http.cookiejar as cookielib

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print ("cookie未能加载")

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent
}

def is_login():
    #通过个人中心页面返回状态码来判断登录状态
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    return True



def get_xsrf():
    #获取xsrf
    response = session.get("https://www.zhihu.com", headers = header)
    #text = '<input type="hidden" name="_xsrf" value="28caed5f1d4d7e10f14a93c0476415ab"/>'
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""

def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode('utf-8'))
    print ("ok")
'''
def get_captcha():
    #获取captcha
    response = session.get("https://www.zhihu.com", headers = header)
    captcha = re.match('', response.text)
'''
def get_capcha():
    url = 'http://www.zhihu.com/captcha.gif?r='+str((int(time.time()*1000)))
    file = io.BytesIO(urlopen(url).read())
    image = Image.open(file)
    image.show()

    return input('输入验证码: ')



def zhihu_login(account, password):
    #知乎登陆
    if re.match("^1\d{10}", account):
        print ("手机号码登陆")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha":get_capcha()




        }

    else:
        if "@" in account:
            #判断用户名是否为邮箱
            print("邮箱登陆")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password,
                "captcha": get_capcha()
            }

    response_text = session.post(post_url, data=post_data, headers=header)
    print (response_text)
    # 将从服务器获取的信息保存
    session.cookies.save()


zhihu_login("yupei0318@gmail.com","yumin716")
get_index()
print (is_login())


