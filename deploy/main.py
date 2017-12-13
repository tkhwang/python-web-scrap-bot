import schedule
import time
import reddit
import search_naver
import packtbook
import analyze_word


Local = False
if Local:
    # Local
    WORD_CLOUD_NAVER = './naver.png'
else:
    WORD_CLOUD_NAVER = '/root/deploy/naver.png'

NUMBER_RECENT = 30


def run_packtbook():
    v_packtbook = packtbook.Packtbook()
    v_packtbook.publish()


def run_naver_serach():
    v_naver_search = search_naver.SearchNaver()
    # Caution ! Just get_update, not publish.
    v_naver_search.get_update()


def run_wordcloud_naver_search():

    v_analyze_word = analyze_word.AnalyzeWord()
    v_search_naver = search_naver.SearchNaver()

    summary = v_search_naver.summary_recent(NUMBER_RECENT)

    tags = v_analyze_word.get_tags(summary)
    v_analyze_word.draw_pytagcloud(tags, WORD_CLOUD_NAVER, (2700, 2700))
    v_analyze_word.post_image_to_slack(WORD_CLOUD_NAVER)

    v_analyze_word.report_to_slack(v_search_naver.serialize_summary(summary))    


def run_reddit_python():
    v_reddit = reddit.Reddit('Python')
    v_reddit.publish()


def run_reddit_ctf():
    v_reddit = reddit.Reddit('securityCTF')
    v_reddit.publish()


def run_reddit_django():
    v_reddit = reddit.Reddit('djangolearning')
    v_reddit.publish()


if __name__ == '__main__':
    schedule.every().day.at("09:10").do(run_packtbook)

    schedule.every(30).minutes.do(run_naver_serach)
    schedule.every().day.at("08:00").do(run_wordcloud_naver_search)
    schedule.every().day.at("17:00").do(run_wordcloud_naver_search)

    schedule.every().day.at("09:00").do(run_reddit_python)
    schedule.every().day.at("10:00").do(run_reddit_ctf)
    schedule.every().day.at("11:00").do(run_reddit_django)

    while True:
        schedule.run_pending()
        time.sleep(1)
