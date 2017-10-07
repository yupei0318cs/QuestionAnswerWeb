#-*- coding: UTF-8 -*-

import scrapy, json
import io
from PIL import Image
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request
import time
class ZhihuSpider(scrapy.spiders.Spider):
    #name = 'zhihuu'

    # 最开始的请求
    def start_requests(self):
     # 这个请求用来获取cookie，以及获取xsrf字段
        return [FormRequest("http://www.zhihu.com/login/email", callback=self.init)]

    def init(self,response):
     # 获取了cookir和xsrf字段后向验证码地址发请求，此时scrapy会自动在请求上带上cookie
        self._xsrf = Selector(response).xpath('//input[@name="_xsrf"][email protected]').extract()[0]
        return Request('http://www.zhihu.com/captcha.gif?r='+time.time()*1000, callback=self.login)

    def getcapid(self,response):
     # 显示验证码，接收用户输入，返回验证码。显示图片使用PIL库，在OSX上可以直接调用预览显示图片，别的系统不知道了。
        Image.open(io.StringIO(response.body)).show()
        return input('输入验证码: ')

    def login(self,response):
     # 登录动作
        return FormRequest("http://www.zhihu.com/login/email",formdata={
        'email': 'yupei0318@gmail.com',
        'password': 'yumin716',
        'remember_me':'true',
        '_xsrf': self._xsrf,
        'captcha': self.getcapid(response),
        },callback=self.after_login)

    def after_login(self,response):
     # 现在已经收到登录请求的响应了
        if json.loads(response.body)['msg'].encode('utf8') == "登陆成功":
            yield self.make_requests_from_url('http://www.zhihu.com/people/penny-40-15')
        else:
            print ("验证码错误")

    def parse(self,response):
        print(response.body)