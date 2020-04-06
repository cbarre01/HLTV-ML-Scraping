# -*- coding: utf-8 -*-
import scrapy
#import pdb


class BrspiderSpider(scrapy.Spider):
    #pdb.set_trace()
    name = 'BRSpider'
    def start_requests(self):
        urls = [
            'https://www.hltv.org/stats/matches/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = "test"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file' % filename)
	
        
