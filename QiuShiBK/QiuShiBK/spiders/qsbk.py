# -*- coding: utf-8 -*-
import scrapy
from QiuShiBK.items import QiushibkItem

class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qishibaike.com']
    base_url = "https://www.qiushibaike.com"
    first_url = "/8hr/page/1/"
    start_urls = [base_url + first_url]

    url_pool = [] #链接总池
    crawled_pool = [] #已爬取链接池
    crawl_pool = []  # 待爬取链接池
    crawled_pool.append(first_url)
    url_pool.append(first_url)
    # 待爬取链接池 已爬取连接池 本次爬取链接 链接总池
    def parse(self, response):
        # #将第一个爬虫链接放入已爬取链接池
        main_url = response.xpath("//div[@id='menu']/a/@href").extract()
        page_url = response.xpath("//ul[@class='pagination']/li/a/@href").extract()
        for url in main_url:
            if url not in self.url_pool:
                self.url_pool.append(url)
            if url not in self.crawled_pool:
                if url not in self.crawl_pool:
                    self.crawl_pool.append(url)
        #获取页面上的小链接，并放入链接总池，如果不在已爬取链接池，则放入待爬取链接池；如果不在链接总池则放入链接总池
        for url in page_url:
            if url not in self.url_pool:
                self.url_pool.append(url)
            if url not in self.crawled_pool:
                if url not in self.crawl_pool:
                    self.crawl_pool.append(url)
        node_list = response.xpath("//div[@id='content-left']/div")
        for node in node_list:
            item = QiushibkItem()
            if len(node.xpath("./div[@class='author clearfix']/a")) != 0:
                item['author_name'] = ''.join(str(node.xpath("./div[@class='author clearfix']/a/h2/text()").extract()[0]).split('\n'))
                item['author_link'] = node.xpath("./div[@class='author clearfix']/a/@href").extract()[0]
            else:
                item['author_name'] = '匿名用户'
                item['author_link'] = ''
            item['content'] = ''.join(str(node.xpath("./a[@class='contentHerf']/div[@class='content']/span/text()").extract()[0]).split('\n'))
            yield item

        if self.crawl_pool:
            new_url = self.crawl_pool.pop()
            self.crawled_pool.append(new_url)
            yield scrapy.Request(self.base_url + new_url,callback = self.parse,dont_filter=True)

