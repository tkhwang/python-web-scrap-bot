from slacker import Slacker


class SlackBot:
    def __init__(self):
        self.token = ''
        self.slack = Slacker(self.token)
        self.slack_board = '#z-bot'

    def send_message(self, msg):
        self.slack.chat.post_message(self.slack_board, msg)
