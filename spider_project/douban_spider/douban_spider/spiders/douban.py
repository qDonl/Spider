# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban_spider.items import DoubanSpiderItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    rules = (
        Rule(LinkExtractor(allow=r'.*?start=\d+.*'), follow=True),
        Rule(LinkExtractor(allow=r".*/subject/\d+.*"), callback='parse_item', follow=False)
    )

    def parse_item(self, response):
        rank_No = response.xpath("//span[@class='top250-no']/text()").get()
        rank = rank_No.split('.')[1]
        title = response.xpath("//h1/span/text()").get()
        year_text = response.xpath("//span[@class='year']/text()").get()
        year = re.sub(r'\(|\)', '', year_text)

        infos = response.xpath("//div[@id='info']/span")
        director = infos[0].xpath(".//a/text()").get()
        screenwriter_list = infos[1].xpath(".//a/text()").getall()
        screenwriter = ','.join(screenwriter_list)
        stars_list = infos[2].xpath(".//a/text()").getall()
        stars = ','.join(stars_list)
        types_list = response.xpath("//div[@id='info']/span[@property='v:genre']/text()").getall()
        types = ','.join(types_list)
        runtime = response.xpath("//span[@property='v:runtime']/text()").get()
        IMDb = response.xpath("//div[@id='info']/a[@rel='nofollow']/@href").get()
        origin_url = response.url
        pub_time = response.xpath("//span[@property='v:initialReleaseDate']/@content").get()

        others = response.xpath("//div[@id='info']/text()").getall()
        country, language, *_ = [x for x in list(map(lambda x: re.sub(r"\s|/", '', x), others)) if x]

        item = DoubanSpiderItem(rank=rank,
                                title=title,
                                year=year,
                                director=director,
                                screenwriter=screenwriter,
                                stars=stars,
                                types=types,
                                runtime=runtime,
                                IMDb=IMDb,
                                origin_url=origin_url,
                                pub_time=pub_time,
                                )
        yield item

