from slacker import Slacker

SLACK_TOKEN = ''
SLACK_BOARD = ''

class SlackBot:
    def __init__(self):
        self.token = SLACK_TOKEN
        self.slack = Slacker(self.token)
        self.slack_board = SLACK_BOARD

    def send_message(self, msg):
        self.slack.chat.post_message(self.slack_board, msg)
