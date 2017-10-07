# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from scrapy.http import HtmlResponse
from ArticleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem
import datetime
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
from scrapy.loader import ItemLoader

try:
    from PIL import Image
except:
    pass



session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")

class ZhihuSpider(scrapy.Spider):
    name = "zhihu_cookies"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']
    # question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {

        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

    }
    custom_settings = {
        "COOKIES_ENABLED": True
    }

    cookies = {'d_c0': '"ADACSBPVaQuPTqj1XgYdz2SpwgU88VY0QzU=|1488860848"',
               '_zap': "94d51b03-8823-4001-ab44-8af286f574d9",
               'UM_distinctid': '15b42282af5270-0eb6c0cf0b6157-57e1b3c-100200-15b42282af6267',
               'Hm_lvt_121183b56614747c7eacae977e64ed21': '1491463580,1491463610',
               'CNZZDATA1256424439': '1217880109-1491461425-%7C1491461425',
               '_qzja': '1.300742629.1491463582081.1491463582081.1491463582082.1491463605123.1491463618537.0.0.0.3.1',
               '_jzqa': '1.3825927322562668000.1491463582.1491463582.1491463582.1',
               'q_c1': '661ac36c027248798d0a37cd157b9839|1494535341000|1488860848000',
               '_xsrf': 'e983800f653a651ba3d79cf488cf30f6',
               'capsion_ticket': '"2|1:0|10:1494537389|14:capsion_ticket|44:MTU2MDYyNDEyN2Y2NGY1MGE0MTdiMWJhZWZiNmQyNTI=|e1d1a17048467611d4cb8da5c147aa32efaa68370b14cc64319cb8f1260b4cdf"',
               's-q': 'python',
               's-i': '1',
               'sid': 'ls2lo026',
               'r_cap_id': '"Yzk1MDgyZWRkMzhjNGI1M2JkZjk5NjgwNmI0MDZiNDY=|1495256861|09112efcabd2a0514734046e66e6d09547d7bf3c"',
               'cap_id': '"NGYwZWRmODQzNjRiNDMyM2FkN2Y4YjZjODBlMzE0ZGY=|1495256861|ff7a75f618265ce25ad969dc6897d758a921cf8b"',
               '__utma': '51854390.1544797122.1494825771.1494997520.1495256861.5',
               '__utmb': '51854390.0.10.1495256861',
               '__utmc': '51854390',
               '__utmz': '51854390.1495256861.5.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/penny-40-15/activities',
               '__utmv': '51854390.000--|3=entry_date=20170306=1',
               'l_n_c': '1',
               'z_c0': 'Mi4wQUlEQ29HeWNrQXNBTUFKSUU5VnBDeGNBQUFCaEFsVk5MVnhIV1FDTzZNVndrMHpNSEZkS0xfQV9VM1JSbkpSdGRR|1495256878|11086027bb3df583c86ac6b988ee266ed521f235'
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
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            print(url)
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                #如果提取到question相关页面则下载后交由程序进行提取
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                #print(request_url, question_id)
                yield scrapy.Request(request_url, headers=self.headers, cookies =self.cookies, callback=self.parse_question)
                #break
            else:
                #如果不是question页面，则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, cookies=self.cookies, callback=self.parse)
                #pass


    def parse_question(self, response):
        #处理question页面，从页面中提取出具体的question item
        question_id = 0
        if "QuestionHeader-title" in response.text:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)

            item_loader.add_css("title", 'h1.QuestionHeader-title::text')
            #print(response.css('h1.QuestionHeader-title::text').extract())
            #print (item_loader)
            #item_loader.add_css('content', 'QuestionHeader-detail::text')
            #print(response.xpath('//div[contains(@class, "QuestionHeader-detail")]/div/div/span/text()').extract())
            item_loader.add_xpath('content', '//div[contains(@class, "QuestionHeader-detail")]/div/div/span/text()')
            item_loader.add_xpath('comments_num', '//div[contains(@class, "QuestionHeader-Comment")]/button/text()')
            item_loader.add_value('url', response.url)
            item_loader.add_value('zhihu_id', question_id)
            item_loader.add_css('answer_num', ".List-headerText span::text")
            #item_loader.add_css('comments_num', ".QuestionHeader-actions button::text")
            #item_loader.add_xpath('answer_num', '//h4[contains(@class, "List-headerText")]/span/text()')
            item_loader.add_xpath('comments_num','//div[contains(@class, "QuestionHeader-Comment")]/button/text()')
            #print (response.xpath('//div[contains(@class, "QuestionHeader-Comment")]/button/text()').extract())

            #print (response.xpath('//h4[contains(@class, "List-headerText")]/span/text()').extract())
            item_loader.add_css('watch_user_num', ".NumberBoard-value::text")
            #item_loader.add_css('topics', ".QuestionHeader-topics .Popover div::text"  #this works too
            #print(response.xpath("//*[@id='root']/div/main/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/span/a/div/div/text()").extract())
            #print(response.xpath('//div[contains(@class, "Popover")]/div/text()').extract())
            item_loader.add_xpath('topics', '//div[contains(@class, "Popover")]/div/text()')
            question_item = item_loader.load_item()
            #print (question_item)



            #处理新版本
        else:
            #处理知乎旧版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))
            item_loader = ItemLoader(item=ZhihuQuestionItem, response=response)
            item_loader.add_css('title', 'zhi-question-title h2 a::text')
            item_loader.add_css('content', '#zhi-question-detail')
            item_loader.add_value('url', response.url)
            item_loader.add_value('zhihu_id', question_id)
            item_loader.add_css('answer_num', "#zh-question-answer-num::text")
            item_loader.add_css('comments_num', "#zh-question-meta-wrap a[name='addcomment']::text")
            item_loader.add_css('watch_user_num', "#zh-question-side-header-wrap::text")
            item_loader.add_css('topics', ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers, cookies=self.cookies, callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        #处理question的answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        total_ans = ans_json["paging"]["totals"]
        next_url = ans_json["paging"]["next"]

        #提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item['zhihu_id'] = answer["id"]
            answer_item['url'] = answer["url"]
            answer_item['question_id'] = answer["question"]["id"]

            answer_item['author_id'] = answer["author"]['id'] if "id" in answer["author"] else None
            answer_item['content'] = answer["content"] if "content" in answer else None
            answer_item['praise_num'] = int(answer["voteup_count"])
            answer_item['comments_num'] = answer["comment_count"]

            answer_item['create_time'] = answer["created_time"]
            answer_item['update_time'] = answer["updated_time"]
            answer_item['crawl_time'] = datetime.datetime.now()

            yield answer_item
        if not is_end:
            yield scrapy.Request(self.start_answer_url.format(next_url, 20, 0), headers=self.headers,
                                 cookies=self.cookies, callback=self.parse_answer)

    def start_requests(self):

        return [scrapy.Request("https://www.zhihu.com/#signin", cookies=self.cookies, headers=self.headers,
                               callback=self.parse)]


    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

