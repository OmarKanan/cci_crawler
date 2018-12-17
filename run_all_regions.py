import subprocess

from constants import *


if __name__ == "__main__":
    for region in REGIONS_LIST:
        subprocess.getoutput("python run.py --region=%s --start_page=1" % region)
