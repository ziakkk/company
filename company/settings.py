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
ROBOTSTXT_OBEY = False

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

QIXIN_COOKIE = 'aliyungf_tc=AQAAAHZldgYSHAEABhj2dJPm48UyasmI; channel=baidu; cookieShowLoginTip=3; sid=s%3AKBjPtOFnn9K0sVksWVve_rBSadcMS9IR.jXdBO9SF9vho8N6xMlQ0AYtVZaR%2FTQ1a2CZsyXY9ZDM; _zg=%7B%22uuid%22%3A%20%2215dc5023ce6777-0d1e50825ba188-6b1b1279-100200-15dc5023ce72a2%22%2C%22sid%22%3A%201505111503.093%2C%22updated%22%3A%201505112530.542%2C%22info%22%3A%201504755811691%2C%22cuid%22%3A%20%22b3da6317-15d6-4757-99fc-5159c5e0d8b1%22%7D; Hm_lvt_52d64b8d3f6d42a2e416d59635df3f71=1504755811,1504756028,1504842555; Hm_lpvt_52d64b8d3f6d42a2e416d59635df3f71=1505112531; responseTimeline=86'
TIANYANCHA_COOKIE = 'aliyungf_tc=AQAAAE12mlubPgQABhj2dHNbyIr90wi8; csrfToken=2PEUvgMJDrWhor205I07KN8a; TYCID=ca8e20607b5811e7870ddba38ac7849d; uccid=a496f66e6882eb9dbdabd06a3ae0809f; ssuid=4185346910; bannerFlag=true; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzYwMTg0MTgyMCIsImlhdCI6MTUwNDYwMTgzNSwiZXhwIjoxNTIwMTUzODM1fQ.rQxmiJqwt22ChBsmrKottoXlWWeM0Qd2h_XS2Bp7mKRF_oEY5xJ1ZzUIdtWQveZHSNnine5tLwQdpNjIq3W3rQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213601841820%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzYwMTg0MTgyMCIsImlhdCI6MTUwNDYwMTgzNSwiZXhwIjoxNTIwMTUzODM1fQ.rQxmiJqwt22ChBsmrKottoXlWWeM0Qd2h_XS2Bp7mKRF_oEY5xJ1ZzUIdtWQveZHSNnine5tLwQdpNjIq3W3rQ; RTYCID=824de562ec294d43aed542e18c80b8d0; token=a8d728607026452ab3cb3e71813545de; _utm=052d7de8ca5d40a0a6865f945f2e312f; _csrf=/e443nfJs3DdIRNGkFI7xA==; OA=9lJ7cHJsj0yOApYJ5if36o6bZ50pbmg2gXSn5eIPwjzLQt/OEVQYo9QoAPf0GqmRegKRGWqQ2xfqRwrolskm3A==; _csrf_bk=56c3a2070913bf11b418569ffc872723; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1504601823,1504773484; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504775362'
QICHACHA_COOKIE = {
    '13601841820': 'acw_tc=AQAAACAneTTwgQ4ABhj2dGQnuuCtyJ05; UM_distinctid=15dc0eed41f9b-07650eaace7a31-6b1b1279-100200-15dc0eed4202bd; gr_user_id=b1675263-be73-4840-b10f-151dd25c779b; _uab_collina=150218046698266691527842; PHPSESSID=ojhbqu2e692i704veqtcb9s1e0; hasShow=1; _umdata=55F3A8BFC9C50DDAE1513FFF088E7EA8A5F404B8708F0DB00ACEAA5497C221842B3CE3DD40749E4CCD43AD3E795C914C9D874D7745D52BC6C7F87E2DB93E4B96; zg_did=%7B%22did%22%3A%20%2215e6f7fb6c222a-020352e88b8f62-6b1b1279-100200-15e6f7fb6c31dd%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201506143550546%2C%22updated%22%3A%201506144137254%2C%22info%22%3A%201505716496591%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22fa39ac5c71f8cee30f114b7896ea20e3%22%7D; CNZZDATA1254842228=430190341-1502175979-null%7C1506139482',
    '15921538812': 'UM_distinctid=15e9d31c5e3401-038c14298c8abf-1571466f-100200-15e9d31c5e437f; _uab_collina=150587584254582559595484; acw_tc=59c77c73|dd8a57cb6a70c0b90d1144b67d46bdb8; hasShow=1; _umdata=2BA477700510A7DFE3BC62A98B5F8AB18EE40C9FCA8B40EEC5A866927CB345E6BECD1EA5DAAA6EF0CD43AD3E795C914C2D62C69C21B22D1C50BBB3AA3DDDA127; PHPSESSID=g37ilr22ibhpl0oaubaoac56v0; acw_tc=AQAAABPVa2twcQwAkvah07NzhDkbSata; zg_did=%7B%22did%22%3A%20%2215e9d31c6491a4-0813bb2911b6ba-1571466f-100200-15e9d31c64a190%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201506245744087%2C%22updated%22%3A%201506245842329%2C%22info%22%3A%201505875838562%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%22afde5cc1b404366d58b933cfb8938eb7%22%7D; CNZZDATA1254842228=1293478807-1505871673-https%253A%252F%252Fwww.sogou.com%252F%7C1506240521',
    '15800302286': 'CNZZDATA1254842228=1205608619-1506053685-%7C1506303036; _uab_collina=150605452403600885148997; hasShow=1; PHPSESSID=gf1jjts6vbku7u7if2a1p6tqb2; acw_tc=AQAAAKhScGuYqQoABhj2dAzQ7HdSxhCf; _umdata=A502B1276E6D5FEF7882387E0D99AFB2FDC1973910F4C689012B0E0BE1E077B4BB53A858D2A6095ACD43AD3E795C914C63B0CA86321EA7D4A76F666260FF2BF7; zg_did=%7B%22did%22%3A%20%2215ea7d847c351b-072995ed3316c44-3a064d5a-100200-15ea7d847c48e5%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201506305661608%2C%22updated%22%3A%201506306751639%2C%22info%22%3A%201506054522863%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.so.com%22%2C%22cuid%22%3A%20%22df1c77be85d05ae383f0e353e4a02226%22%7D; UM_distinctid=15ea7d84bb3771-04c7023b47dbc68-3a064d5a-100200-15ea7d84bb46fd',
    '13636387206': 'UM_distinctid=15eb6da37ae26-0ea2a7802b158b-18104336-100200-15eb6da37b01; hasShow=1; acw_tc=AQAAADJ/6nfqvQwABhj2dP5YsmkIjUSK; _uab_collina=150630635001360276537906; _umdata=C234BF9D3AFA6FE72B04A3821E20BA20EC956BEB2771C6B1C27BEE78990C2B8E120AFFE30D97AD09CD43AD3E795C914C63B0CA86321EA7D4E9120A7A84574080; PHPSESSID=9el1c6sjrhqepkumuhkbreffk0; zg_did=%7B%22did%22%3A%20%2215eb6da37c347-00b93fb77dce22-18104336-100200-15eb6da37c41ef%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201506306308040%2C%22updated%22%3A%201506306412698%2C%22info%22%3A%201506306308051%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%226024f259d5dacb5cc9d509b1e78b9541%22%7D; CNZZDATA1254842228=1365875980-1506303036-https%253A%252F%252Fwww.baidu.com%252F%7C1506303036',
    '13601754301': 'gr_user_id=7770da44-df15-424d-9ee0-fee74635c370; UM_distinctid=15dbfc10320c5-0c5e621cece897-41554130-100200-15dbfc103222d2; CNZZDATA1254842228=262732710-1502159779-%7C1506303036; _uab_collina=150216068419021679802797; PHPSESSID=eask2mbaur78961oet6na6r3n5; zg_did=%7B%22did%22%3A%20%2215ea3c899e3317-089b8b246cb5de-41554130-100200-15ea3c899e4344%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201506306003624%2C%22updated%22%3A%201506306163648%2C%22info%22%3A%201505986386415%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22c4b90d092f457c1cf03cfa9968e0cb58%22%7D; _umdata=0823A424438F76AB0990AB898E5881DD01206AF550DE37C78AE61EA7E9B051A32B82F749BCC2701ECD43AD3E795C914C63B0CA86321EA7D4BA0F785C30E83CB8; acw_tc=AQAAAPqtkEYkOAcABhj2dEAzyeqqx50Y; hasShow=1',
    '15000578917': 'UM_distinctid=15c1090b1b941d-02e428155d8536-4e47052e-100200-15c1090b1ba6bc; gr_user_id=e6d8bfcc-c614-43ea-bb4a-24c300610b1e; _uab_collina=149550603080366167480776; hasShow=1; acw_tc=AQAAAM7k1kOMcwMA4pH2OqLZkRoQpyA7; PHPSESSID=qj1j89raqk8ejbr6f98d6a5d92; _umdata=2BA477700510A7DFB8CE3EF15C83C95F956AC63EB0A9A826E136847499BB83BDDF82EE38A9E79DCBCD43AD3E795C914CB550F6EE09557E04B0BDB55E901AAAE4; zg_did=%7B%22did%22%3A%20%2215eb6ea5fdd155-0edb6acc31bf7c-3a3e5f04-100200-15eb6ea5fde469%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201506307366882%2C%22updated%22%3A%201506307657637%2C%22info%22%3A%201506307366886%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%226170b9d4fc2f6a86b0edb320bd902feb%22%7D; CNZZDATA1254842228=704063168-1494921223-null%7C1506303036',
}

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
