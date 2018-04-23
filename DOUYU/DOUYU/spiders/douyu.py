# -*- coding: utf-8 -*-
import scrapy
import json
from DOUYU.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyucdn.cn']
    
    base_url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
    offset = 0
    
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        data_list = json.loads(response.body)['data']
        for data in data_list:
            item = DouyuItem()
            item['nick_name'] = data["nickname"]
            item['img_link'] = data["vertical_src"]

            yield item

        if len(json.loads(response.body)['data']) != 0:
            # print(json.loads(response.body)['data'])
            # print("*" * 8)
            self.offset += 20
            # print(self.offset)
            url = self.base_url + str(self.offset)
            yield scrapy.Request(url,callback = self.parse)
