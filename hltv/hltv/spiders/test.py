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

        #Overall Score
        XPATH_SCOREBOX = "//div[@class='match-info-box']"
        XPATH_LEFT_TEAM_NAME = "/div[@class='team-left']/img"
        XPATH_LEFT_TEAM_SCORE = "/div[@class='team-left']/div"
        XPATH_RIGHT_TEAM_NAME = "/div[@class='team-right']/img"
        XPATH_RIGHT_TEAM_SCORE = "/div[@class='team-right']/div"

        raw_left_team_name = response.xpath(XPATH_SCOREBOX + XPATH_LEFT_TEAM_NAME).extract()
        raw_right_team_name = response.xpath(XPATH_SCOREBOX + XPATH_RIGHT_TEAM_NAME).extract()
        raw_left_team_score = response.xpath(XPATH_SCOREBOX + XPATH_LEFT_TEAM_SCORE).extract()
        raw_right_team_score = response.xpath(XPATH_SCOREBOX + XPATH_RIGHT_TEAM_SCORE).extract()
        

        ##Round by round score
        RH_T1H1 = response.xpath("//div[@class='round-history-half']")[0]
        RH_T1H2 = response.xpath("//div[@class='round-history-half']")[1]
        RH_T2H1 = response.xpath("//div[@class='round-history-half']")[2]
        RH_T2H2 = response.xpath("//div[@class='round-history-half']")[3]

        indiv_rounds_Xpath = 'child::node()/@title'

        Team1Half1 = RH_T1H1.xpath(indiv_rounds_Xpath)
        Team1Half2 = RH_T1H2.xpath(indiv_rounds_Xpath)
        Team2Half1 = RH_T2H1.xpath(indiv_rounds_Xpath)
        Team2Half2 = RH_T2H2.xpath(indiv_rounds_Xpath)

        

        #For each round, take the data for the filled in team (winning team)
        roundScoresH1 = [99] * len(Team1Half1)

        #pdb.set_trace()
        roundNo = 1
        roundScoresFilledH1 = roundScoresH1

        for curRound in roundScoresH1:
            
            val1 = Team1Half1[roundNo - 1].extract()
            val2 = Team2Half1[roundNo - 1].extract()
            if len(val1) >= len(val2):
                roundScoresFilledH1[roundNo - 1] = val1
            else:
                roundScoresFilledH1[roundNo - 1] = val2
            roundNo = roundNo + 1

        roundScoresH2 = [99] * len(Team1Half2)
        
        roundNo = 1
        roundScoresFilledH2 = roundScoresH2

        for curRound in roundScoresH2:
            val1 = Team1Half2[roundNo - 1].extract()
            val2 = Team2Half2[roundNo - 1].extract()
            if len(val1) > len(val2):
                roundScoresFilledH2[roundNo - 1] = val1
            else:
                roundScoresFilledH2[roundNo - 1] = val2
            roundNo = roundNo + 1




        yield{
                'team1_name': raw_left_team_name,
                'team2_name': raw_right_team_name,
                'team1_score': raw_left_team_score,
                'team2_score': raw_right_team_score, 
                'r1_score': roundScoresFilledH1[0], 
                'r2_score': roundScoresFilledH1[1], 
                'r3_score': roundScoresFilledH1[2]
 }

         
'''
        with open('test', 'wb') as f:
            f.write(matches)
        self.log('Saved file %s' % 'test')
'''
