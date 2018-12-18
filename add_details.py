import argparse
import sys
from time import sleep

import numpy as np
import pandas as pd

import utils
from config import *
from constants import *
from crawl import request_home, RegionListAction


def request_details(url, cookies, user_agent, region):
    command = utils.get_curl_command(url=url, headers=CARTE_PRO_REQUEST.headers(user_agent), cookies=cookies)
    response = utils.run_command(command)
    details = utils.retrieve_details(response, region)
    return details


def save_details(details, region, url, num):
    with open(os.path.join(DETAILS_DIR, region + ".txt"), mode="a") as f:
        f.write("%s\t%s\t%s\t%s\n" % (url, details[0], details[1], details[2]))
    utils.add_log(region, "%s %d done" % (CARTE_PRO, num))


def save_excel_with_details(region, data):
    try:
        details = pd.read_csv(os.path.join(DETAILS_DIR, region + ".txt"), sep="\t", header=None, index_col=0)
        details.columns = [COLUMN.DETAIL_1, COLUMN.DETAIL_2, COLUMN.DETAIL_3]
        details_dict = {c: details[c].to_dict() for c in details.columns}

        dataset = data.copy()
        for c in details.columns:
            dataset[c] = data[COLUMN.URL].map(details_dict[c])

        filename = os.path.join(RESULTS_WITH_DETAILS_DIR, region + ".xls")
        dataset.to_excel(filename, region, index=False, encoding="utf-8")
        utils.add_log(region=region, text="\nREGION DONE\nSaved %s" % filename)

    except Exception as e:
        utils.add_log(region, e, is_exception=True)


def iter_details(data, region, start, num_iter, user_agent):
    cp_index = data[data.document == CARTE_PRO].index
    cp_index = cp_index[start - 1:start - 1 + num_iter]
    sub_data = data.loc[cp_index]

    if sub_data.empty:
        return False

    try:
        cookies, p_auth = request_home(user_agent=user_agent)
    except Exception as e:
        utils.add_log(region, e, is_exception=True)
        return False

    for i, url in enumerate(sub_data[COLUMN.URL]):
        sleep(np.random.random() * (MAX_SLEEP - MIN_SLEEP) + MIN_SLEEP)
        try:
            details = request_details(url=url, cookies=cookies, user_agent=user_agent, region=region)
            save_details(details=details, region=region, url=url, num=start + i)
        except Exception as e:
            utils.add_log(region, e, is_exception=True)

    if len(cp_index) < num_iter:
        return False
    return True


def get_region_details(region, start):
    utils.add_log(region, "-" * 50)
    data = pd.read_excel(os.path.join(RESULTS_DIR, region + ".xls"))
    data.index = np.arange(1, len(data) + 1)

    should_continue = True
    while should_continue:
        should_continue = iter_details(data=data, region=region, start=start, num_iter=NUM_REQUESTS_BEFORE_PAUSE,
                                       user_agent=utils.random_user_agent())
        if should_continue:
            start += NUM_REQUESTS_BEFORE_PAUSE
            sleep(PAUSE_SLEEP)

    save_excel_with_details(region=region, data=data)


def add_details():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--region", choices=REGIONS_LIST,
                       help="choose a region to add details, for example: \"--region %s\"" % REGIONS_LIST[0])
    group.add_argument("--regions", action=RegionListAction,
                       help="choose a list of regions to add details, for example: \"--regions %s\""
                            % ",".join(REGIONS_LIST[:2]))
    group.add_argument("--all_regions", help="add details for all regions", action='store_true')

    parser.add_argument("--start", default=1, type=int,
                        help="(requires --region) choose which 'carte pro' to start adding details, for example: \"--start 1\"")
    args = parser.parse_args()

    if "--start" in sys.argv and "--region" not in sys.argv:
        parser.error("--start requires --region")

    regions_list = [args.region] if args.region else args.regions if args.regions else REGIONS_LIST
    print("-" * 50 + "\nREGIONS THAT WILL BE ADDED DETAILS:\n %s\n" % regions_list + "-" * 50)

    for region in regions_list:
        print("Adding details to region '%s' starting from 'carte pro' %d" % (region, args.start))
        get_region_details(region, args.start)
        print("-" * 50)


if __name__ == "__main__":
    add_details()
