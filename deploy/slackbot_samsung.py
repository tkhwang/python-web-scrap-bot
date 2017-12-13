from slacker import Slacker

SLACK_TOKEN = ''
SLACK_BOARD = ''

class SlackBotSamsung:
    def __init__(self):
        self.token = SLACK_TOKEN
        self.slack = Slacker(self.token)
        self.slack_board = SLACK_BOARD

    def send_message(self, msg):
        self.slack.chat.post_message(self.slack_board, msg)

    def post_image(self, img):
        self.slack.files.upload(img, channels=self.slack_board)
