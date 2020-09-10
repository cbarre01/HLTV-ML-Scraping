# -*- coding: utf-8 -*-
import scrapy
import re
import pdb
from time import sleep

scrapeNo = 450

class testSpider(scrapy.Spider):
    name = 'hltv'
    def start_requests(self):

            
        
        urls = self.getMatchPageURLs()
        for url in urls:
            sleep(5) ## Avoid angering website
            yield scrapy.Request(url=url, callback=self.parse1)

    def getMatchPageURLs(self):
        #Returns all the seperate web pages of most recent MAX_MATCH_NUM matches as a list
        MAX_MATCH_NUM = 1000
        #match_page_offsets = range(50,MAX_MATCH_NUM,50)
        match_page_offsets = [scrapeNo]
        match_page_urls = []
        base_url = 'https://www.hltv.org/stats/matches/'
        for i, os in enumerate(match_page_offsets):
            match_page_urls.append(base_url + "?offset=" + str(os))
        return match_page_urls

    def parse1(self, response):
	#Gets links to specific match stat pages from the list of all matches, which are then handled by parse2
        XPATH_MATCHES = "//div[@class='stats-section']/table/tbody/tr"
        matches = response.xpath(XPATH_MATCHES)
        match_links = response.xpath("//div[@class='stats-section']/table/tbody/tr/td/a").extract()

        #sleep(5) ## Avoid angering website
        for match in match_links:
            sleep(0.5) ## Avoid angering website
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


        #parse/cleaning
        clean_left_team_name = raw_left_team_name[0].split()[1][5:]
        clean_right_team_name = raw_right_team_name[0].split()[1][5:]
        clean_left_team_score = raw_left_team_score[0].split()[2]
        clean_right_team_score = raw_right_team_score[0].split()[2]

        clean_left_team_score =re.search('>(.*)<',clean_left_team_score).group(1)
        clean_right_team_score =re.search('>(.*)<',clean_right_team_score).group(1)


        yield{
                'team1_name': clean_left_team_name,
                'team2_name': clean_right_team_name,
                'team1_score': clean_left_team_score,
                'team2_score': clean_right_team_score, 
                'r1_score': roundScoresFilledH1[0], 
                'r2_score': roundScoresFilledH1[1], 
                'r4_score': roundScoresFilledH1[3],
                'r5_score': roundScoresFilledH1[4],
                'r6_score': roundScoresFilledH1[5],
                'r7_score': roundScoresFilledH1[6],
                'r8_score': roundScoresFilledH1[7],
                'r9_score': roundScoresFilledH1[8],
                'r10_score': roundScoresFilledH1[9],
                'r11_score': roundScoresFilledH1[10],
                'r12_score': roundScoresFilledH1[11],
                'r13_score': roundScoresFilledH1[12],
                'r14_score': roundScoresFilledH1[13],
                'r15_score': roundScoresFilledH1[14],
                'r16_score': roundScoresFilledH2[0],
                'r17_score': roundScoresFilledH2[1],
                'r18_score': roundScoresFilledH2[2],
                'r19_score': roundScoresFilledH2[3],
                'r20_score': roundScoresFilledH2[4],
                'r21_score': roundScoresFilledH2[5],
                'r22_score': roundScoresFilledH2[6],
                'r23_score': roundScoresFilledH2[7],
                'r24_score': roundScoresFilledH2[8],
                'r25_score': roundScoresFilledH2[9],
                'r26_score': roundScoresFilledH2[10],
                'r27_score': roundScoresFilledH2[11],
                'r28_score': roundScoresFilledH2[12],
                'r29_score': roundScoresFilledH2[13],
                'r30_score': roundScoresFilledH2[14],
 }

'''         
        filename = 'hltv' + str(scrapeNo)
        with open(filename, 'wb') as f:
            f.write(matches)
        self.log('Saved file %s' % 'filename')
'''

