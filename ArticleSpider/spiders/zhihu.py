# -*- coding: utf-8 -*-
import scrapy
import re
import requests
from scrapy.http import Request


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/explore']

    def parse(self, response):
        所有问题url = response.css('[data-type="daily"] h2::attr(href)')
