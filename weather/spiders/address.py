# -*- coding: utf-8 -*-
import scrapy
from utils.selenium_request import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
from utils.user_agent import get_random_useragent

class AddressSpider(scrapy.Spider):
    name = 'address'
    allowed_domains = ['www.cma.gov.cn']
    js_script = '''
        var selector = document.querySelector('select[name=province]');  
        selector.options[14].selected = true;
        var event = document.createEvent("HTMLEvents");
        event.initEvent("change", true, true);
        selector.dispatchEvent(event);
    '''

    def start_requests(self):
        url = 'http://www.cma.gov.cn/'
        # headers = {
        #     "Connection": "keep-alive",
        #     "Upgrade-Insecure-Requests": 1,
        #     "User-Agent": get_random_useragent(),
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        # }
        
        yield SeleniumRequest(
            url=url, 
            callback=self.parse,
            # wait_time=5,
            # wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name=province]')),
            # script=self.js_script,
            )
        # yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):
        logging.warning("aaabbafdsafasdfasdf")
        logging.warning(response.css('select[name=chinacity]').get())
