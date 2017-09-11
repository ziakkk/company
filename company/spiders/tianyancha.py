# -*- coding: utf-8 -*-

import re
import urllib
import time
from copy import deepcopy
from datetime import datetime

import scrapy
from pymongo import MongoClient
from fake_useragent import UserAgent


class TianyanchaSpider(scrapy.Spider):
    name = 'tianyancha'
    allowed_domains = ['www.tianyancha.com']

    def __init__(self, **kwargs):
        self.search_key = kwargs.pop('search', None)
        self.cookie = kwargs.pop('cookie', None)
        self.user_agent = UserAgent().random

        self.log('Search Word: {}, type: {}'.format(self.search_key, type(self.search_key)), 20)

        self._headers = {
            'User-Agent': self.user_agent,
            'Host': 'www.tianyancha.com',
            'Upgrade-Insecure-Requests': '1'
        }

        self.client = MongoClient()
        self.db = self.client.crawl.corp_info
        self.schedule_db = self.client.crawl.corp_schedule

        super(TianyanchaSpider, self).__init__(**kwargs)

    @property
    def cookies(self):
        return dict([ck.split('=', 1) for ck in self.settings['TIANYANCHA_COOKIE'].split(';')])

    def start_requests(self):
        key_urlencode = urllib.quote(self.search_key.decode('u8'))
        search_url = 'https://www.tianyancha.com/search?key={}&checkFrom=searchBox'.format(key_urlencode)

        headers = deepcopy(self._headers)
        headers['Referer'] = 'https://www.tianyancha.com/'
        yield scrapy.Request(
            search_url,
            meta={'search_key': self.search_key},
            headers=headers, cookies=self.cookies
        )

    def parse(self, response):
        # print response.request.headers
        # print response.request.cookies

        headers = deepcopy(self._headers)
        headers['Referer'] = response.url

        corp_css = 'div.search_result_single a.query_name.search-new-color.sv-search-company{}'
        corp_url = response.css(corp_css.format('::attr(href)')).extract_first()

        if corp_url is None:
            return

        yield scrapy.Request(
            corp_url,
            meta=response.meta,
            headers=headers, cookies=self.cookies, callback=self.parse_corp
        )

    def parse_corp(self, response):
        eid_regex = re.compile(r'company/(\d+)')
        eid_m = eid_regex.search(response.url)
        eid = eid_m.group(1) if eid_m else None

        document = {'upt': datetime.now()}
        query = {'eid': eid, 'typ': 'tianyancha', 'search': response.meta['search_key']}

        industry = ''
        partition_regex = re.compile(ur'[:：]', re.S)
        blank_regex = re.compile(r'\s', re.S)
        corp_name = response.css('div#company_web_top span.f18.in-block.vertival-middle::text').extract_first() or ''
        is_site = bool(response.css('div#company_web_top a[nofollow].c9::attr(href)').extract_first())
        # print 'corp_name:', corp_name, 'site:', is_site

        # 行业
        for sel in response.css('td.basic-td'):
            text = ''.join(sel.css('td *::text').extract())
            belong = partition_regex.split(text)

            if len(belong) == 2 and belong[0] == u'行业':
                industry = belong[1].strip().replace(' ', '')
                break

        document.update({'corp_name': corp_name, 'is_site': is_site, 'ind': industry})

        # 是否有分支机构、失信信息、股权出质、动产抵押、对外投资、招投标信息
        selector = 'div.company-main div.nav_item_Box div.nav-item-p.text-left div.position-rel'
        for is_sel in response.css(selector):
            key = None
            _text = blank_regex.sub('', ''.join(is_sel.css('div::text').extract()))
            _count = blank_regex.sub('', ''.join(is_sel.css('span::text').extract()))
            # print _text, type(_text), _count, type(_count)

            if u'分支机构' == _text:
                key = 'is_branch'

            if u'失信信息' == _text:
                key = 'is_credit'

            if u'股权出质' == _text:
                key = 'is_stock_pledge'

            if u'动产抵押' == _text:
                key = 'is_chattel_mortgage'

            if u'对外投资' == _text:
                key = 'is_invest_abroad'

            if u'招投标' == _text:
                key = 'is_bid'

            key and document.update(**{key: bool(int(_count or '0'))})

        # 对外投资企业的成立时长、注册资本
        investment_pages = self.get_corp_pages(response)
        document['invests'] = self.parse_invest_corps(response)
        document.update(query)
        # print 'investment_pages:', investment_pages

        # if not investment_pages:
        #     self.db.update(query, document, upsert=True)
        #     return

        self.insert_db(document)

        # headers = deepcopy(self._headers)
        # headers.pop('Upgrade-Insecure-Requests')
        # headers.update({'Referer': response.url, 'X-Requested-With': 'XMLHttpRequest', 'Accept': '*/*'})
        # invest_url = 'https://www.tianyancha.com/pagination/invest.xhtml?ps={}&pn=2&id={}&_={}'.format(
        #     (investment_pages - 1) * 20, eid, long(time.time() * 1000)
        # )
        #
        # yield scrapy.Request(
        #     invest_url, meta={'tyc_doc': document},
        #     headers=headers, cookies=self.cookies, callback=self.parse_other_investment_corps
        # )

    def parse_invest_corps(self, response):
        invests = []

        for invest_sel in response.css('div.out-investment-container table tbody tr'):
            name = invest_sel.css('tr td:first-child span.text-click-color::text').extract_first() or ''
            capital = invest_sel.css('tr td:nth-child(3) span::text').extract_first() or ''
            _time = invest_sel.css('tr td:nth-child(6) span::text').extract_first() or ''

            invests.append({'name': name, 'capital': capital, 'time': _time})

        return invests

    def get_corp_pages(self, response):
        total = response.css('div#_container_invest div.company_pager div.total::text').extract_first() or '0'
        return int(total)

    def parse_other_investment_corps(self, response):
        print response.body

        other_invest_corps = self.parse_invest_corps(response)
        document = response.meta['tyc_doc']
        document['invests'].extend(other_invest_corps)

        query = {'eid': document['eid'], 'typ': 'tianyancha', 'search': document['search']}
        self.db.update(query, document, upsert=True)

    def insert_db(self, document):
        typ = document['typ']
        search = document['search']
        query = {'eid': document['eid'], 'typ': typ, 'search': search}
        self.db.update(query, document, upsert=True)

        self.schedule_db.insert({
            'typ': typ, 'upt': datetime.now()
        })


    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)

        spider.client.close()


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(TianyanchaSpider, search=u'百度')
    crawler.start()

