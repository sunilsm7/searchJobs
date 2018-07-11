# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import FormRequest, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ShellJobItem

class ShelljobsSpider(scrapy.Spider):
    name = 'shelljobs'
    allowed_domains = ['shell.com']
    search_url = "https://www.shell.com/careers/experienced-professionals/_jcr_content/par/jobsearch.kenexa?7528=&filter1=&filter2=United Kingdom&siteId=5798&siteLocaleId=&7529=&48372=&49283=United Kingdom&57800=&7530=&48337=&page=1&_charset_=utf-8"
    start_urls = [search_url]

    def parse(self, response):
        cookies = {
            "_ga": "GA1.2.923543165.1531227449",
            "AAM": "5902350",
            "aam_uuid": "39308232951443784360885314303723190646",
        }
        yield Request(url=self.search_url, cookies=cookies, callback=self.parse_item)
        
    def parse_item(self, response):
        data = json.loads(response._body)
        results_set = data['envelope']['unit']['packet']['payload']['resultset']
        jobs=results_set['jobs']['job']
        
        for job in jobs:
            item_details_url = job.get('jobdetaillink')
            print(item_details_url)
            request = scrapy.Request(item_details_url, dont_filter=True, callback=self.parse_details)
            yield request
 

    def parse_details(self, response):
        # import pdb; pdb.set_trace()
        item = ShellJobItem()
        # job = response.get('job', None)
        item['title'] = response.css("h1::text").extract_first().strip()
        item['jobdetail_link'] = response.css('jobdetaillink')
        item['job_description'] = response.css(".jobdescriptionInJobDetails > strong::text").extract_first().strip()
        item['skill_group'] = response.css('question')[1].get('content')
        item['location'] = response.css('question')[2].get('content')
        item['last_updated'] = response.css('lastupdated')
        item['hot_job'] = response.css('hotjob')


