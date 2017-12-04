from selenium import webdriver
import slackbot
import datetime
import requests
import os
import time


URL_PACKET = "https://www.packtpub.com/packt/offers/free-learning"
IMG_PACKET = "./../img/packet.png"

class Packtbook:
    def __init__(self):
        self.slack = slackbot.SlackBot()
        self.scraps = { 'result' : [] }
        os.system("rm -rf " + IMG_PACKET)


    def beautify_msg(self, msgs):
        str = ''
        str += msgs['head']
        msgs = msgs['result']
        for msg in msgs:
            str += "\n\n"
            str += msg['title'] + "( remaining {})".format(msg['time'])
            str += "\n"
            str += msg['img']
        return str

    def get_update(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        driver = webdriver.Chrome('./../run/mac/chromedriver', chrome_options=options)
        #driver = webdriver.Chrome('./../run/mac/chromedriver')

        driver.get('https://www.packtpub.com/packt/offers/free-learning')
        driver.implicitly_wait(10)

        self.scraps['head'] = "\n\n[*] Packtbook : {}\n{}".format(datetime.datetime.now(), URL_PACKET)

        book_title = driver.find_element_by_css_selector('#deal-of-the-day > div > div > div > div > h2').text
        remained_time = driver.find_element_by_css_selector('#deal-of-the-day > div > div > div > div.eighteen-days-countdown-bar > span').text
        img = driver.find_element_by_css_selector('#deal-of-the-day > div > div > div > a > img').get_attribute('src')
        self.scraps['result'].append({
            'title': book_title
            , 'time' : remained_time
            , 'img' : img
        })

        """
        res = requests.get(img, stream=True)
        f = open(IMG_PACKET, 'wb+')
        for chunk in res.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        time.sleep(3)
        """
        driver.quit()
        return self.beautify_msg(self.scraps)

    def report_to_slack(self):
        msg = self.get_update()
        self.slack.send_message(msg)


if __name__ == '__main__':
    packtbook = Packtbook()
    packtbook.report_to_slack()
