from __future__ import with_statement

import datetime
import requests
from bs4 import BeautifulSoup as bs
import json

import slackbot

JSON_FILE_NAVER = "./naver.json"
POINT = 21

class SearchNaver():
    def __init__(self):
        try:
            with open(JSON_FILE_NAVER) as f:
                self.l_naver = json.load(f)
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            self.l_naver = {
                'title': 'NAVER 실시간 검색어',
                'url': 'http://naver.com',
                'update': []
            }
            json.dump(self.l_naver, open(JSON_FILE_NAVER, "w+"))


    def serialize_msg(self, site):
        str = ''
        str += '*[*] ' + site['title'] + '*' + '\n'
        str += site['url'] + '\n'
        str += site['update'][-1]['date'] + '\n'
        for key, value in site['update'][-1]['terms'].items():
            str += value + " : " + key + "\n"
        return str


    def get_update(self):
        req = requests.get("http://naver.com")
        html = req.text
        soup = bs(html, 'lxml')

        t = {}
        t['date'] = '{}'.format(datetime.datetime.now())
        t['terms'] = {}

        l = soup.select('div.ah_roll_area > ul.ah_l > li.ah_item > a.ah_a')
        for i in l:
            t['terms'][i.select_one('span.ah_k').text] = i.select_one('span.ah_r').text
        self.l_naver['update'].append(t)

        json.dump(self.l_naver, open('naver.json', 'w+'))
        return self.serialize_msg(self.l_naver)


    def rank_to_point(self, rank):
        return POINT - int(rank)


    def summary_recent(self, numbers):
        updates = self.l_naver['update']
        summary = {}
        j = 0
        for i, update in enumerate(updates[::-1]):
            if i < numbers:
                for key, value in update['terms'].items():
                    if key in summary.keys():
                        j = summary[key]
                        summary[key] = j + self.rank_to_point(value)
                    else:
                        summary[key] = self.rank_to_point(value)
        print(summary)
        return summary


    def report_to_slack(self):
        msg = self.get_update()
        self.slack.send_message(msg)


if __name__ == '__main__':
    search_naver = SearchNaver()
    #print(search_naver.get_daum_update())
    print(search_naver.get_update())
    #searchTerm.generate_word_cloud(searchTerm.l_naver)
    #searchTerm.report_to_slack()
    search_naver.summary_recent(5)