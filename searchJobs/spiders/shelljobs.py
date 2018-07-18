# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from scrapy.http import Request


class ShelljobsSpider(scrapy.Spider):
    name = 'shelljobs'
    allowed_domains = ['shell.com']
    search_url = "https://www.shell.com/careers/experienced-professionals/_jcr_content/par/jobsearch.kenexa?7528=&filter1=&filter2=United Kingdom&siteId=5798&siteLocaleId=&7529=&48372=&49283=United Kingdom&57800=&7530=&48337=&page=1&_charset_=utf-8"  # noqa
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
        jobs = results_set['jobs']['job']

        for job in jobs:
            item = {
                "title": job.get('question')[0].get('content'),
                "jobdetail_link": job.get('jobdetaillink'),
                "job_description": job.get('jobdescription'),
                "skill_group": job.get('question')[1].get('content'),
                "location": job.get('question')[2].get('content'),
                "last_updated": job.get('lastupdated'),
                "hot_job": job.get('hotjob'),
            }
            yield item
