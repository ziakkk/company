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
    custom_settings = {'DOWNLOAD_DELAY': 1.8}

    def __init__(self, **kwargs):
        self._typ = 'qichacha'
        self._cookies = kwargs.pop('cookie', None)
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
        doc_dict = {}
        cookies_dict = deepcopy(self.settings['QICHACHA_COOKIE'])
        parse_cookie_str = (lambda _c: dict([ck.split('=', 1) for ck in _c.split(';')]))

        if self._cookies is None:
            now = datetime.now()
            cookie_db = self.client.crawl.corp_cookies
            cursor = [d for d in cookie_db.find().sort([('crt', -1)]).limit(1000)]

            for doc in cursor:
                doc_dict.setdefault(doc['phone'], []).append(doc)

            sorted_dict = {k: sorted(v, key=lambda _d: _d['crt']) for k, v in doc_dict.iteritems()}
            diff_keys = set(cookies_dict) - set(sorted_dict)

            if not cursor:
                pk = choice(cookies_dict.keys())  # 表为空
            else:
                if diff_keys:
                    pk = choice(list(diff_keys))
                else:
                    # 匹配间隔时间不小于30s的记录
                    used_cookies = [(k, v[0]['crt']) for k, v in sorted_dict.iteritems()
                                    if (now - v[0]['crt']).total_seconds() > 30
                                    ]
                    if not used_cookies:
                        return

                    sorted_cookies_items = sorted(used_cookies, key=lambda item: item[1])
                    pk = sorted_cookies_items[0][0]

            self._cookies = cookies_dict[pk]
            cookie_db.insert_one({'typ': self.name, 'phone': pk, 'crt': now})

        return parse_cookie_str(self._cookies)

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
        cookies = self.cookies

        if not cookies:
            return

        yield scrapy.Request(search_url, headers=headers, cookies=cookies)

    def parse(self, response):
        target_css = 'table.m_srchList > tbody > tr:first-child > td:nth-child(2) > a::attr(href)'
        href = response.css(target_css).extract_first()
        eid = self.get_eid(href)

        if eid is None:
            return

        url = response.urljoin(href)
        headers = deepcopy(self._headers)
        headers['Referer'] = response.url
        cookies = self.cookies

        if not cookies:
            return

        yield scrapy.Request(
            url, meta={'result': {'eid': eid}},
            headers=headers, cookies=cookies, callback=self.parse_corp
        )

        self.schedule_db.insert({
            'typ': self._typ, 'upt': datetime.now(), 'word': self.search_key
        })

    def parse_corp(self, response):
        name = (response.css('div.company-top-name::text').extract_first() or '').strip()
        is_site = bool(response.css('a.company-top-url::attr(href)').extract_first())

        if not name:
            return

        name_urlencode = urllib.quote(name.encode('u8'))
        response.meta['result'].update({'name': name, 'is_site': is_site})
        response.meta['name_urlencode'] = name_urlencode

        headers = deepcopy(self._headers)
        headers['Referer'] = response.url
        headers.pop('Upgrade-Insecure-Requests')
        headers['X-Requested-With'] = 'XMLHttpRequest'

        corp_detail_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=base'.format(
            response.meta['result']['eid'], name_urlencode
        )

        cookies = self.cookies

        if not cookies:
            return

        yield scrapy.Request(
            corp_detail_url, meta=response.meta,
            headers=headers, cookies=cookies, callback=self.parse_corp_detail
        )

    def parse_corp_detail(self, response):
        industry = ''

        # 所属行业
        for tr_sel in response.css('table.m_changeList tr'):
            is_break = False
            text_list = tr_sel.css('td::text').extract()

            for index, text in enumerate(text_list):
                if u'所属行业' in text:
                    is_break = True
                    industry = text_list[index + 1].strip()
                    break

            if is_break:
                break

        # 分支机构
        is_branch = bool(response.css('section#Subcom div.panel-heading span.badge').extract_first())
        response.meta['result'].update({'is_branch': is_branch, 'ind': industry})

        headers = deepcopy(self._headers)
        headers.pop('Upgrade-Insecure-Requests')
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Referer'] = ''.join(response.request.headers['Referer'])

        risk_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=susong'.format(
            response.meta['result']['eid'], response.meta['name_urlencode']
        )

        cookies = self.cookies

        if not cookies:
            return

        yield scrapy.Request(
            risk_url, meta=response.meta,
            headers=headers, cookies=cookies, callback=self.parse_risk_info
        )

    def parse_risk_info(self, response):
        # 失信信息
        is_credit = bool(response.css('section#shixinlist div.panel-heading span.badge').extract_first())
        operation_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&tab=run'.format(
            response.meta['result']['eid'], response.meta['name_urlencode']
        )

        headers = deepcopy(self._headers)
        headers.pop('Upgrade-Insecure-Requests')
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Referer'] = ''.join(response.request.headers['Referer'])

        response.meta['result']['is_credit'] = is_credit

        cookies = self.cookies

        if not cookies:
            return

        yield scrapy.Request(
            operation_url, meta=response.meta,
            headers=headers, cookies=cookies, callback=self.parse_operation
        )

    def parse_operation(self, response):
        is_chattel_mortgage = False

        # 股权出质
        is_stock_pledge = bool(response.css('section#pledgeList div.panel-heading span.badge').extract_first())

        # 投招标
        is_bid = bool(response.css('section#tenderlist div.panel-heading span.badge').extract_first())

        # 动产抵押
        for text in response.css('div.panel-body a.m-r-sm.m-t-sm::text').extract():
            m = re.compile(r'\d+').search(text)
            if u'动产抵押' in text and m and int(m.group()):
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

        cookies = self.cookies

        if not cookies:
            return

        yield scrapy.Request(
            investment_url, meta=response.meta,
            headers=headers, cookies=cookies, callback=self.parse_investment
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

        investment_count = int(response.css('div.panel-heading span.badge::text').extract_first() or '0') - 20

        if is_last_page or investment_count <= 0:
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
            pages = investment_count / 20 + bool(investment_count % 20)

            for page in range(1, pages + 1):
                meta = deepcopy(response.meta)
                meta['is_investment'] = True
                meta['is_last_page'] = page == pages

                cookies = self.cookies

                if not cookies:
                    return

                yield scrapy.Request(
                    other_invest_url.format(eid, name_urlencode, page + 1),
                    meta=meta, headers=headers, cookies=cookies, callback=self.parse_investment
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
    crawler.crawl(QichachaSpider, search=u'众安')
    crawler.start()



