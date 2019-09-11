# -*- coding: utf-8 -*-
import scrapy
from Xiaohua.items import XiaohuaItem

class JokeSpider(scrapy.Spider):
    name = 'joke'
    allowed_domains = ['xiaohua.zol.com.cn']
    start_urls = ['http://xiaohua.zol.com.cn/']
    baseurl="http://xiaohua.zol.com.cn"
    def parse(self, response):
        fenleiurls=response.xpath('//ul[@class="news-list classification-nav clearfix"]/li/a/@href').extract()
        for fenleiurl in fenleiurls:
            yield scrapy.Request(self.baseurl+fenleiurl,callback=self.parse_fenlei)
    def parse_fenlei(self,response):
        fenleiinfo=response.xpath('//ul[@class="article-list"]/li//a[@class="all-read"]/@href').extract()
        for singleinfo in fenleiinfo:
            yield scrapy.Request(self.baseurl+singleinfo,callback=self.parse_info)
        nexturl=response.xpath('//a[@class="page-next"]/@href').extract()
        if len(nexturl)!=0:
            yield scrapy.Request(self.baseurl+nexturl[0],callback=self.parse_fenlei)
    def parse_info(self,response):
        item=XiaohuaItem()
        item['title']=response.xpath('//h1[@class="article-title"]/text()').extract_first()
        item['contents']=response.xpath('//div[@class="article-text"]').extract_first()
        item['fenlei']=response.xpath('//div[@class="wrapper location clearfix"]/a[4]/text()').extract_first()
        item['laiyuan']=response.xpath('//div[@class="article-source"]/span[2]/text()').extract_first()
        #print(item['contents'])
        yield item
        #yield item