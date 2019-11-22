import scrapy
import logging
from scrapy.utils.log import configure_logging
from scrapy.loader import ItemLoader
from hello.items import HelloItem, MainLoader


configure_logging(install_root_handler=False)

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        for quote in response.css('div.quote'):
            l = MainLoader(item=HelloItem(), selector=quote,response=response)
            l.add_css('text', 'span.text::text')  
            l.add_css('author', '.quote small.author::text')
            l.add_css('tags', 'div.tags a.tag::text') 
            yield l.load_item()

        #     yield {
        #         'text': quote.css('span.text::text').get(),
        #         'author': quote.css('span small::text').get(),
        #         'tags': quote.css('div.tags a.tag::text').getall(),
        #     }

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tag::text').getall(),
    #         }
    #     next_page = response.css('li.next a::attr(href)').get()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse)
