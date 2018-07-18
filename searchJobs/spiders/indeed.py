# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request


class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    allowed_domains = ['indeed.co.in']
    search_url = "https://www.indeed.co.in/jobs?q=django&l=pune"
    start_urls = ['http://indeed.co.in/']

    def parse(self, response):
        yield Request(url=self.search_url, cookies=cookies, callback=self.parse_item)

    def parse_item(self, response):
        import pdb; pdb.set_trace()
        pass
