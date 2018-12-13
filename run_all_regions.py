import os
import re
import subprocess
from glob import glob

import pandas as pd

import utils
from constants import *


if __name__ == "__main__":
    for region in REGIONS_LIST:
        subprocess.getoutput("python run.py --region=%s --start_page=1" % region)
        filenames = sorted(glob(os.path.join(RESULTS_DIR, region, "*")), key=lambda x: int(re.findall("\d+", x)[0]))
        dataset = pd.concat((pd.read_csv(f, sep="\t", index_col=0) for f in filenames), ignore_index=True)
        dataset.to_excel(os.path.join(RESULTS_DIR, region + ".xls"), region, index=False, encoding="utf-8")
        utils.add_log(region=region, text="Saved %s" % os.path.join(RESULTS_DIR, region + ".xls"))