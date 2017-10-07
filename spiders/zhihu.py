# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from scrapy.http import HtmlResponse

try:
    import urlparse as parse
except:
    from urllib import parse
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import time
import json
from scrapy.http.cookies import CookieJar
import os.path

try:
    from PIL import Image
except:
    pass

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']

    headers = {

        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

    }

    def parse(self, response):
        '''

        提取出html页面中的所有的url 并跟踪这些url进一步爬取
        如果提取的url中格式为/question/xx就下载后直接进入解析函数
        :param response: 
        :return: 
        '''

        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # all_urls = filter(lambda x: True if x.startWith("https") else False, all_urls)
        for url in all_urls:
            print(url)
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                print(request_url, question_id)

    def start_requests(self):
        return [scrapy.Request("https://www.zhihu.com/#signin", meta={'cookiejar': 1}, headers=self.headers,
                               callback=self.login)]

    def login(self, response):
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login&lang=cn"
        r = session.get(captcha_url, headers=self.headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()

        # 用pillow 的 Image 显示验证码
        # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
        captcha = input("please input the captcha\n>")

        # response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = (match_obj.group(1))

        self.headers["X-Xsrftoken"] = xsrf
        self.headers["X-Requested-With"] = "XMLHttpRequest"

        post_url = 'https://www.zhihu.com/login/email'
        postdata = {'_xsrf': xsrf,
                    'password': "yumin716",
                    'email': "yupei0318@gmail.com",

                    }
        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postdata, headers=self.headers)
        # print(login_page)
        login_code = login_page.json()
        # login_page = session.post(post_url, data=postdata, headers=headers)
        # login_code = login_page.json()
        # print(login_code['msg'])
        if login_code['r'] == 1:
            # 不输入验证码登录失败
            # 使用需要输入验证码的方式登录
            print (captcha)
            postdata["captcha"] = captcha
            ##login_page = session.post(post_url, data=postdata, headers=self.headers)
            # login_code = login_page.json()
            # print(login_code['msg'])
            ##text_json = login_page.json()
            ##resp = session.get("https://www.zhihu.com", headers=self.headers)

            session.cookies.save()

            ##with open("index_page.html", "wb") as f:
                ##f.write(resp.text.encode('utf-8'))
            # response = HtmlResponse("index_page.html",body=respon.text, encoding="utf-8")
            # return [scrapy.FormRequest(response=response)]
            # return [response]
            # print("1"+text_json['msg'])

            ##if "msg" in text_json and text_json["msg"] == "登录成功":
                ##print("successful!")
        return [scrapy.FormRequest.from_response(response,
                                                     url=post_url,
                                                     formdata=postdata,
                                                     headers=self.headers,
                                                     meta={'cookiejar': response.meta['cookiejar']},
                                                     callback=self.check_login
                                                     )]
    def check_login(self, response):
        print (response.status)
        with open("index.html", "wb") as f:
            f.write(response.text.encode('utf-8'))
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 headers=self.headers,
                                 dont_filter=True
                                 )
            #yield scrapy.Request(url, dont_filter=True, headers=self.headers)
                    # response = session.get("https://www.zhihu.com", headers=self.headers)
                    # with open("index_page1.html", "wb") as f:
                    # f.write(response.text.encode('utf-8'))