# -*- coding: utf-8 -*-
import re
import urllib
import json
from random import choice
from copy import deepcopy
from datetime import datetime

import scrapy
from pymongo import MongoClient
from fake_useragent import UserAgent
from company import defaults


class QixinSpider(scrapy.Spider):
    name = 'qixin'
    allowed_domains = ['www.qixin.com']
    custom_settings = {'DOWNLOAD_DELAY': 2}

    def __init__(self, **kwargs):
        self._typ = 'qixin'
        self._cookie = kwargs.pop('cookie', None)
        self.search_key = kwargs.pop('search', None)
        self.user_agent = choice(defaults.USER_AGENT)
        self.invests = []

        self._headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': self.user_agent,
            'Host': 'www.qixin.com',
            'Upgrade-Insecure-Requests': '1',
        }

        self.client = MongoClient()
        self.db = self.client.crawl.corp_info
        self.schedule_db = self.client.crawl.corp_schedule

        super(QixinSpider, self).__init__(**kwargs)

    @property
    def cookies(self):
        cookies = self._cookie or self.settings['QIXIN_COOKIE']
        return dict([ck.split('=', 1) for ck in cookies.split(';')])

    @staticmethod
    def get_eid(url):
        if not url:
            return None

        eid_regex = re.compile(r'/company/(.*?)$')
        eid_m = eid_regex.search(url)

        return eid_m.group(1) if eid_m else None

    def start_requests(self):
        if self.search_key is None:
            return

        headers = deepcopy(self._headers)
        headers['Referer'] = 'http://www.qixin.com/'

        if isinstance(self.search_key, unicode):
            word = self.search_key.encode('u8')
        else:
            word = self.search_key

        key_urlencode = '%' in word and urllib.quote(word) or word
        search_url = 'http://www.qixin.com/search?key={}'.format(key_urlencode)

        yield scrapy.Request(search_url, headers=headers, cookies=self.cookies)

    def parse(self, response):
        print 'h1:', response.request.headers
        print 'h1:', response.request.cookies
        # print response.body

        href = response.css('div#s2-c1 div.company-title > a::attr(href)').extract_first()
        print 'href:', href
        eid = self.get_eid(href)
        print 'eid:', eid

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
        risk_url = 'http://www.qixin.com/company-risk/{}'.format(response.meta['result']['eid'])
        name = response.css('div.container div[class="row"] h3::text').extract_first() or ''
        print 'name:', name

        for tr_sel in response.css('div#icinfo table tr'):
            is_break = False
            td_test_list = tr_sel.css('td::text').extract()

            for index, text in enumerate(td_test_list):
                if u'所属行业' in text:
                    is_break = True
                    industry = td_test_list[index + 1]
                    break

            if is_break:
                break

        office_site = response.css(u'a[data-event-name="企业官网"]::attr(href)').extract_first()
        is_site = bool(office_site)

        # 分支机构
        branches = response.css('div#branches h4 span.badge::text').extract_first() or '0'
        is_branch = bool(int(branches.strip().replace(' ', '')))
        response.meta['result'].update({
            'is_site': is_site, 'is_branch': is_branch, 'ind': industry, 'name': name
        })

        headers = deepcopy(self._headers)
        headers['Referer'] = response.url

        yield scrapy.Request(
            risk_url, meta=response.meta,
            headers=headers, cookies=self.cookies, callback=self.parse_risk_info
        )

    def parse_risk_info(self, response):
        risk = {}
        operation_url = 'http://www.qixin.com/company-operation/{}'.format(response.meta['result']['eid'])

        # 失信信息
        execution = response.css('div#execution h4 span.badge::text').extract_first() or '0'
        risk['is_credit'] = bool(int(execution.strip().replace(' ', '')))

        # 股权出质
        equity = response.css('div#equity h4 span.badge::text').extract_first() or '0'
        risk['is_stock_pledge'] = bool(int(equity.strip().replace(' ', '')))

        # 动产抵押
        mortgages = response.css('div#mortgages h4 span.badge::text').extract_first() or '0'
        risk['is_chattel_mortgage'] = bool(int(mortgages.strip().replace(' ', '')))

        response.meta['result'].update(risk)
        headers = deepcopy(self._headers)
        headers['Referer'] = response.url

        yield scrapy.Request(
            operation_url, meta=response.meta,
            headers=headers, cookies=self.cookies, callback=self.parse_operation
        )

    def parse_operation(self, response):
        investment_url = 'http://www.qixin.com/company-investment/{}'.format(response.meta['result']['eid'])

        bid = response.css('div#bidding h4 span.badge::text').extract_first() or '0'
        is_bid = bool(int(bid.strip().replace(' ', '')))

        response.meta['result'].update(is_bid=is_bid)
        headers = deepcopy(self._headers)
        headers['Referer'] = response.url

        yield scrapy.Request(
            investment_url, meta=response.meta,
            headers=headers, cookies=self.cookies, callback=self.parse_investment
        )

    def parse_investment(self, response):
        time_regex = re.compile(ur'(成立.*?年)', re.S)
        capital_regex = re.compile(ur'注册资本：(.*)|注册资本:(.*)', re.S)

        investment = response.css('div#s2-c0 h4.section-title span.badge::text').extract_first() or '0'
        investment_count = int(investment.strip().replace(' ', '')) - 10
        print 'invest:', investment, investment_count

        for sel in response.css('div.app-investment-list div.investment-item'):
            name = sel.css('div.col-2 > div.col-2-1 > div:first-child > h5 > a::text').extract_first() or ''
            text = sel.css('div.col-2 > div.col-2-1 > div:nth-child(2)::text').extract_first() or ''

            _time = time_regex.findall(text)
            captical = capital_regex.findall(text)

            self.invests.append({
                'name': name,
                'time': _time and _time[0] or '',
                'capital': captical and (captical[0][0] or captical[0][1]) or ''
            })

        response.meta['result']['invests'] = self.invests
        self.insert_db(response.meta['result'])

        # if investment_count <= 0:
        #     response.meta['result']['invests'] = self.invests
        #     self.insert_db(response.meta['result'])
        #     return

        # 请求头含有一个随机变量， 目前无法捕捉
        # investment_pages = investment_count / 10 + bool(investment_count % 10)
        # other_investment_url = 'http://www.qixin.com/api/enterprise/getInvestment'
        # print 'invest pages:', investment_pages
        #
        # for page in range(1, investment_pages + 1):
        #     headers = deepcopy(self._headers)
        #     headers.pop('Upgrade-Insecure-Requests')
        #     headers['Referer'] = response.url
        #     headers['Content-Length'] = '55'
        #     headers['Content-Type'] = 'application/json;charset=UTF-8'
        #     headers['Origin'] = 'http://www.qixin.com'
        #     headers['Accept'] = 'application/json, text/plain, */*'
        #     headers['X-Requested-With'] = 'XMLHttpRequest'
        #
        #     meta = deepcopy(response.meta)
        #     meta['is_last_page'] = page == investment_pages
        #     print 'is_last_page:', meta['is_last_page']
        #     data = {'eid': meta['result']['eid'], 'page': page + 1}
        #     print other_investment_url
        #
        #     yield scrapy.Request(
        #         other_investment_url, method='POST', body=json.loads(data),
        #         meta=meta, headers=headers, cookies=self.cookies, callback=self.parse_other_investment
        #     )

    def parse_other_investment(self, response):
        invest_list = []
        is_last_page = response.meta['is_last_page']

        data = json.loads(response.body)
        for item in data:
            invest_list.append({
                'name': item['name'], 'time': item['establishmentPeriod'], 'capital': item['regCapi']
            })

        response.meta['result']['invests'].extand(invest_list)

        if is_last_page:
            self.insert_db(response.meta['result'])

    def insert_db(self, document):
        document['typ'] = self._typ
        document['search'] = self.search_key
        document['upt'] = datetime.now()

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
    crawler.crawl(QixinSpider, search=u'阿里巴巴')
    crawler.start()
