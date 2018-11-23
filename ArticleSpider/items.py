# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def get_nums(value):
    try:
        数字 = int(re.search(r'\d+', value).group())
    except AttributeError:
        数字 = 0
    finally:
        return 数字


def get_date(value):
    try:
        日期 = re.search(r'\d{4}/\d{2}/\d{2}', value).group()
        return 日期
    except AttributeError:
        pass


def remove_comment_tags(类型):
    if not 类型.endswith('评论 '):
        return 类型


class JobBoleArticleItem(scrapy.Item):
    标题 = scrapy.Field(
        output_processor=TakeFirst()
    )
    创建日期 = scrapy.Field(
        input_processor=MapCompose(get_date),
        output_processor=TakeFirst()
    )
    文章url = scrapy.Field(
        output_processor=TakeFirst()
    )
    文章url_md5 = scrapy.Field(
        output_processor=TakeFirst()
    )
    点赞数 = scrapy.Field(
        input_processor=MapCompose(get_nums),
        output_processor=TakeFirst()
    )
    收藏数 = scrapy.Field(
        input_processor=MapCompose(get_nums),
        output_processor=TakeFirst()
    )
    评论数 = scrapy.Field(
        input_processor=MapCompose(get_nums),
        output_processor=TakeFirst()
    )
    类型列表 = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(',')
    )
    文章封面图url = scrapy.Field()
    文章封面图片保存路径 = scrapy.Field()

    def get_insert_sql(self):
        插入数据的sql语句 = '''
            INSERT INTO jobbole(标题, 创建日期, 文章url, 文章url_md5, 点赞数, 收藏数, 
            评论数, 类型列表, 文章封面图url, 文章封面图片保存路径)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        参数 = (self['标题'], self['创建日期'], self['文章url'], self['文章url_md5'],
              self['点赞数'], self['收藏数'], self['评论数'], self['类型列表'],
              self['文章封面图url'][0], self['文章封面图片保存路径'])
        return 插入数据的sql语句, 参数
