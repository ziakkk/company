# -*- coding: utf-8 -*-

# Scrapy settings for company project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'company'

SPIDER_MODULES = ['company.spiders']
NEWSPIDER_MODULE = 'company.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'company (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
}

QIXIN_COOKIE = 'aliyungf_tc=AQAAAHZldgYSHAEABhj2dJPm48UyasmI; channel=baidu; cookieShowLoginTip=3; sid=s%3A6alA3SWibzg2y8NIe3bVmeIEVBiItAel.Fxx6I0pHoih73Cp61JQH9esKxorc%2FrFfpYPW5VchJBw; Hm_lvt_52d64b8d3f6d42a2e416d59635df3f71=1502332706,1502341592,1504755811,1504756028; Hm_lpvt_52d64b8d3f6d42a2e416d59635df3f71=1504767539; _zg=%7B%22uuid%22%3A%20%2215dc5023ce6777-0d1e50825ba188-6b1b1279-100200-15dc5023ce72a2%22%2C%22sid%22%3A%201504767537.872%2C%22updated%22%3A%201504767539.73%2C%22info%22%3A%201504755811691%2C%22cuid%22%3A%20%22b3da6317-15d6-4757-99fc-5159c5e0d8b1%22%7D; responseTimeline=77'
TIANYANCHA_COOKIE = 'aliyungf_tc=AQAAAE12mlubPgQABhj2dHNbyIr90wi8; csrfToken=2PEUvgMJDrWhor205I07KN8a; TYCID=ca8e20607b5811e7870ddba38ac7849d; uccid=a496f66e6882eb9dbdabd06a3ae0809f; ssuid=4185346910; bannerFlag=true; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzYwMTg0MTgyMCIsImlhdCI6MTUwNDYwMTgzNSwiZXhwIjoxNTIwMTUzODM1fQ.rQxmiJqwt22ChBsmrKottoXlWWeM0Qd2h_XS2Bp7mKRF_oEY5xJ1ZzUIdtWQveZHSNnine5tLwQdpNjIq3W3rQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213601841820%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzYwMTg0MTgyMCIsImlhdCI6MTUwNDYwMTgzNSwiZXhwIjoxNTIwMTUzODM1fQ.rQxmiJqwt22ChBsmrKottoXlWWeM0Qd2h_XS2Bp7mKRF_oEY5xJ1ZzUIdtWQveZHSNnine5tLwQdpNjIq3W3rQ; RTYCID=824de562ec294d43aed542e18c80b8d0; token=a8d728607026452ab3cb3e71813545de; _utm=052d7de8ca5d40a0a6865f945f2e312f; _csrf=/e443nfJs3DdIRNGkFI7xA==; OA=9lJ7cHJsj0yOApYJ5if36o6bZ50pbmg2gXSn5eIPwjzLQt/OEVQYo9QoAPf0GqmRegKRGWqQ2xfqRwrolskm3A==; _csrf_bk=56c3a2070913bf11b418569ffc872723; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1504601823,1504773484; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504775362'

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'company.middlewares.CompanySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'company.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'company.pipelines.CompanyPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
