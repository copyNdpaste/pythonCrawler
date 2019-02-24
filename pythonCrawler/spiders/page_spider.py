# -*- coding: utf-8 -*-
import scrapy
from pythonCrawler.items import PythoncrawlerItem
from scrapy import Request
from pymongo import MongoClient

class pageLinks(scrapy.Spider):
    client = MongoClient('localhost', 27017)
    database = client.jobInfos
    collection = database.infos

    name = "jobCrawler"
    #rotate_user_agent = True #user_agent 교체하기
    allowed_domains = ["jobkorea.co.kr"]
    start_urls=[]
    dictionary = {}
    for i in range(1,6):
        start_urls.append('http://www.jobkorea.co.kr/Starter/?JoinPossible_Stat=0&schPart=%2C10016%2C&schOrderBy=0&LinkGubun=0&LinkNo=0&schType=0&schGid=0&Page='+str(i))
    def parse(self, response): #페이지의 기업 홈페이지 주소를 스크래핑함
        self.log('I just visited: ' + response.url)
        infos = response.xpath('//*[@id="devStarterForm"]/div[2]/ul//li')
        #여기서 페이지 이동해서 값 가져오는 함수 호출(???)
        for info in infos:
            item = PythoncrawlerItem()
            item['company_name'] = info.xpath('div[1]/div[1]/a/text()')[0].extract()
            link = info.xpath('div[1]/div[1]/a/@href')[0].extract()
            if link[0] == '/':
                self.log('first char is /')
                item['company_info'] = 'www.jobkorea.co.kr'+info.xpath('div[1]/div[1]/a/@href')[0].extract()
            elif link[0] == 'h':
                item['company_info'] = info.xpath('div[1]/div[1]/a/@href')[0].extract()
            item['title'] = info.xpath('div[2]/div[1]/a/span/text()')[0].extract()
            deadline = info.xpath('div[4]/span[@class="day"]/text() | div[4]/span[@class="day schedule"]/text() | div[4]/span[@class="day tomorrow"]/text() | div[4]/span[@class="day today"]/text()')[:].extract()
            item['deadline'] = deadline
            item['achievement'] = info.xpath('div[3]/span[1]/text()')[0].extract()
            item['career'] = info.xpath('div[3]/strong/text()')[0].extract()
            item['area'] = info.xpath('div[3]/span[2]/text()')[0].extract()
            item['job'] = info.xpath('div[2]/div[2]/span/text()')[:].extract()
            link = response.urljoin(info.xpath('div[2]/div[1]/a/@href')[0].extract())
            #print(link)
            #yield scrapy.Request(link, callback=self.parse_homepage)
            #lenth = len(item)
            #for i in range(lenth):
            #    self.collection.insert({list(item.keys())[i]:list(item.values())[i]})
            for key in item:
                self.dictionary[key] = item.get(key)
            self.collection.insert(self.dictionary,manipulate=False)
            #self.collection.insert({'hi': 'www.jobkorea.co.kr/Recruit/Co_Read/C/fany77sy?Oem_Code=C1&PageGbn=ST',
            #                        "sdfsdf":12})
            yield item