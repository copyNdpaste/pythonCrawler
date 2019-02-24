# -*- coding: utf-8 -*-
import scrapy
from pythonCrawler.items import PythoncrawlerItem
from pymongo import MongoClient

class JobCrawler(scrapy.Spider):
    name = 'JobCrawler'
    client = MongoClient('localhost', 27017)  # 로컬 서버의 27017 port에 MongoDB 연동
    database = client.jobInfos  # Database 이름은 jobInfos
    collection = database.infos  # collection 이름은 infos
    allowed_domains = ["jobkorea.co.kr", "saramin.co.kr"]
    start_urls=[]
    dictionary = {}
    def start_requests(self):
        #for i in range(1, 2):
        yield scrapy.Request(
            'http://www.jobkorea.co.kr/Starter/?JoinPossible_Stat=0&schPart=%2C10016%2C&schOrderBy=0&LinkGubun=0&LinkNo=0&schType=0&schGid=0&Page=1',
            self.parse_jobkorea)
            #yield scrapy.Request('http://www.jobkorea.co.kr/Starter/?JoinPossible_Stat=0&schPart=%2C10016%2C&schOrderBy=0&LinkGubun=0&LinkNo=0&schType=0&schGid=0&Page=%d' % i, self.parse_jobkorea)
            #yield scrapy.Request('http://www.saramin.co.kr/zf_user/jobs/public/list/page/%d?up_cd%5B0%5D=3&sort=ud&listType=public&public_list_flag=y&up_cd_list%5B0%5D%5B0%5D=301&up_cd_list%5B0%5D%5B1%5D=302&up_cd_list%5B0%5D%5B2%5D=303&up_cd_list%5B0%5D%5B3%5D=304&up_cd_list%5B0%5D%5B4%5D=305&up_cd_list%5B0%5D%5B5%5D=306&up_cd_list%5B0%5D%5B6%5D=307&up_cd_list%5B0%5D%5B7%5D=308&up_cd_list%5B0%5D%5B8%5D=309&page=%d#searchTitle' % i % i, self.parse_saramin)
    def parse_jobkorea(self, response):  # 페이지의 기업 홈페이지 주소를 스크래핑함
        self.log('I just visited: ' + response.url)
        infos = response.xpath('//*[@id="devStarterForm"]/div[2]/ul//li')
        # 여기서 페이지 이동해서 값 가져오는 함수 호출
        for info in infos:
            item = PythoncrawlerItem()  # items.py에서 지정한 model
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
            try:
                item['achievement'] = info.xpath('div[3]/span[1]/text()')[0].extract()
            except IndexError:
                item['achievement'] = 'no'
            item['career'] = info.xpath('div[3]/strong/text()')[0].extract()
            item['area'] = info.xpath('div[3]/span[2]/text()')[0].extract()
            item['job'] = info.xpath('div[2]/div[2]/span/text()')[:].extract()
            for key in item:
                self.dictionary[key] = item.get(key)
            self.collection.insert(self.dictionary, manipulate=False)
            yield item  # yield는 데이터가 쌓이도록 해줌
    def parse_saramin(self, response):
        self.log('I just visited: ' + response.url)
        infos = response.xpath('//tbody//tr')
        for info in infos:
            item = PythoncrawlerItem()
            item['company_name'] = info.xpath('td[2]/a/@title')[0].extract()
            link = 'http://www.saramin.co.kr' + info.xpath('td[2]/a/@href')[0].extract()
            item['company_info'] = link
            item['title'] = info.xpath('td[3]/div/a/@title')[0].extract()
            item['deadline'] = info.xpath('td[6]/p[@class="deadlines"]/text()')[0].extract()
            item['achievement'] = info.xpath('td[4]/p[@class="education"]/text()')[0].extract()
            item['career'] = info.xpath('td[4]/p[@class="career"]/text()')[0].extract()
            item['area'] = info.xpath('td[5]/p[@class="work_place"]/text()')[0].extract()
            item['job'] = info.xpath('td[3]/div[2]/span/text()')[:].extract()
            for key in item:
                self.dictionary[key] = item.get(key)
            self.collection.insert(self.dictionary, manipulate=False)
            yield item  # yield는 데이터가 쌓이도록 해줌'''