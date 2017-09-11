# -*- coding: utf-8 -*-

import requests
from fake_useragent import UserAgent

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.qixin.com',
    'Pragma': 'no-cache',
    'Cookie': 'aliyungf_tc=AQAAAHZldgYSHAEABhj2dJPm48UyasmI; channel=baidu; cookieShowLoginTip=3; sid=s%3A6alA3SWibzg2y8NIe3bVmeIEVBiItAel.Fxx6I0pHoih73Cp61JQH9esKxorc%2FrFfpYPW5VchJBw; Hm_lvt_52d64b8d3f6d42a2e416d59635df3f71=1502332706,1502341592,1504755811,1504756028; Hm_lpvt_52d64b8d3f6d42a2e416d59635df3f71=1504767539; _zg=%7B%22uuid%22%3A%20%2215dc5023ce6777-0d1e50825ba188-6b1b1279-100200-15dc5023ce72a2%22%2C%22sid%22%3A%201504767537.872%2C%22updated%22%3A%201504767539.73%2C%22info%22%3A%201504755811691%2C%22cuid%22%3A%20%22b3da6317-15d6-4757-99fc-5159c5e0d8b1%22%7D; responseTimeline=77',
    'User-Agent': UserAgent().random,
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://www.qixin.com/',
    '066e57d66d2d0c37a437': 'c33dea7a3271a700c970a4065f7a7b4eee97afa6633009c4daa078486cd5bb64216fb2f6ed92f8b8ab54026d90185133c004b1f481da11fe0dad4aa313e059eb'
}

print requests.get('http://www.qixin.com/api/search/suggestion?key=%E7%99%BE%E5%BA%A6', headers=DEFAULT_REQUEST_HEADERS).content