# -*- coding: utf-8 -*-

from selenium import webdriver
from scrapy.selector import Selector

浏览器 = webdriver.Chrome(executable_path='E:\scrapyspider\ArticleSpider\chromedriver.exe')
浏览器.get('https://www.zhihu.com/signin')
浏览器.find_element_by_css_selector('input[name="username"]').send_keys('767366925@qq.com')
浏览器.find_element_by_css_selector('input[name="password"]').send_keys('QQ767366925')
浏览器.find_element_by_css_selector('.SignFlow-submitButton').click()
页面html = Selector(text=浏览器.page_source)

print(页面html.css('.SignFlowHeader-slogen::text').extract())