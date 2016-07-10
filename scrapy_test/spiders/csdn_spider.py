# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from ..items import CsdnSpiderItem
from scrapy.http import Request

class CsdnSpider(BaseSpider):
    name = 'csdn_spider'
    start_urls = [
        "http://blog.csdn.net/index.html?&page=1"
        # "http://blog.csdn.net/newest.html?&page=1"
      ]

    def parse_1(self, response):
        selector = Selector(response)

        item = CsdnSpiderItem()
        title = selector.xpath('//head/title/text()').extract()
        read_count = selector.xpath('//div[@class="article_r"]/span[2]/text()').re(r'(\d+)')
        comment_count = selector.xpath('//div[@class="article_r"]/span[3]/text()').re(r'(\d+)')

        if len(title) > 0:
            item['title'] = title[0].encode('utf-8')
        if read_count:
            item['read_count'] = read_count[0]
        if comment_count:
            item['comment_count'] = comment_count[0]
        item['url'] = response.url
        yield item

        urls = selector.xpath('//h1/span/a/@href').extract()
        for url in urls:
            url = 'http://blog.csdn.net' + url
            yield Request(url=url, callback=self.parse)

        next_url = 'http://blog.csdn.net' + selector.xpath('//div[@class="pagelist"]/a/@href').extract()[-2]
        yield Request(url=next_url, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        articles = selector.xpath('//div[@class="blog_list"]')
        article_list = articles[0]

        item = CsdnSpiderItem()
        if article_list:
            url_list = article_list.xpath('//h1/a[last()]/@href').extract()
            title_list = article_list.xpath('//h1/a[last()]/text()').extract()
            read_count_list = article_list.xpath('//div[@class="about_info"]/span[2]/a[2]/text()').re(r'(\d+)')
            comment_count_list = article_list.xpath('//div[@class="about_info"]/span[2]/a[3]/text()').re(r'(\d+)')

            print len(url_list)
            print len(title_list)
            print len(read_count_list)
            print len(comment_count_list)

            for i in range(0, len(articles)):
                item['title'] = title_list[i]
                item['url'] = url_list[i]
                item['read_count'] = read_count_list[i]
                item['comment_count'] = comment_count_list[i]
                yield item

        next_url = 'http://blog.csdn.net' + selector.xpath('//div[@class="page_nav"]/a/@href').extract()[-2]
        yield Request(url=next_url, callback=self.parse)