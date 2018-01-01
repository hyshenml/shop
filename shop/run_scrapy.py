# -*- coding: utf-8 -*-
from scrapy import cmdline
for i in range(50):
    cmdline.execute("scrapy crawl dpShop".split())
