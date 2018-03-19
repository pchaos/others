# -*- coding: utf-8 -*-
import scrapy
import logging as log

from zizhitongjian.items import ZizhitongjianItem

class ZztjSpider(scrapy.Spider):
    name = 'zztj'
    allowed_domains = ['https://www.sbkk88.com/mingzhu/gudaicn/zizhitongjian/']
    start_urls = ['https://www.sbkk88.com/mingzhu/gudaicn/zizhitongjian//']
    base_urls = ['https://www.sbkk88.com/mingzhu/gudaicn/zizhitongjian/']

    def parse(self, response):
        log.info("scraping parse")
        body = response.css('.mingzhuLeft')
        for sel in body.xpath('ul/li'):
            item = ZizhitongjianItem()
            item['title'] = sel.xpath('a/text()').extract_first()
            log.info("title length: {0}".format(len(item['title'])))
            if  len(item['title']) > 0:
                # 获取到list
                LinkDest = response.urljoin(sel.xpath('a/@href').extract_first())
                item['link'] = sel.xpath('a/@href').extract_first()
                item['desc'] = sel.xpath('text()').extract_first()
                log.info(item['title'], item['link'], item['desc'])
                yield item
