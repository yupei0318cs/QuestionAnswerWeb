import time
print (int(time.time()*1000))

    ''''
    def login(self, response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
        xsrf= ''
        if match_obj:
            xsrf = (match_obj.group(1))

        if xsrf:
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "yupei0318@gmail.com",
                "password": "yumin716",
                "captcha": self.get_captcha()

            }
            return [scrapy.FormRequest(
                url = post_url,
                formdata = post_data,
                headers = self.headers,
                callback=self.check_login
            )]
'''
''''
   def check_login(self, response):
       # 通过查看用户个人信息来判断是否已经登录
       url = "https://www.zhihu.com/settings/profile"
       login_code = session.get(url, headers=self.headers, allow_redirects=False).status_code
       if login_code == 200:
           print("success")
           for url in self.start_urls:
               yield scrapy.Request(url, dont_filter=True, headers=self.headers)
       else:
           print('not successful')
   '''


                 '''   
            return scrapy.FormRequest.from_response(
                response = response,
                formdata = postdata,
                callback=self.check_login
            )
            #login_page = session.post(post_url, data=postdata, headers=self.headers)
            #login_code = login_page.json()

            '''

            # 保存 cookies 到文件，
        # 下次可以使用 cookie 直接登录，不需要输入账号和密码
        #session.cookies.save()
'''
    def check_login(self, response):
        print("After LOGIN")
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            print("successful!")
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers )
        else:
            print ("unsuccessful!")
'''


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




    def login(self, response):
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
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
        #response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = (match_obj.group(1))

        self.headers["X-Xsrftoken"] = xsrf
        self.headers["X-Requested-With"] = "XMLHttpRequest"

        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': xsrf,
            'password': "yumin716",
            'email': "yupei0318@gmail.com"
        }
        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postdata, headers=self.headers)
        #print(login_page)
        login_code = login_page.json()
        #login_page = session.post(post_url, data=postdata, headers=headers)
        #login_code = login_page.json()
        #print(login_code['msg'])
        if login_code['r'] == 1:
            # 不输入验证码登录失败
            # 使用需要输入验证码的方式登录
            postdata["captcha"] = captcha
            login_page = session.post(post_url, data=postdata, headers=self.headers)
            text_json = login_page.json()
            session.cookies.save()
            #print(text_json['msg'])
            #response = session.get("https://www.zhihu.com", headers=self.headers)

            print (text_json["msg"])

            return scrapy.FormRequest.from_response(
                response=response.meta['previous_response'],
                formdata=postdata,
                callback=self.check_login
            )

        def start_requests(self):
            return [scrapy.Request("https://www.zhihu.com/#signin", headers=self.headers, callback=self.login)]


                    #text_json = json.loads(response.text)
                    #print (text_json)
                    #all_urls = response.css("a::attr(href)").extract()
                    #all_urls = [parse.urljoin(response.url, url) for url in all_urls]
                    #for url in all_urls:
                        #pass




    def check_login(self, response):

        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        print (text_json['msg'])
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

                '''
                        return [scrapy.FormRequest(
                            url=post_url,
                            meta={'cookiejar': response.meta['cookiejar']},
                            formdata={
                                '_xsrf': xsrf,
                                'password': "yumin716",
                                'email': "yupei0318@gmail.com",
                                'captcha': self.get_captcha(),
                            },
                            headers=self.headers,
                            callback= self.check_login,
                            dont_filter = True)]


                        #print (session.cookies)
                        #print(text_json['msg'])
                        #response = session.get("https://www.zhihu.com", headers=self.headers)
                        #cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
                        #print (text_json["msg"])
                        #print (response.text)

                        return [scrapy.FormRequest.from_response(response, formnumber=0,
                                                          formdata=postdata,
                                                          callback=self.check_login)]
import scrapy, json
import io
from PIL import Image
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request
from urllib.request import urlopen
import urllib.request
import requests
session = requests.session()
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent
}
def get_chapcha():

     # 显示验证码，接收用户输入，返回验证码。显示图片使用PIL库，在OSX上可以直接调用预览显示图片，别的系统不知道了。
    #url = "https://www.zhihu.com/captcha.gif?r=1494628214735"

    #image = urllib.request.urlopen(url)  # The url you want to open

    response = session.get("https://www.zhihu.com", headers=header)


    #Image.open(io.StringIO(response.body)).show()
    file = io.BytesIO(urlopen(url).read())
    image = Image.open(file)
    image.show()
    return input('输入验证码: ')
    #return Request('http://www.zhihu.com/captcha.gif?r=1494628214735')

#print (get_chapcha())