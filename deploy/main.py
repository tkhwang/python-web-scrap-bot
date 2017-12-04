import schedule
import time
import reddit
import search_terms


def run_search_terms():
    v_searchTerm = search_terms.SearchTerms()
    v_searchTerm.report_to_slack()


def run_reddit():
    BOARDS = [
        "securityCTF",
        "MachineLearning",
        "learnmachinelearning"
    ]
    v_reddit = reddit.Reddit()
    for board in BOARDS:
        print(v_reddit.report_to_slack(board))


if __name__ == '__main__':
    schedule.every(1).hour.do(run_search_terms)
    schedule.every(1).hour.do(run_reddit)

    while True:
        schedule.run_pending()
        time.sleep(1)