# -*- coding: utf-8 -*-
import scrapy


class ZztjSpider(scrapy.Spider):
    name = 'zztj'
    allowed_domains = ['https://www.sbkk88.com/mingzhu/gudaicn/zizhitongjian/']
    start_urls = ['http://https://www.sbkk88.com/mingzhu/gudaicn/zizhitongjian//']

    def parse(self, response):
        pass
