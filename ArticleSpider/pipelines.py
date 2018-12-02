# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closr(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json exporter导出json
    def __init__(self):
        self.file = open('article_exporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8',
                                         ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_closr(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    # 同步操作 io阻塞
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'test123456',
                                    'scrapyspider', charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        插入数据的sql语句 = '''
            INSERT INTO jobbole(标题, 创建日期, 文章url, 文章url_md5, 点赞数, 收藏数, 评论数, 
            类型列表, 文章封面图url, 文章封面图片保存路径)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        self.cursor.execute(插入数据的sql语句, (
        item['标题'], item['创建日期'], item['文章url'], item['文章url_md5'],
        item['点赞数'], item['收藏数'], item['评论数'], item['类型列表'],
        item['文章封面图url'][0], item['文章封面图片保存路径']))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    # twisted 提供的异步写入Mysql
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = {
            'host': settings['MYSQL_HOST'],
            'db': settings['MYSQL_DBNAME'],
            'user': settings['MYSQL_USER'],
            'password': settings['MYSQL_PASSWORD'],
            'charset': 'utf8',
            'cursorclass': MySQLdb.cursors.DictCursor,
            'use_unicode': True,
        }
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 处理异常

    def handle_error(self, failure):
        # 处理异步插入异常
        print(failure)

    def do_insert(self, cursor, item):
        插入数据的sql语句, 参数 = item.get_insert_sql()

        cursor.execute(插入数据的sql语句, 参数)


class ElasticsearchPipeline(object):
    # 数据写入es
    def process_item(self, item, spider):
        # 将item转换成es的数据
        item.save_to_es()

        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        try:
            for ok, value in results:
                文章封面图片保存路径 = value['path']
            item['文章封面图片保存路径'] = 文章封面图片保存路径
        except TypeError as e:
            print('发生错误:', e)
        finally:
            return item
