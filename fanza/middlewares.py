# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from re import T
from scrapy import signals, Spider, Item
from scrapy.http import HtmlResponse, Request
from scrapy.http.cookies import CookieJar
from fanza.exceptions.fanza_exception import ExtractException
from fanza.movie.movie_constants import MOVIE_STORE, STORE_SOD, SOD_AGE_CHECK_URL

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class FanzaSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FanzaDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:8181"

class SodDownloaderMiddleware(object):
    def  __init__(self) -> None:
        self.jar = CookieJar(check_expired_frequency=10)
        self.processed = 0

    def process_request(self, request: Request, spider: Spider):
        if request.meta.get(MOVIE_STORE, None) != STORE_SOD:
            return
        if len(self.jar._cookies) != 0:
            spider.logger.debug('add sod cookie, url: %s', request.url)
            request.meta[MOVIE_STORE] = None
            request.headers.pop('Cookie', None)
            self.jar.add_cookie_header(request)
            self.processed += 1
            if self.processed % self.jar.check_expired_frequency == 0:
                self.jar.clear()            

    def process_response(self, request: Request, response: HtmlResponse, spider: Spider):
        if request.meta.get(MOVIE_STORE, None) != STORE_SOD:
            spider.logger.debug('not sod, url: %s', request.url)
            return response
        spider.logger.debug('extract sod cookie start, url: %s', response.url)
        self.jar.extract_cookies(response, request)
        req = Request(
            SOD_AGE_CHECK_URL,
            meta={'handle_httpstatus_list': [404], MOVIE_STORE: STORE_SOD},
            cb_kwargs=request.cb_kwargs,
            callback=request.callback,
            dont_filter=True
        )
        req.headers.appendlist('Referer', response.url)
        spider.logger.debug('add sod cookie finish, url: %s', req.url)
        return req

class GlobalExceptionHandleSpiderMiddleware(object):    
    def process_spider_exception(self, response: HtmlResponse, exception, spider: Spider):
        if isinstance(exception, ExtractException):
            spider.logger.exception(exception.get_message() + ' ,url: %s', response.url, exc_info=exception)
            return Item()
