# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from shop.targetManager import targetManager,target
from scrapy import Request
from shop.items import urlItem,ShopItem
from scrapy.selector import Selector
from time import time
import re
from shop.utils import get_domain,list_get_safe

class dpSpider(Spider):
    name='dpShop'

    def start_requests(self):
      targets=targetManager.prepare_targets()
      for target in targets:
        callback=self._router_(target)
        url=target.url

        yield Request(url=target.url, callback=callback)
        #target.record_update_time()

    def _record_update_(self,url):
        t=target()
        print url,' has finished'
        t.setUrl(url)
        t.record_update_time()



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
                url_item['url']="http://"+url
                url_item['target_type']='city'
                url_item['last_parse_time']=0
                yield url_item
            except Exception,e:
                print e
        self._record_update_(response.url)


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
            print 'err',e
        self._record_update_(response.url)


    def parse_busi_div(self,response):
        sel=Selector(text=response.body).xpath('//div[@id="classfy" and @class="nc-items"]/a[@href]/@href').extract()
        for s in sel:
            url=s
            url_item = urlItem()
            url_item['url'] = url
            url_item['target_type'] = 'div_category'
            url_item['last_parse_time'] = 0
            yield url_item
        self._record_update_(response.url)

    def parse_div_category(self,response):
        text = response.body
        next_page = Selector(text=text).xpath(u'//a[text()="下一页" and @class="next"]/@href').extract()

        if(len(next_page)>0):
            t=target()
            t.setType('div_category')
            t.setUrl(next_page[0])
            callback=self._router_(t)
            yield Request(url=t.url, callback=callback)

        city=list_get_safe(Selector(text=text).xpath('//a[@class="city J-city"]/span/text()').extract())
        shop_list = Selector(text=text).xpath(u'//div[@id="shop-all-list"]/ul/li')
        for shop in shop_list:
            shop_item=ShopItem()
            href=shop.xpath('./div/div[@class="tit"]/a/@href').extract()
            p=re.compile('\/(\d+)$')
            href=list_get_safe(href)
            shop_id=list_get_safe(re.findall(p,href))
            name=shop.xpath('./div/div[@class="tit"]/a/h4/text()').extract()
            name=list_get_safe(name)
            comment=shop.xpath('./div/div[@class="comment"]/span/@title').extract()
            comment=list_get_safe(comment)
            tag=shop.xpath('./div/div[@class="tag-addr"]/a/span[@class="tag"]/text()').extract()
            type=list_get_safe(tag)
            address=shop.xpath('./div/div[@class="tag-addr"]/span[@class="addr"]/text()').extract()
            address=list_get_safe(address)
            area=list_get_safe(tag,1)
            comment_score=shop.xpath('./div/span[@class="comment-list"]/span/b/text()').extract()
            taste=list_get_safe(comment_score,0,0)
            environment=list_get_safe(comment_score,1,0)
            service=list_get_safe(comment_score,2,0)
            dishs=shop.xpath('./div/div[@class="recommend"]/a/text()').extract()
            if len(dishs)>1:
                recommended_dish=reduce(lambda x,y:x+','+y,dishs)
            else:
                recommended_dish=list_get_safe(dishs,0,'')

            shop_item['city']=city.encode('utf-8')
            shop_item['shop_id']=shop_id.encode('utf-8')
            shop_item['name']=name.encode('utf-8')
            shop_item['type']=type.encode('utf-8')
            shop_item['comment']=comment.encode('utf-8')
            shop_item['address']=address.encode('utf-8')
            shop_item['area']=area.encode('utf-8')
            shop_item['taste']=float(taste)
            shop_item['environment']=float(environment)
            shop_item['service']=float(service)
            shop_item['recommended_dish']=recommended_dish.encode('utf-8')
            yield shop_item
        self._record_update_(response.url)



    def parse(self,response):
        print '############'



