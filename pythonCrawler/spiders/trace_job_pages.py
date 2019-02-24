# -*- coding: utf-8 -*-
import scrapy
from pythonCrawler.items import PythoncrawlerItem

import time as t
class pageLinks(scrapy.Spider):
    name = "links"
    #rotate_user_agent = True  # user_agent 교체하기

    allowed_domains = ["jobkorea.co.kr"]
    start_urls = ['http://www.jobkorea.co.kr/Starter/?JoinPossible_Stat=0&schPart=%2C10016%2C&schOrderBy=0&LinkGubun=0&LinkNo=0&schType=0&schGid=0&Page=1']

    def parse(self, response):
        infos = response.xpath('//*[@id="devStarterForm"]/div[2]/ul//li')
        for info in infos:
            title_link = response.urljoin(info.xpath('div[2]/div[1]/a/@href')[0].extract())

            yield scrapy.Request(title_link, callback=self.parse2) #follow link of title

    def parse2(self,response):
        item = PythoncrawlerItem()
        print('PAGE MOVE')

        item['homepage'] = response.xpath('//*[@id="container"]/section/div/article/div[2]/div[3]/dl/dd[5]/span/a/@href')[0].extract()
        #print('zz',item['homepage'])
        #t.sleep(10)
        yield item
