import scrapy

class manySpider(scrapy.Spider):
    name = 'manyspider'
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        for joke in response.xpath('//div[@class="quote"]'):
            content = joke.xpath('span[1]/text()').extract_first()
            author = joke.xpath('span[2]/small/text()').extract_first()


            print (content, author)
            yield{"content": content, "author": author}
            next_page =  response.xpath('//li[@class="next"]/a/@href').extract_first()
            if next_page:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

