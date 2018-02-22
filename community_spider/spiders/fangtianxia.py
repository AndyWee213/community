# -*- coding: utf-8 -*-
import scrapy
import re

from community_spider.items import CommunitySpiderItem


class FangtianxiaSpider(scrapy.Spider):
    name = 'fangtianxia'
    allowed_domains = ['fang.com']
    start_urls = 'http://esf.hz.fang.com/housing/__0_0_0_0_1_0_0_0/'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "upgrade-insecure-requests": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
    }

    def start_requests(self):
        return [scrapy.Request(self.start_urls, headers=self.headers)]

    def parse(self, response):
        communities = response.xpath('//div[@class="houseList"]/div[@class="list rel"]')
        for community in communities:
            community_url = community.xpath('./dl/dd/p[1]/a/@href').extract()[0]
            community_id = re.findall(r"http://(.+?)\..*", community_url)
            community_title = community.xpath('./dl/dd/p[1]/a/text()').extract()[0]
            community_type = community.xpath('./dl/dd/p[1]/span[1]/text()').extract()[0]
            community_segment = community.xpath('./dl/dd/p[2]/a[1]/text()').extract()[0] + \
                                community.xpath('./dl/dd/p[2]/a[2]/text()').extract()[0]
            item = CommunitySpiderItem()
            item['id'] = community_id
            item['url'] = community_url
            item['title'] = community_title
            item['type'] = community_type
            item['segment'] = community_segment
            yield item

        next_page_url = response.xpath('//a[@id="PageControl1_hlk_next"]/@href').extract()
        if next_page_url:
            yield scrapy.Request('http://esf.hz.fang.com'+next_page_url[0].strip(), headers=self.headers)
