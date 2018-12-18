import os


class COLUMN:
    PAGE = "page"
    NOM = "nom"
    DOCUMENT = "document"
    URL = "url"
    LIEU = "lieu"
    REGION = "region"
    DETAIL_1 = "detail_1"
    DETAIL_2 = "detail_2"
    DETAIL_3 = "detail_3"


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

REGIONS_LIST = sorted([x[1] for x in REGION.__dict__.items() if not x[0].startswith("__")])
assert set(REGION_CODES) == set(REGIONS_LIST)


def create_dir(name):
    directory = os.path.join(os.getcwd(), name)
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def create_sub_results_dirs():
    for region in REGIONS_LIST:
        region_dir = os.path.join(RESULTS_DIR, region)
        if not os.path.exists(region_dir):
            os.mkdir(region_dir)


def create_user_agents_list():
    with open("user_agents.txt") as f:
        user_agents = [x.strip() for x in f.readlines()]
    return user_agents


LOGS_DIR = create_dir("logs")
RESULTS_DIR = create_dir("results")
DETAILS_DIR = create_dir("details")
RESULTS_WITH_DETAILS_DIR = create_dir("results_with_details")
create_sub_results_dirs()

USER_AGENTS_LIST = create_user_agents_list()

NUM_RESULTS_BY_PAGE = 10

MIN_SLEEP = 1
MAX_SLEEP = 5
NUM_REQUESTS_BEFORE_PAUSE = 30
PAUSE_SLEEP = 30

CARTE_PRO = "Carte Professionnelle"
