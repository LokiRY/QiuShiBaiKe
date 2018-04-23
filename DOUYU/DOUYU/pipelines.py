# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
from DOUYU.settings import IMAGES_STORE as images_store
from scrapy.pipelines.images import ImagesPipeline
from DOUYU.items import DouyuItem

class DouyuPipeline(ImagesPipeline):

    # def open_spider(self,spider):
    #     self.f = open("data.txt","w")
    #
    # def process_item(self, item, spider):
    #     content = item["img_link"] + '\n'
    #     self.f.write(content)
    #     return item

    def get_media_requests(self,item,info):
        link = item["img_link"]
        print(link)
        yield scrapy.Request(link)

    def item_completed(self,results,item,info):
        img_path = [x["path"] for ok,x in results if ok]
        os.rename(images_store + img_path[0],images_store + "full/" + item['nick_name'] + '.jpg' )
        return item