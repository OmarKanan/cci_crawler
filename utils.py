import math
import re
import subprocess

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from config import *
from constants import *


def add_log(region, text):
    print(text)
    with open(os.path.join(LOGS_DIR, "%s.txt" % region), mode="a") as f:
        f.write(text + "\n")


def random_user_agent():
    return np.random.choice(USER_AGENTS_LIST)


def get_curl_command(url, params=None, headers=None, cookies=None, data=None):
    cmd = "curl -Lsi --compressed '" + url + "'"
    if params:
        cmd = cmd[:-1] + "?" + "&".join(k + "=" + v for k, v in params.items()) + "'"
    if headers:
        cmd += " -H " + " -H ".join("'%s: %s'" % (k, v) for k, v in headers.items())
    if cookies:
        cmd += " -H 'Cookie: " + "; ".join("%s=%s" % (k, v) for k, v in cookies.items()) + "'"
    if data:
        cmd += " --data '" + "&".join(k + "=" + v for k, v in data.items()) + "'"
    return cmd


def run_command(command):
    return subprocess.getoutput(command)


def retrieve_cookies(response):
    cookies = dict(re.findall("set-cookie: ([^\s]*)=([^\s]*);", response, re.IGNORECASE))
    if not cookies:
        raise Exception("No cookies found")
    return cookies


def retrieve_p_auth(response):
    matches = re.findall("p_auth=([^&]*)&", response, re.IGNORECASE)
    if not matches:
        raise Exception("No auth found")
    return matches[-1]


def retrieve_number_of_pages(response):
    matches = re.findall("(\d+) résultats trouvés", response)
    if not matches:
        raise Exception("Number of results not found")
    return int(math.ceil(int(matches[-1]) / NUM_RESULTS_BY_PAGE))


def strip_text(text):
    return re.sub("\s+", " ", text).strip()


def format_new_result(name, columns, page):
    if len(columns) != 3:
        raise Exception("Row with %d number of columns instead of 3" % len(columns))
    return {
        COLUMN.PAGE: page,
        COLUMN.NOM: name,
        COLUMN.DOCUMENT: strip_text(columns[0].find("a").get_text()),
        COLUMN.URL: strip_text(DOMAIN + columns[0].find("a").get("href")),
        COLUMN.LIEU: strip_text(columns[1].get_text()),
        COLUMN.REGION: strip_text(columns[2].get_text()),
    }


def retrieve_table_results(table, page):
    results = []
    current_name = None

    for row in table.findAll("tr"):
        row_class = row.get("class", [None])[0]

        if not row_class:
            name = row.find("td", {"class": "titre_entreprise"})
            if name:
                current_name = name.get_text()

        elif row_class == "ligne":
            columns = row.findAll("td")
            results.append(format_new_result(current_name, columns, page))

    return pd.DataFrame(results)[[COLUMN.PAGE, COLUMN.NOM, COLUMN.LIEU, COLUMN.REGION, COLUMN.DOCUMENT, COLUMN.URL]]


def retrieve_page_results(response, page):
    soup = BeautifulSoup(response, "html.parser")
    tables = soup.findAll("table", {"class": "tableauResultat"})
    if not tables:
        raise Exception("No table of class 'tableauResultat' found")
    return retrieve_table_results(tables[-1], page)
