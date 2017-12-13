from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import requests
from bs4 import BeautifulSoup as bs

import slackbot
import slackbot_samsung


Local = True
if Local:
    # Local
    SCREENSHOT_PREFIX = './'
    PHANTOMJS = '../run/phantomjs'
else:
    # Server
    SCREENSHOT_PREFIX = '/root/deploy/'
    PHANTOMJS= '/root/run/phantomjs'


class Reddit(object):
    def __init__(self, board):
        self.slack = slackbot.SlackBot()
        self.slack_samsung = slackbot_samsung.SlackBotSamsung()
        self.board = board

    def arrange_link(self, ref):
        t = ref.text
        l = ref['href']
        if l[:3] == "/r/":
            l = "https://www.reddit.com" + l
        if l[-1] == "/":
            l = l[:-1]
        return (t, l)


    def beautify_msg(self, msgs):
        str = ''
        str += '\n\n[*] @ /r/{} in {}'.format(self.board, datetime.datetime.now())
        msgs = msgs[self.board]
        for msg in msgs:
            str += "\n\n"
            str += msg['title']
            str += "\n"
            str += msg['link']
        return str


    def get_update(self):

        options = DesiredCapabilities.PHANTOMJS
        options["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        driver = webdriver.PhantomJS('phantomjs', desired_capabilities=options)

        driver.get("https://www.reddit.com/r/" + self.board)
        driver.implicitly_wait(3)
        driver.save_screenshot(SCREENSHOT_PREFIX + self.board + '.png')

        scraps = {}

        with requests.Session() as s:
            s.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
            first_page = s.get('https://www.reddit.com/r/' + self.board)
    
            html = first_page.text
            soup = bs(html, 'lxml')
    
            refs = soup.select('div > div > p.title > a')
            scraps[self.board] = []
            for ref in refs:
                title, link = self.arrange_link(ref)
                if title == "updating the sidebar links":
                    continue
                scraps[self.board].append({
                    'title' : title,
                    'link'  : link
                })
        return self.beautify_msg(scraps)


    # veritas
    def report_to_slack(self, msg):
        self.slack.send_message(msg)


    def post_image_to_slack(self, img):
        self.slack.post_image(img)

    # samsung
    def report_to_slack_samsung(self, msg):
        self.slack.send_message(msg)


    def post_image_to_slack_samsung(self, img):
        self.slack.post_image(img)


    def publish(self):
        m = self.get_update()                
        self.post_image_to_slack(SCREENSHOT_PREFIX + self.board + '.png')
        self.report_to_slack(m)


if __name__ == '__main__':

    reddit = Reddit('Python')
    reddit.publish()
