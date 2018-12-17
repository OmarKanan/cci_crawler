import argparse
import re
import sys
from glob import glob
from time import sleep

import numpy as np
import pandas as pd

import utils
from config import *
from constants import *


class RegionListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = sorted(set(values.split(",")))
        for v in values:
            assert v in REGIONS_LIST, "%s not a valid region" % v
        setattr(namespace, self.dest, values)


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

    try:
        results, total_num_pages = request_results(p_auth=p_auth, cookies=cookies, region=region, user_agent=user_agent)
    except Exception as e:
        utils.add_log(region, str(e))
        return False

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


def concatenate_results(region):
    filenames = sorted(glob(os.path.join(RESULTS_DIR, region, "*")), key=lambda x: int(re.findall("\d+", x)[0]))
    dataset = pd.concat((pd.read_csv(f, sep="\t", index_col=0) for f in filenames), ignore_index=True)
    dataset.to_excel(os.path.join(RESULTS_DIR, region + ".xls"), region, index=False, encoding="utf-8")
    utils.add_log(region=region, text="\nREGION DONE\nSaved %s" % os.path.join(RESULTS_DIR, region + ".xls"))


def crawl_region(region, start_page):
    should_continue = True
    while should_continue:
        should_continue = iter_results_pages(region=region, start_page=start_page, num_iter=NUM_REQUESTS_BEFORE_PAUSE)
        if should_continue:
            start_page += NUM_REQUESTS_BEFORE_PAUSE
            sleep(PAUSE_SLEEP)
    try:
        concatenate_results(region)
    except Exception as e:
        utils.add_log(region, str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--region", choices=REGIONS_LIST,
                       help="choose a region to crawl, for example: \"--region %s\"" % REGIONS_LIST[0])
    group.add_argument("--regions", action=RegionListAction,
                       help="choose a list of regions to crawl, for example: \"--regions %s\"" % ",".join(REGIONS_LIST[:2]))
    group.add_argument("--all_regions", help="crawl all regions", action='store_true')

    parser.add_argument("--start", default=1, type=int,
                        help="(requires --region) choose which page to start crawling, for example: \"--start 1\"")

    if "--start" in sys.argv and "--region" not in sys.argv:
        parser.error("--start requires --region")

    args = parser.parse_args()
    regions_list = [args.region] if args.region else args.regions if args.regions else REGIONS_LIST

    print("-" * 50 + "\nREGIONS THAT WILL BE CRAWLED:\n %s\n" % regions_list + "-" * 50)
    for region in regions_list:
        print("Crawling region '%s' starting from page %d" % (region, args.start))
        crawl_region(region, args.start)
        print("-" * 50)
