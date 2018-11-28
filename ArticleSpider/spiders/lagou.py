# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import LagouJobItem


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    login_url = "https://passport.lagou.com/login/login.html"

    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def start_requests(self):
        browser = webdriver.Chrome(executable_path="E:\scrapyspider\ArticleSpider\chromedriver.exe")
        browser.get(self.login_url)
        browser.find_element_by_css_selector('[placeholder="请输入常用手机号/邮箱"]').send_keys("18679050075")
        browser.find_element_by_css_selector('[placeholder="请输入密码"]').send_keys("QQ767366925")
        browser.find_element_by_css_selector('[data-lg-tj-id="1j90"]').click()
        time.sleep(5)
        cookies = browser.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']
        return [scrapy.Request(self.start_urls[0], cookies=cookie_dict)]



    def parse_job(self, response):
        item_loader = ItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("招聘职位名称", ".job-name::attr(title)")
        item_loader.add_value("招聘页面url", response.url)
        item_loader.add_css("职位薪水", ".job_request .salary::text")
        item_loader.add_xpath("需求工作经验", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("需求学历", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("工作类型", "//*[@class='job_request']/p/span[5]/text()")
        item_loader.add_css("工作标签", '.position-label li::text')
        item_loader.add_css("招聘发布时间", ".publish_time::text")
        item_loader.add_css("职位描述", ".job_bt div")
        item_loader.add_css("工作地址", ".work_addr")
        item_loader.add_css("公司名称", "#job_company dt a img::attr(alt)")
        item_loader.add_css("公司网址", "#job_company dt a::attr(href)")
        job_item = item_loader.load_item()
        return job_item
