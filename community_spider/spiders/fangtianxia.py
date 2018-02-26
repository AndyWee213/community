# -*- coding: utf-8 -*-
import scrapy
import uuid
from community_spider.items import CommunitySpiderItem


class FangtianxiaSpider(scrapy.Spider):
    name = 'fangtianxia'
    allowed_domains = ['fang.com']
    start_urls = 'http://esf.hz.fang.com/housing/'

    def start_requests(self):
        return [scrapy.Request(self.start_urls)]

    def parse(self, response):
        print(response.request.headers)
        find_commu_num = int(response.xpath('//b[@class="findplotNum"]/text()').extract()[0])
        if find_commu_num > 2000:
            counties = response.xpath('//div[@class="qxName"]/a')
            for county in counties:
                county_name = county.xpath('./text()').extract()[0]
                if county_name and county_name != '不限':
                    yield scrapy.Request('http://esf.hz.fang.com' + county.xpath('./@href').extract()[0].strip())

        communities = response.xpath('//div[@class="houseList"]/div[@class="list rel"]')
        for community in communities:
            community_url = community.xpath('./dl/dd/p[1]/a/@href').extract()[0]
            community_title = community.xpath('./dl/dd/p[1]/a/text()').extract()[0]
            community_type = community.xpath('./dl/dd/p[1]/span[1]/text()').extract()[0]
            community_segment = community.xpath('./dl/dd/p[2]/a[1]/text()').extract()[0] + \
                                community.xpath('./dl/dd/p[2]/a[2]/text()').extract()[0]
            community_county = community.xpath('./dl/dd/p[2]/a[1]/text()').extract()[0]
            item = CommunitySpiderItem()
            item['id'] = uuid.uuid1()
            item['url'] = community_url
            item['title'] = community_title
            item['type'] = community_type
            item['segment'] = community_segment
            item['province'] = '浙江'
            item['city'] = '杭州'
            item['county'] = community_county
            yield item

        next_page_url = response.xpath('//a[@id="PageControl1_hlk_next"]/@href').extract()
        if next_page_url:
            yield scrapy.Request('http://esf.hz.fang.com'+next_page_url[0].strip())
