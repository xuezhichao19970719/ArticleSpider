# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ChemicalItem

class ChemicalbookSpider(CrawlSpider):
    name = 'chemicalbook'
    allowed_domains = ['chemicalbook.com']
    start_urls = ['https://www.chemicalbook.com/ProductIndex.aspx']
    headers = {
        "HOST": "www.chemicalbook.com",
        "Referer": "https://www.chemicalbook.com/ProductIndex.aspx",
    }
    rules = (
        Rule(LinkExtractor(allow=r'CASDetailList_\d+.htm'), callback='parse_chemica', follow=True),
    )

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "HOST": "www.chemicalbook.com",
            "Referer": "https://www.chemicalbook.com/ProductIndex.aspx",
        }
    }


    def parse_chemica(self, response):
        CAS列表 = response.css('[style="width:150px;"] a::text').extract()
        中文名称列表 = response.css('[style="width:270px;"] a::text').extract()
        英文名称列表 = list(map(lambda x: x.strip(), response.css(
            '[style="width:380px;"]::text').extract()))
        化学式列表 = response.css('[style="width:200px;"] span::text').extract()

        def 获取化学结构式图片url函数(CAS):
            return 'https://www.chemicalbook.com/CAS/GIF/{}.gif'.format(CAS)

        化学结构式图片url列表 = list(map(获取化学结构式图片url函数, CAS列表))

        for CAS, 中文名称, 化学式, 英文名称, 化学结构式图片url in zip(CAS列表, 中文名称列表, 英文名称列表 , 化学式列表 , 化学结构式图片url列表):
            化学药品实例 = ChemicalItem()
            化学药品实例['CAS'] = CAS
            化学药品实例['中文名称'] = 中文名称
            化学药品实例['化学式'] = 化学式
            化学药品实例['英文名称'] = 英文名称
            化学药品实例['化学结构式图片url'] = 化学结构式图片url
            yield 化学药品实例
