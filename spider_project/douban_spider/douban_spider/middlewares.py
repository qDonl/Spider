# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random

import requests
from scrapy import signals
from douban_spider.models import ProxyModel
from twisted.internet.defer import DeferredLock


class UserAgentDownloaderMiddleware(object):
    def __init__(self):
        self.UserAgents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
            'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
            'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16',
        ]

    def process_request(self, request, spider):
        useragent = random.choice(self.UserAgents)
        request.headers['User-Agent'] = useragent


class ProxyDownloaderMiddleware(object):
    def __init__(self):
        super(ProxyDownloaderMiddleware, self).__init__()
        self.PROXY_URL = "http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="
        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self, request, spider):
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            self.upgrade_proxy()
            request.meta['proxy'] = self.current_proxy.proxy

    def process_process(self, request, response, spider):
        if response.status != 200:
            self.upgrade_proxy()
            return request
        return response

    def upgrade_proxy(self):
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expiring:
            resp = requests.get(self.PROXY_URL)
            result = resp.text
            data = json.loads(result)['data'][0]
            if data:
                proxy_model = ProxyModel(data)
                self.current_proxy = proxy_model
        self.lock.release()


