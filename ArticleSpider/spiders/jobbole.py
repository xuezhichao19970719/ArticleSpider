# -*- coding: utf-8 -*-
#import re
import scrapy
from scrapy import Request, signals
from scrapy.loader import ItemLoader
from scrapy.xlib.pydispatch import dispatcher
from urllib import parse
from selenium import webdriver
from ..items import JobBoleArticleItem
from ..utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    handle_httpstatus_list =[404]

    def __init__(self):
        self.失败url列表 = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
    # def __init__(self):
    #     self.浏览器 = webdriver.Chrome(
    #         executable_path='E:\scrapyspider\ArticleSpider\chromedriver.exe')
    #     super().__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self, spider):
    #     print('爬虫关闭,退出Chrome')
    #     self.浏览器.quit()

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value('失败url字符串', ','.join(self.失败url列表))


    def parse(self, response):
        if response.status == 404:
            self.失败url列表.append(response.url)
            self.crawler.stats.inc_value('失败url个数')
        # 获取文章列表所有文章url
        单个页面所有文章节点 = response.css('.post.floated-thumb .post-thumb a')
        for 文章节点 in 单个页面所有文章节点:
            文章url = parse.urljoin(response.url, 文章节点.css('  ::attr(href)').extract_first(''))
            文章封面图url = parse.urljoin(response.url, 文章节点.css('img::attr(src)').extract_first(''))
            yield Request(url=文章url, meta={'文章封面图url': 文章封面图url}, callback=self.parse_detail)

        # 获取下一页url并交给scrapy下载
        '''
        下一页url = response.css('.next::attr(href)').extract_first('')
        if 下一页url:
            yield Request(url=parse.urljoin(response.url, 下一页url), callback=self.parse)
        '''

    def parse_detail(self, response):
        # 标题 = response.xpath('//*[@class="entry-header"]/h1/text()').extract()[0]
        # 创建日期 = response.xpath('//*[@class="entry-meta-hide-on-mobile"]/text()').extract()[0][16:26]
        # 收藏数 = re.search(r'\d+',response.xpath('//*[contains(@class,"bookmark-btn")]/text()').extract()[0]).group()
        # 点赞数 = response.xpath('//h10/text()').extract()[0]
        # 评论数 = re.search(r'\d+',response.xpath('//*[@href="#article-comment"]/span/text()').extract()[0]).group()
        # 类型列表 = response.xpath('//*[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        '''
        文章实例 = JobBoleArticleItem()
        文章实例['标题'] = response.css('.entry-header h1::text').extract_first('')

        文章实例['创建日期'] = re.search(r'\d{4}/\d{2}/\d{2}', response.css('.entry-meta-hide-on-mobile::text').extract_first('')).group()

        文章实例['点赞数'] = int(response.css('h10::text').extract_first('0'))

        try:
            文章实例['收藏数'] = int(re.search(r'\d+', response.css('.bookmark-btn::text').extract_first('')).group())
        except AttributeError as e:
            文章实例['收藏数'] = 0

        try:
            文章实例['评论数'] = int(re.search(r'\d+', response.css('[href="#article-comment"] span::text').extract_first('')).group())
        except AttributeError as e:
            文章实例['评论数'] = 0

        文章实例['类型列表'] = ','.join(list(filter(lambda x: not x.endswith('评论 '), response.css('.entry-meta-hide-on-mobile a::text').extract())))

        文章实例['文章url'] = response.url
        文章实例['文章url_md5'] = get_md5(response.url)
        文章实例['文章封面图url'] = [response.meta['文章封面图url']]
        '''
        # item loader 加载item
        item_loader= ItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_css('标题', '.entry-header h1::text')
        item_loader.add_css('创建日期', '.entry-meta-hide-on-mobile::text')
        item_loader.add_css('点赞数', 'h10::text')
        item_loader.add_css('收藏数', '.bookmark-btn::text')
        item_loader.add_css('评论数', '[href="#article-comment"] span::text')
        item_loader.add_css('类型列表', '.entry-meta-hide-on-mobile a::text')
        item_loader.add_value('文章url', response.url)
        item_loader.add_value('文章url_md5', get_md5(response.url))
        item_loader.add_value('文章封面图url', [response.meta['文章封面图url']])
        item_loader.add_css('文章内容', 'div.entry')

        文章实例 = item_loader.load_item()
        yield 文章实例
