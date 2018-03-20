# -*- coding: utf-8 -*-
import scrapy
import logging as log

from zizhitongjian.items import ZizhitongjianItem, ZizhitongjianContentItem


class ZztjSpider(scrapy.Spider):
    name = 'zztj'

    allowed_domains = ['www.sbkk88.com']
    start_urls = ['https://www.sbkk88.com/mingzhu/gudaicn/zizhitongjian//']
    base_urls = 'https://www.sbkk88.com/mingzhu/gudaicn/zizhitongjian/'

    # def start_requests(self):
    #     # 支持多页面爬取
    #     urls = [
    #         'https://www.sbkk88.com/mingzhu/gudaicn/zizhitongjian/'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        log.info("SCRAPING PARSE")
        # 获取目录
        body = response.css('.mingzhuLeft')
        for sel in body.xpath('ul/li'):
            item = ZizhitongjianItem()
            item['title'] = sel.xpath('a/text()').extract_first()
            try:
                if item['title'] is not None:
                    # 获取到list
                    LinkDest = response.urljoin(sel.xpath('a/@href').extract_first())
                    item['link'] = sel.xpath('a/@href').extract_first()
                    item['desc'] = ""
                    # yield item
                    yield scrapy.Request(url=LinkDest, callback=self.parse_Details, meta=item)
                    log.info("PARSE link: {0} {1} {2} {3}".format(item['title'], item['link'], item['desc'], LinkDest))

            except:
                log.info("item['title'] length unknown!")

    def parse_Details(self, response):
        log.info("PARSE_CONTENTS {}".format(response.url))
        # 获取每章内容
        subtitile = response.xpath('//*[@id="f_title1"]/h1/text()').extract_first()
        lContent = response.xpath('//*[@id="f_article"]')
        # sContent = ""
        # for i in lContent.css('p::text').extract():
        #     sContent += i
        #     sContent += '\r\n'
        # if (len(sContent) < 5):
        #     log.info("SCRAP NONE ,RESPONSE.TEXT: {0}".format(lContent.extract_first()))
        sContent = lContent.extract_first().replace("<u>一</u>", "")
        item = ZizhitongjianItem()
        item['title'] = response.meta['title']
        item['link'] = response.meta['link']
        item['desc'] = sContent
        yield item
