import datetime
import requests
from bs4 import BeautifulSoup as bs
import slackbot


class SearchTerms():
    def __init__(self):
        self.l_naver = []
        self.l_daum  = []
        self.slack = slackbot.SlackBot()

    def beautify_msg(self):
        str = ''

        str += '\n[*] Naver @{}\n'.format(datetime.datetime.now())
        for i in self.l_naver:
            str += i + '\n'

        str += '\n[*] Daum @{}\n'.format(datetime.datetime.now())
        for i in self.l_daum:
            str += i + '\n'
        #print(str)
        return str

    def get_update(self):
        # NAVER
        req = requests.get("http://naver.com")
        html = req.text
        soup = bs(html, 'lxml')

        l = soup.select('div.ah_roll_area > ul.ah_l > li.ah_item > a.ah_a > span.ah_k')
        for i in l:
            self.l_naver.append(i.text)

        # DAUM
        req = requests.get("http://daum.net")
        html = req.text
        soup = bs(html, 'lxml')

        l = soup.select('ol.list_hotissue.issue_row.list_mini a.link_issue')
        for i in l:
            self.l_daum.append(i.text)

        return self.beautify_msg()

    def report_to_slack(self):
        msg = self.get_update()
        self.slack.send_message(msg)


if __name__ == '__main__':
    searchTerm = SearchTerms()
    searchTerm.report_to_slack()