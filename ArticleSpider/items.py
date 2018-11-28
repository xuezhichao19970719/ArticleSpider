# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
from w3lib.html import remove_tags
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
        return str(datetime.datetime.now().date())


def remove_comment_tags(类型):
    if not 类型.endswith('评论 '):
        return 类型

def remove_splash(value):
    #去掉工作城市的斜线
    return value.replace("/","")


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)

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

class ChemicalItem(scrapy.Item):
    CAS = scrapy.Field()
    中文名称 = scrapy.Field()
    英文名称 = scrapy.Field()
    化学式 = scrapy.Field()
    化学结构式图片url = scrapy.Field()

class LagouJobItem(scrapy.Item):
    招聘职位名称 = scrapy.Field(output_processor=TakeFirst())
    招聘页面url = scrapy.Field(output_processor=TakeFirst())
    职位薪水 = scrapy.Field(output_processor=TakeFirst())
    需求工作经验 = scrapy.Field(
        input_processor=MapCompose(remove_splash),
        output_processor=TakeFirst()
    )
    需求学历 = scrapy.Field(
        input_processor=MapCompose(remove_splash),
        output_processor=TakeFirst()
    )
    工作类型 = scrapy.Field(output_processor=TakeFirst())
    工作标签 = scrapy.Field()
    招聘发布时间 = scrapy.Field(
        input_processor=MapCompose(get_date),
        output_processor=TakeFirst()
    )
    职位描述 = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
        output_processor=TakeFirst()
    )
    工作地址 = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
        output_processor=TakeFirst()
    )
    公司名称 = scrapy.Field(output_processor=TakeFirst())
    公司网址 = scrapy.Field(output_processor=TakeFirst())

    def get_insert_sql(self):
        插入数据的sql语句 = '''
            INSERT INTO LagouJob(招聘职位名称, 招聘页面url, 职位薪水, 需求工作经验, 需求学历, 工作类型, 工作标签, 招聘发布时间, 职位描述, 工作地址, 公司名称, 公司网址)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        参数 = (self['招聘职位名称'], self['招聘页面url'], self['职位薪水url'], self['需求工作经验'],self['需求学历'], self['工作类型'], self['工作标签'], self['招聘发布时间'], self['职位描述'], self['工作地址'], self['公司名称'], self['公司网址'])
        return 插入数据的sql语句, 参数
