import scrapy

class cnBlogSpider(scrapy.Spider):
    name = 'cnblog'
    start_urls = ['https://www.cnblogs.com/pick/#p%s' % p for p in range(1, 21)]
    print (start_urls)

    def parse(self, response):
        for blog in response.xpath('//div[@class="post_item"]'):
            
            votes = blog.xpath('div[@class="digg"]/div/span/text()').extract_first()
            title = blog.xpath('div[@class="post_item_body"]/h3/a/text()').extract_first()
            print (title, votes)
            yield{'title': title,  'votes': votes}

