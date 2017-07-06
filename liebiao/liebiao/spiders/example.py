# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import requests
import re
from scrapy.selector import Selector
from liebiao.items import LiebiaoItem
from selenium import webdriver


class ExampleSpider(scrapy.Spider):
    name = 'liebiao'
    allowed_domains = ['liebiao.com']
    # start_urls = ['http://anshun.liebiao.com/', 'http://anqing.liebiao.com/']
    start_urls = [ 'http://ankang.liebiao.com/', 'http://ali.liebiao.com/', 'http://aletai.liebiao.com/', 'http://alashan.liebiao.com/', 
                   'http://alaer.liebiao.com/', 'http://akesu.liebiao.com/', 'http://aba.liebiao.com/', 'http://beijing.liebiao.com/', 
                   'http://baoding.liebiao.com/', 'http://baotou.liebiao.com/', 'http://binzhou.liebiao.com/', 'http://baicheng.liebiao.com/', 
                   'http://bengbu.liebiao.com/', 'http://benxi.liebiao.com/', 'http://bijie.liebiao.com/', 'http://boertala.liebiao.com/', 
                   'http://beihai.liebiao.com/', 'http://bazhong.liebiao.com/', 'http://bayinguoleng.liebiao.com/', 'http://bayannaoer.liebiao.com/', 
                   'http://baoshan.liebiao.com/', 'http://baoji.liebiao.com/', 'http://baiyin.liebiao.com/', 'http://baishan.liebiao.com/']
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    def parse(self, response):
        for each in response.selector.css('.xb-box-1>dl>dd>ul>li>a ::attr(href)').extract():
            yield scrapy.Request(url= str(response.url)[:-1] + each, callback=self.get_url)
    
    def get_url(self,response):
        for each in response.selector.css('.fang-title ::attr(href)').extract():
            yield scrapy.Request(url=each,callback=self.detail)
        if response.selector.css('.next a'):
            next_url = response.selector.css('.next a ::attr(href)').extract()[0]
            yield scrapy.Request(url=next_url,callback=self.get_url)

    def detail(self,response):
        item = LiebiaoItem()
        item['name'] = response.selector.css('.name ::text').extract()[0].strip()
        tel = response.selector.css('.lxr-phone .phone-size ::text').extract()[0]
        item['tel'] = tel
        # item['addr'] = ''.join(response.selector.css('.detail-right>a ::text').extract())
        prefix_addr = response.selector.css('.weizhi ::text').extract()[0]
        item['addr'] = ''.join(response.selector.css('.detail-content dl:last-child .detail-right a ::text').extract()) + prefix_addr
        # item['belongtowhere'] = ''
        label_url = "http://www.ip138.com:8080/search.asp?action=mobile&mobile=" + tel.strip()
        wb_data = requests.get(label_url,headers=self.headers)
        wb_data.encoding = 'gb2312'
        item['belongtowhere'] = ''.join(Selector(response=wb_data).css('.tdc2 ::text').extract()[4:5]).replace(r'\ax0','')
        yield item


    # def detail(self,response):
    #     item = LiebiaoItem()
    #     item['name'] = response.selector.css('.name ::text').extract()[0].strip()
    #     tel = response.selector.css('.lxr-phone .phone-size ::text').extract()[0]
    #     item['tel'] = tel
    #     item['addr'] = ''.join(response.selector.css('.detail-right a ::text').extract())

    #     label_url = "http://www.ip138.com:8080/search.asp?action=mobile&mobile=" + tel.strip()
    #     wb_data = requests.get(label_url,headers=self.headers)
    #     wb_data.encoding = 'gb2312'
    #     soup = BeautifulSoup(wb_data.text, 'lxml')
    #     page_lists = soup.select('body')
    #     address_pat = '卡号归属地[\d\D]*?</tr>' 
    #     pat="<.*?>"
    #     position_data = re.search(address_pat,str(page_lists))
    #     position_data = re.sub(pat, "",position_data.group()).replace(" -->","").replace("卡号归属地","").replace("\n","")
    #     item['belongto'] = position_data
    #     yield item



    # def get_phone_address_bj(request):
    
    #     obj = models.Label_msg_bj.objects.filter(phone_address="")
    #     for i in obj:
        
    #         label_url="http://www.ip138.com:8080/search.asp?action=mobile&mobile="
    #         if len(i.phone) == 11 and "-" not in i.phone and i.phone[0]=="1":
    #             time.sleep(0.6)
    #             label_url = label_url+i.phone.strip()
    #             wb_data = requests.get(label_url,headers=headers)
    #             wb_data.encoding = 'gb2312'

    #             soup = BeautifulSoup(wb_data.text, 'lxml')
    #             page_lists = soup.select('body')
    #             address_pat = '卡号归属地[\d\D]*?</tr>' 
    #             pat="<.*?>"
    #             position_data = re.search(address_pat,str(page_lists))
    #             position_data = re.sub(pat, "",position_data.group()).replace(" -->","").replace("卡号归属地","").replace("\n","")
    #             print(position_data)
    #             models.Label_msg_bj.objects.filter(id=i.id).update(phone_address=position_data)