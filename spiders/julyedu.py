import scrapy

class julyEduSpider(scrapy.Spider):
    name = 'julyedu'
    start_urls = ['https://www.julyedu.com/category/index']

    def parse(self, response):
        for julyedu_class in response.xpath('//div[@class="course_info_box"]'):
            title = julyedu_class.xpath('a/h4/text()').extract_first()
            description =  julyedu_class.xpath('a/p[@class="course-info-tip"][1]/text()').extract_first()
            schedule =  julyedu_class.xpath('a/p[@class="course-info-tip"][2]/text()').extract_first()

            print (title, description, schedule)
            yield{'title': title, 'descripton': description, 'schedule': schedule}

