# -*- coding: utf-8 -*-
import re
import urllib
import json
from random import choice
from copy import deepcopy
from datetime import datetime

import scrapy
from pymongo import MongoClient
from company import defaults


class QichachaSpider(scrapy.Spider):
    name = 'qichacha'
    allowed_domains = ['www.qichacha.com']
    custom_settings = {'DOWNLOAD_DELAY': 1.5}

    def __init__(self, **kwargs):
        self._typ = 'qichacha'
        self._cookie = kwargs.pop('cookie', None)
        self.search_key = kwargs.pop('search', None)
        self.user_agent = choice(defaults.USER_AGENT)
        self.invests = []

        self._headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': self.user_agent,
            'Host': 'www.qichacha.com',
            'Upgrade-Insecure-Requests': '1',
        }

        self.client = MongoClient()
        self.db = self.client.crawl.corp_info
        self.schedule_db = self.client.crawl.corp_schedule

        super(QichachaSpider, self).__init__(**kwargs)

    @property
    def cookies(self):
        cookies = self._cookie or self.settings['QICHACHA_COOKIE']
        return dict([ck.split('=', 1) for ck in cookies.split(';')])

    @staticmethod
    def get_eid(url):
        if not url:
            return None

        eid_regex = re.compile(r'/firm_(.*?)\.html')
        eid_m = eid_regex.search(url)

        return eid_m.group(1) if eid_m else None

    def start_requests(self):
        if self.search_key is None:
            return

        headers = deepcopy(self._headers)
        headers['Referer'] = 'http://www.qichacha.com/'

        if isinstance(self.search_key, unicode):
            word = self.search_key.encode('u8')
        else:
            word = self.search_key

        key_urlencode = '%' in word and urllib.quote(word) or word
        search_url = 'http://www.qichacha.com/search?key={}'.format(key_urlencode)

        yield scrapy.Request(search_url, headers=headers, cookies=self.cookies)

    def parse(self, response):
        target_css = 'table.m_srchList > tbody > tr:first-child > td:nth-child(2) > a::attr(href)'
        href = response.css(target_css).extract_first()
        eid = self.get_eid(href)

        if eid is None:
            return

        url = response.urljoin(href)
        headers = deepcopy(self._headers)
        headers['Referer'] = response.url

        yield scrapy.Request(
            url, meta={'result': {'eid': eid}},
            headers=headers, cookies=self.cookies, callback=self.parse_corp
        )

        self.schedule_db.insert({
            'typ': self._typ, 'upt': datetime.now(), 'word': self.search_key
        })

    def parse_corp(self, response):
        industry = ''

        for tr_sel in response.css('table.m_changeList tr'):
            is_break = False
            text_list = tr_sel.css('td::text').extract()

            for index, text in enumerate(text_list):
                if u'所属行业' in text:
                    is_break = True
                    industry = text_list[index + 1]
                    break

            if is_break:
                break

        name = (response.css('div.company-top-name::text').extract_first() or '').strip()
        is_site = bool(response.css('a.company-top-url::attr(href)').extract_first())
        is_branch = bool(response.css('section#Subcom div.panel-heading span.badge').extract_first())

        if not name:
            return

        name_urlencode = urllib.quote(name.encode('u8'))
        response.meta['result'].update({
            'name': name, 'is_branch': is_branch, 'is_site': is_site, 'ind': industry
        })
        response.meta['name_urlencode'] = name_urlencode

        headers = deepcopy(self._headers)
        headers['Referer'] = response.url
        headers.pop('Upgrade-Insecure-Requests')
        headers['X-Requested-With'] = 'XMLHttpRequest'

        risk_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=susong'.format(
            response.meta['result']['eid'], name_urlencode
        )

        yield scrapy.Request(
            risk_url, meta=response.meta,
            headers=headers, cookies=self.cookies, callback=self.parse_risk_info
        )

    def parse_risk_info(self, response):
        # 失信信息
        is_credit = bool(response.css('section#shixinlist div.panel-heading span.badge').extract_first())
        operation_url = 'http://www.qichacha.com/company_getinfos?unique=&companyname=&tab=run'.format(
            response.meta['result']['eid'], response.meta['name_urlencode']
        )

        headers = deepcopy(self._headers)
        headers.pop('Upgrade-Insecure-Requests')
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Referer'] = ''.join(response.request.headers['Referer'])

        response.meta['result']['is_credit'] = is_credit

        yield scrapy.Request(
            operation_url, meta=response.meta,
            headers=headers, cookies=self.cookies, callback=self.parse_operation
        )

    def parse_operation(self, response):
        is_chattel_mortgage = False

        # 股权出质
        is_stock_pledge = bool(response.css('section#pledgeList div.panel-heading span.badge').extract_first())

        # 投招标
        is_bid = bool(response.css('section#tenderlist div.panel-heading span.badge').extract_first())

        # 动产抵押
        for text in response.css('div.panel-body a.m-r-sm.m-t-sm::text').extract():
            if u'动产抵押' in text and re.compile(r'\d+').search(text):
                is_chattel_mortgage = True
                break

        response.meta['result'].update({
            'is_bid': is_bid, 'is_stock_pledge': is_stock_pledge, 'is_chattel_mortgage': is_chattel_mortgage
        })

        investment_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=touzi'.format(
            response.meta['result']['eid'], response.meta['name_urlencode']
        )
        headers = deepcopy(self._headers)
        headers.pop('Upgrade-Insecure-Requests')
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Referer'] = ''.join(response.request.headers['Referer'])

        yield scrapy.Request(
            investment_url, meta=response.meta,
            headers=headers, cookies=self.cookies, callback=self.parse_investment
        )

    def parse_investment(self, response):
        is_last_page = response.meta.get('is_last_page', False)
        is_investment = response.meta.get('is_investment', False)

        for index, sel in enumerate(response.css('table.m_changeList tr')):
            if index == 0:
                continue

            name = (sel.css('tr td:first-child a::text').extract_first() or '').strip()
            capital = (sel.css('tr td:nth-child(3)::text').extract_first() or '0.00').strip()
            _time = (sel.css('tr td:nth-child(5)::text').extract_first() or '').strip()

            self.invests.append({'name': name, 'capital': capital, 'time': _time})

        if is_last_page:
            response.meta['result']['invests'] = self.invests
            self.insert_db(response.meta['result'])
            return

        headers = deepcopy(self._headers)
        headers.pop('Upgrade-Insecure-Requests')
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Referer'] = ''.join(response.request.headers['Referer'])

        eid = response.meta['result']['eid']
        name_urlencode = response.meta['name_urlencode']
        other_invest_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&p={}&tab=touzi&box=touzi'

        if not is_investment:
            investment_count = int(response.css('div.panel-heading span.badge::text').extract_first() or '0') - 20

            if investment_count <= 0:
                return

            pages = investment_count / 20 + bool(investment_count % 20)

            for page in range(1, pages + 1):
                meta = deepcopy(response.meta)
                meta['is_investment'] = True
                meta['is_last_page'] = page == pages

                yield scrapy.Request(
                    other_invest_url.format(eid, name_urlencode, page + 1),
                    meta=meta, headers=headers, cookies=self.cookies, callback=self.parse_investment
                )

    def insert_db(self, document):
        document['typ'] = self._typ
        document['search'] = self.search_key
        document['upt'] = datetime.now()
        document['is_invest_abroad'] = bool(self.invests)

        query = {'eid': document['eid'], 'typ': self._typ, 'search': self.search_key}
        self.db.update(query, document, upsert=True)

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
    crawler.crawl(QichachaSpider, search='阿里巴巴')
    crawler.start()



