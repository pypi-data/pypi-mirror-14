# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.linkextractors import LinkExtractor

from scrapy_splash import SplashRequest


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = ['http://www.dmoz.org/']

    # http_user = 'splash-user'
    # http_pass = 'splash-password'

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            yield SplashRequest(
                link.url,
                self.parse_link,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )

    def parse_link(self, response):
        print("PARSED", response.real_url, response.url)
        print(response.css("title").extract())
        print(response.data["har"]["log"]["pages"])
        print(response.headers.get('Content-Type'))



class MySpider(scrapy.Spider):
    name = 'dmoz2'
    custom_settings = {
        # 'COOKIES_DEBUG': True,
        'DEPTH_PRIORITY': -1,
    }
    handle_httpstatus_list = [400]

    script = """
    function last_response_headers(splash)
      local entries = splash:history()
      local last_entry = entries[#entries]
      return last_entry.response.headers
    end

    function main(splash)
      if splash.args.cookies ~= nil then
        splash:init_cookies(splash.args.cookies)
      end
      assert(splash:go{splash.args.url, headers=splash.args.headers})
      assert(splash:wait(0.5))

      return {
        headers = last_response_headers(splash),
        cookies = splash:get_cookies(),
        html = splash:html()
      }
    end
    """

    # allowed_domains = ["dmoz.org"]
    start_urls = ['http://www.dmoz.org/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='execute',
                args={'lua_source': self.script}
            )

    def parse(self, response):
        # print(response.data)
        print(response.css('title').extract_first())
        # print(response.headers)
        # print(response.data['headers'])
        # print(response.data['cookies'])

        le = LinkExtractor()
        for link in le.extract_links(response):
            yield SplashRequest(
                link.url,
                self.parse_link,
                endpoint='execute',
                args={'lua_source': self.script},
            )

    def parse_link(self, response):
        print(response.css('title').extract_first())
        # print(response.data['cookies'])

        # print(response.data["har"]["log"]["pages"])
        # print(response.headers.get('Content-Type'))
