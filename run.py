import argparse
from time import sleep

import numpy as np
import utils
from config import *
from constants import *


def request_home(user_agent):
    command = utils.get_curl_command(url=HOME_REQUEST.url, headers=HOME_REQUEST.headers(user_agent))
    response = utils.run_command(command)
    cookies = utils.retrieve_cookies(response)
    p_auth = utils.retrieve_p_auth(response)
    return response, cookies, p_auth


def request_results(p_auth, cookies, region, user_agent):
    command = utils.get_curl_command(url=RESULTS_REQUEST.url, headers=RESULTS_REQUEST.headers(user_agent),
                                     params=RESULTS_REQUEST.params(p_auth), cookies=cookies,
                                     data=RESULTS_REQUEST.data(region))
    response = utils.run_command(command)
    results = utils.retrieve_page_results(response, page=1)
    num_pages = utils.retrieve_number_of_pages(response)
    return results, num_pages


def request_results_page(page, cookies, user_agent):
    command = utils.get_curl_command(url=RESULTS_PAGE_REQUEST.url(page),
                                     headers=RESULTS_PAGE_REQUEST.headers(page, user_agent), cookies=cookies)
    response = utils.run_command(command)
    results = utils.retrieve_page_results(response, page)
    return results


def save_results(results, region, page):
    filename = os.path.join(RESULTS_DIR, region, "page_%d.txt" % page)
    results.to_csv(filename, sep="\t")
    utils.add_log(region, "Page %d done" % page)


def iter_results_pages(region, start_page, num_iter):
    user_agent = utils.random_user_agent()
    home_page_response, cookies, p_auth = request_home(user_agent=user_agent)

    results, total_num_pages = request_results(p_auth=p_auth, cookies=cookies, region=region, user_agent=user_agent)
    if start_page == 1:
        sleep(np.random.random() * (MAX_SLEEP - MIN_SLEEP) + MIN_SLEEP)
        save_results(results=results, region=region, page=1)

    for page in range(max(2, start_page), start_page + num_iter):
        if page > total_num_pages:
            return False
        try:
            sleep(np.random.random() * (MAX_SLEEP - MIN_SLEEP) + MIN_SLEEP)
            results = request_results_page(page=page, cookies=cookies, user_agent=user_agent)
            save_results(results=results, region=region, page=page)
        except Exception as e:
            utils.add_log(region, str(e))

    return True


def crawl_region(region, start_page):
    should_continue = True
    while should_continue:
        should_continue = iter_results_pages(region=region, start_page=start_page, num_iter=NUM_REQUESTS_BEFORE_PAUSE)
        start_page += NUM_REQUESTS_BEFORE_PAUSE
        sleep(PAUSE_SLEEP)
    utils.add_log(region, "\nREGION DONE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", help="choose which region to crawl", choices=REGIONS_LIST, required=True)
    parser.add_argument("--start_page", help="choose which page to start crawling", default=1)
    args = parser.parse_args()

    start_page = int(args.start_page)
    print("Crawling region '%s' starting from page %d" % (args.region, start_page))
    crawl_region(args.region, start_page)
