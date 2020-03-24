# -*- coding: utf-8 -*-
import scrapy
import re
import pdb
from time import sleep

class testSpider(scrapy.Spider):
    name = 'hltv'
    def start_requests(self):
        urls = [
            'https://www.hltv.org/stats/matches/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse1)

    def parse1(self, response):

	#Gets links to specific match stat pages from the list of all matches
        XPATH_MATCHES = "//div[@class='stats-section']/table/tbody/tr"
        matches = response.xpath(XPATH_MATCHES)
        match_links = response.xpath("//div[@class='stats-section']/table/tbody/tr/td/a").extract()

        for match in match_links:
            sleep(0.5)
            m = re.search('mapstatsid(.+?)">\n', match)
            if m:
                found = m.group(1)
                newURL = 'https://www.hltv.org/stats/matches/mapstatsid' + found
                yield(scrapy.Request(url = newURL, callback = self.parse2))


    def parse2(self, response):
        #Parsing of individual match pages here - eg. https://www.hltv.org/stats/matches/mapstatsid/100636/hellraisers-vs-pompa
        #pdb.set_trace()
        XPATH_SCOREBOX = "//div[@class='match-info-box']"
        XPATH_LEFT_TEAM_NAME = "/div[@class='team-left']/img"
        XPATH_LEFT_TEAM_SCORE = "/div[@class='team-left']/div"
        XPATH_RIGHT_TEAM_NAME = "/div[@class='team-right']/img"
        XPATH_RIGHT_TEAM_SCORE = "/div[@class='team-right']/div"

        raw_left_team_name = response.xpath(XPATH_SCOREBOX + XPATH_LEFT_TEAM_NAME).extract()
        raw_right_team_name = response.xpath(XPATH_SCOREBOX + XPATH_RIGHT_TEAM_NAME).extract()
        raw_left_team_score = response.xpath(XPATH_SCOREBOX + XPATH_LEFT_TEAM_SCORE).extract()
        raw_right_team_score = response.xpath(XPATH_SCOREBOX + XPATH_RIGHT_TEAM_SCORE).extract()

        yield{
                'team1_name': raw_left_team_name,
                'team2_name': raw_right_team_name,
                'team1_score': raw_left_team_score,
                'team2_score': raw_right_team_score }

         
'''
        with open('test', 'wb') as f:
            f.write(matches)
        self.log('Saved file %s' % 'test')
'''
