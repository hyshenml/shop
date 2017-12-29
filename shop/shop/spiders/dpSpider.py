# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from shop.targetManager import targetManager
from scrapy import Request
from shop.items import urlItem
from scrapy.selector import Selector
from time import time
import re
from shop.utils import get_domain

class dpSpider(Spider):
    name='dpShop'

    def start_requests(self):
      targets=targetManager.prepare_targets()
      for target in targets:
        callback=self._router_(target)
        yield Request(url=target.url, callback=callback)
        target.record_update_time()

    def _router_(self,target):
        if target.target_type=='root':
            callback=self.parse_city_list
        elif target.target_type=='city':
            callback = self.parse_city_food
        elif target.target_type=='business_div':
            callback = self.parse_busi_div
        elif target.target_type=='div_category':
            callback = self.parse_div_category
        else:
            callback=self.parse
        return callback

    def parse_city_list(self,response):
        sel=Selector(text=response.body).xpath('//a/strong')
        url_item=urlItem()
        for s in sel:
            try:
                url=s.xpath('../@href').extract()
                url=url[0][2:]
                url_item['url']=url
                url_item['target_type']='city'
                url_item['last_parse_time']=0
                yield url_item
            except Exception,e:
                print e

    def parse_city_food(self,response):
        domain=get_domain(response.url)
        p=re.compile('^\/(.+)\/r')
        try:
            business_div=Selector(text=response.body).xpath("//div[@class='nc_item list_business']")[0]
            city_url=business_div.xpath('//ul[@class="nc_list"]/li/a/@href')[0].extract()
            city_url=re.findall(p,city_url)[0]
            sel=business_div.xpath("//dl[@class='list']/dd/ul/li/a")
            for s in sel:
                url_item = urlItem()
                url=domain+city_url+'/'+s.xpath('@data-value')[0].extract()
                url_item['url'] = url
                url_item['target_type'] = 'business_div'
                url_item['last_parse_time'] = 0
                yield url_item
        except Exception,e:
            print e

    def parse_busi_div(self,response):
        sel=Selector(text=response.body).xpath('//div[@id="classfy" and @class="nc-items"]/a[@href]/@href').extract()
        for s in sel:
            url=s
            url_item = urlItem()
            url_item['url'] = url
            url_item['target_type'] = 'div_category'
            url_item['last_parse_time'] = 0
            yield url_item

    def parse_div_category(self,response):
        text = response.body

        next_page = Selector(text=text).xpath(u'//a[text()="下一页" and @class="next"]/@href').extract()

        if(len(next_page)>0):
            url_item = urlItem()
            url_item['url'] = next_page[0]
            url_item['target_type'] = 'div_category'
            url_item['last_parse_time'] = 0
            print url_item
        shop_list = Selector(text=text).xpath(u'//div[@id="shop-all-list"]/ul/li')
        for shop in shop_list:
            pass

    def parse(self,response):
        print '############'



