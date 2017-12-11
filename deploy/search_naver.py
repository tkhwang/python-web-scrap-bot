from __future__ import with_statement
import datetime
import requests
from bs4 import BeautifulSoup as bs
import json
import operator

import slackbot



POINT = 21
NUMBER_RECENT = 20
NUMBER_OF_HOW_MANY = 30

Local = True
if Local:
    # Local
    JSON_FILE_NAVER = "./naver.json"
else:
    # Server
    JSON_FILE_NAVER = "/root/deploy/naver.json"


class SearchNaver():

    def __init__(self):
        self.slack = slackbot.SlackBot()
        try:
            with open(JSON_FILE_NAVER) as f:
                self.l_naver = json.load(f)
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            self.l_naver = {
                'title': 'NAVER famous search terms',
                'url': 'http://naver.com',
                'update': []
            }
            json.dump(self.l_naver, open(JSON_FILE_NAVER, "w+"))


    def serialize_msg(self):
        str = ''
        str += '*[*] ' + self.l_naver['title'] + '*' + '\n'
        str += self.l_naver['url'] + '\n'
        str += self.l_naver['update'][-1]['date'] + '\n'
        for key, value in self.l_naver['update'][-1]['terms'].items():
            str += value + " : " + key + "\n"
        return str


    def serialize_summary(self, summary):
        sorted_summary = sorted(summary.items(), key=operator.itemgetter(1), reverse=True)
        s = ''
        s += '*[*] ' + self.l_naver['title'] + '*' + '\n'
        for n, i in enumerate(sorted_summary):
            (word, point) = i
            s += str(point) + " : " + word + '\n'
        return s


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
        return self.serialize_msg()


    def rank_to_point(self, rank):
        return POINT - int(rank)


    def summary_recent(self, recent_how_many):
        updates = self.l_naver['update']
        summary = {}
        j = 0
        for i, update in enumerate(updates[::-1]):
            if i < recent_how_many:
                for key, value in update['terms'].items():
                    if key in summary.keys():
                        j = summary[key]
                        summary[key] = j + self.rank_to_point(value)
                    else:
                        summary[key] = self.rank_to_point(value)
        # https://stackoverflow.com/a/7197351/2453632
        most_summary = dict(sorted(summary.items(), key=operator.itemgetter(1), reverse=True)[:NUMBER_OF_HOW_MANY])
        return most_summary


    def report_to_slack(self, msg):
        self.slack.send_message(msg)


if __name__ == '__main__':
    search_naver = SearchNaver()
    print(search_naver.get_update())
    #print(search_naver.serialize_summary(search_naver.summary_recent(NUMBER_RECENT)))


