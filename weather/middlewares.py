# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import time
from selenium import webdriver
from utils.selenium_request import SeleniumRequest
from scrapy.http import HtmlResponse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import HardwareType, OperatingSystem

# driver = webdriver.Chrome()
# driver.get('http://www.cma.gov.cn')

# print(driver.title)

# driver.quit()


def randomUserAgent():
    operating_systems = [OperatingSystem.CHROMEOS.value]
    hardware_types = [HardwareType.COMPUTER.value]
    user_agent_rotator = UserAgent(operating_systems=operating_systems,hardware_types=hardware_types)
    ua = user_agent_rotator.get_random_user_agent()
    return ua

class SeleniumSpiderMiddleware(object):
    def __init__(self):
        self.driver = None

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_closed, signals.spider_closed)
        return s 

    def process_request(self, request, spider):
        if not isinstance(request, SeleniumRequest):
            return None
        # time.sleep(10)
        
        ua = randomUserAgent()
        opts = Options()
        opts.add_argument(ua)
        opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
        desired_capabilities = DesiredCapabilities.CHROME.copy()  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities, options=opts)
        driver.get(request.url)
        timeout = WebDriverWait(driver, 10)
        timeout.until(EC.presence_of_element_located((By.NAME, 'province')))
        
        driver.execute_script(request.script)
        time.sleep(3)
        body = str.encode(driver.page_source)
        currenturl = driver.current_url

        driver.delete_all_cookies()
        driver.close()
        return HtmlResponse(
            currenturl,
            body=body,
            encoding='utf-8',
            request=request,
        )

    def spider_closed(self):
        pass
        # if self.driver:
        #     self.driver.quit()

class WeatherSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
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


class WeatherDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        # logging.warning("12123")
        # logging.warning(cls)
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
