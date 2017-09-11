# -*- coding: utf-8 -*-
import urllib
import json

import scrapy
from fake_useragent import UserAgent
from company import settings


class QixinSpider(scrapy.Spider):
    name = 'qixin'
    allowed_domains = ['www.qixin.com']

    def __init__(self, **kwargs):
        self.search_key = kwargs.pop('search', None)
        self.cookie = kwargs.pop('cookie', None)
        self.user_agent = UserAgent().random

        super(QixinSpider, self).__init__(**kwargs)

    def start_requests(self):
        if self.search_key is None:
            return

        key_urlencode = urllib.quote(self.search_key.encode('u8'))
        search_url = 'http://www.qixin.com/search?key={}&page=1'.format(key_urlencode)
        cookie = {}

        headers = {
            'User-Agent': self.user_agent,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://www.qixin.com/',
        }

        yield scrapy.Request(search_url, headers=headers)

    def parse(self, response):
        print 'h1:', response.request.headers
        print 'body:', response.body

        data = json.loads(response.body)
        print data
        corp_url = 'http://www.qixin.com/company/{corp_eid}'
        headers = {
            'User-Agent': self.user_agent,
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://www.qixin.com/search?key={}&page=1'
        }

        if data:
            corp_data = data[0]
            corp_eid = corp_data['eid']
            corp_name = corp_data['name']
            category = corp_data['category']
            headers['Referer'] = headers['Referer'].format(urllib.quote(corp_name))
            meta = {'corp_eid': corp_eid, 'corp_name': corp_name, 'category': category}

            # yield scrapy.Request(
            #     corp_url.format(corp_eid),
            #     headers=headers, callback=self.parse_corp, meta=meta
            # )
    #
    # def parse_corp(self, response):
    #     pass


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(QixinSpider, search=u'新浪')
    crawler.start()
