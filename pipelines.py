# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors
from models.es_types import ArticleType
from w3lib.html import remove_tags


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article1.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

#采用同步的机制写入mysql
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', 'root', 'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, url_object_id, create_date, fav_nums)
            VALUES (%s, %s, %s, %s, %s)
        
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["url_object_id"], item["create_date"], item["fav_nums"]))
        self.conn.commit()

#用twisted提供的框架   异步api（容器）
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, setting):
        dbparams = dict(
            host = setting["MYSQL_HOST"],
            db = setting["MYSQL_DBNAME"],
            user = setting["MYSQL_USER"],
            passwd = setting["MYSQL_PASSWORD"],
            charset= 'utf8',
            cursorclass= MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        #print (item)
        #insert_sql, params = item.get_insert_sql()
        query.addErrback(self.handle_error, item, spider)#处理异常

    def handle_error(self, failure, item, spider):
        #处理一步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        #if item.__class__.__name__ == "JobBoleArticle":
        insert_sql, params = item.get_insert_sql()
        print("in do_insert")
        print(insert_sql, params)
        cursor.execute(insert_sql, params)




class JsonExporterPipeline(object):
    #调用scrapy提供的json export导出json 文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    #
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class ArticleImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item #this is important

        #pass


class ElasticsearchPipeline(object):
    #将数据写入es中

    def process_item(self, item, spider):
        #将item转换成es的数据
        '''
        article = ArticleType()
        article.title = item['title']
        article.create_date = item['create_date']
        article.content = remove_tags(item['content'])
        article.front_image_url = item['front_image_url']
        if "front_image_path" in item:
            article.front_image_path = item['front_image_path']
        article.praise_nums = item['praise_nums']
        article.fav_nums = item['fav_nums']
        article.comment_nums = item['comment_nums']
        article.url = item['url']
        article.tags = item['tags']
        article.meta.id = item['url_object_id']

        article.save()
        '''

        item.save_to_es()
        return item