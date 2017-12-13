from __future__ import with_statement
import datetime
import requests
from bs4 import BeautifulSoup as bs
import json
import operator
from urllib import parse
from pyshorteners import Shortener

import slackbot



POINT = 21
NUMBER_RECENT = 20
NUMBER_OF_HOW_MANY = 30
GOOGLE_API_KEY = ''


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
                'title': 'NAVER search during recent several hours',
                'url': 'http://naver.com',
                'update': []
            }
            json.dump(self.l_naver, open(JSON_FILE_NAVER, "w+"))


    def short_link(self, url):
        shortener = Shortener('Google', api_key=GOOGLE_API_KEY)
        return '{}'.format(shortener.short(url))


    def serialize_msg(self):
        str = ''
        str += '*[*] ' + self.l_naver['title'] + '*' + '\n'
        str += self.l_naver['url'] + '\n'
        str += self.l_naver['update'][-1]['date'] + '\n'
        for key, value in self.l_naver['update'][-1]['terms'].items():
            str += '\n' + value + " : " + key + "\n"
            key_encoded = parse.quote(key)
            url = 'https://search.naver.com/search.naver?where=nexearch&query={}&ie=utf8&sm=tab_lve'.format(key_encoded)
            #link = self.short_link(url)
            str += url + '\n'
        return str


    def serialize_summary(self, summary):
        sorted_summary = sorted(summary.items(), key=operator.itemgetter(1), reverse=True)
        s = ''
        s += '*[*] ' + self.l_naver['title'] + '*' + '\n'
        for n, i in enumerate(sorted_summary):
            (word, point) = i
            s += '\n' + str(point) + " : " + word + '\n'
            word_encoded = parse.quote(word)
            url = 'https://search.naver.com/search.naver?where=nexearch&query={}&ie=utf8&sm=tab_lve'.format(word_encoded) 
            #link = self.short_link(url)
            s += url + '\n'
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

    
    def publish(self):
        m = self.get_update()
        self.report_to_slack(m)


if __name__ == '__main__':
    search_naver = SearchNaver()
    search_naver.publish()

