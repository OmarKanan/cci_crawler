import os


def create_user_agents_list():
    with open("user_agents.txt") as f:
        user_agents = [x.strip() for x in f.readlines()]
    return user_agents


USER_AGENTS_LIST = create_user_agents_list()


class COLUMN:
    PAGE = "page"
    NOM = "nom"
    DOCUMENT = "document"
    URL = "url"
    LIEU = "lieu"
    REGION = "region"


class REGION:
    AUVERGNE_RHONE_ALPES = "auvergne_rhone_alpes"
    BOURGOGNE_FRANCHE_COMTE = "bourgogne_franche_comte"
    BRETAGNE = "bretagne"
    CENTRE_VAL_DE_LOIRE = "centre_val_de_loire"
    COLLECTIVITES_DOUTRE_MER = "collectivites_doutre_mer"
    CORSE = "corse"
    GRAND_EST = "grand_est"
    GUADELOUPE = "guadeloupe"
    GUYANE = "guyane"
    HAUTS_DE_FRANCE = "hauts_de_france"
    ILE_DE_FRANCE = "ile_de_france"
    LA_REUNION = "la_reunion"
    MARTINIQUE = "martinique"
    MAYOTTE = "mayotte"
    NORMANDIE = "normandie"
    NOUVELLE_AQUITAINE = "nouvelle_aquitaine"
    OCCITANIE = "occitanie"
    PAYS_DE_LA_LOIRE = "pays_de_la_loire"
    PROVENCE_ALPES_COTE_DAZUR = "provence_alpes_cote_dazur"


REGIONS_LIST = sorted([x[1] for x in REGION.__dict__.items() if not x[0].startswith("__")])

REGION_CODES = {
    REGION.AUVERGNE_RHONE_ALPES: "84",
    REGION.BOURGOGNE_FRANCHE_COMTE: "27",
    REGION.BRETAGNE: "53",
    REGION.CENTRE_VAL_DE_LOIRE: "24",
    REGION.COLLECTIVITES_DOUTRE_MER: "99",
    REGION.CORSE: "94",
    REGION.GRAND_EST: "44",
    REGION.GUADELOUPE: "01",
    REGION.GUYANE: "03",
    REGION.HAUTS_DE_FRANCE: "32",
    REGION.ILE_DE_FRANCE: "11",
    REGION.LA_REUNION: "04",
    REGION.MARTINIQUE: "02",
    REGION.MAYOTTE: "06",
    REGION.NORMANDIE: "28",
    REGION.NOUVELLE_AQUITAINE: "75",
    REGION.OCCITANIE: "76",
    REGION.PAYS_DE_LA_LOIRE: "52",
    REGION.PROVENCE_ALPES_COTE_DAZUR: "93",
}

assert set(REGION_CODES) == set(REGIONS_LIST)


def create_logs_dirs():
    logs_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    return logs_dir


def create_results_dirs():
    results_dir = os.path.join(os.getcwd(), "results")
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    for region in REGIONS_LIST:
        region_dir = os.path.join(results_dir, region)
        if not os.path.exists(region_dir):
            os.mkdir(region_dir)

    return results_dir


RESULTS_DIR = create_results_dirs()
LOGS_DIR = create_logs_dirs()

NUM_RESULTS_BY_PAGE = 10

MIN_SLEEP = 1
MAX_SLEEP = 5
NUM_REQUESTS_BEFORE_PAUSE = 30
PAUSE_SLEEP = 60
