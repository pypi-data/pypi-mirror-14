# -*- coding: utf-8 -*-

BOT_NAME = 'scrashtest'

SPIDER_MODULES = ['scrashtest.spiders']
NEWSPIDER_MODULE = 'scrashtest.spiders'

DOWNLOADER_MIDDLEWARES = {
    # Engine side
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # Downloader side
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
SPLASH_URL = 'http://192.168.99.100:8050/'
# SPLASH_URL = 'http://ec2-52-89-166-109.us-west-2.compute.amazonaws.com:8050/'

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
HTTPCACHE_ENABLED = True
# HTTPCACHE_IGNORE_MISSING = True
# CLOSESPIDER_PAGECOUNT = 20
DEPTH_LIMIT = 5
