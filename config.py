from constants import REGION_CODES

DOMAIN = "https://www.cci.fr"


class HOME_REQUEST:
    url = DOMAIN + "/web/trouver-un-professionnel-de-l-immobilier"

    @staticmethod
    def headers(user_agent):
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Host": "www.cci.fr",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent,
        }


class RESULTS_REQUEST:
    url = DOMAIN + "/web/trouver-un-professionnel-de-l-immobilier/accueil"

    @staticmethod
    def params(p_auth):
        return {
            'p_auth': p_auth,
            'p_p_id': 'CAIM_Recherche_WAR_CAIM_Rechercheportlet_INSTANCE_jA2G',
            'p_p_lifecycle': '1',
            'p_p_state': 'normal',
            'p_p_mode': 'view',
            'p_p_col_id': 'column-1',
            'p_p_col_pos': '1',
            'p_p_col_count': '3',
            '_CAIM_Recherche_WAR_CAIM_Rechercheportlet_INSTANCE_jA2G_javax.portlet.action': 'validateSubmit',
        }

    @staticmethod
    def headers(user_agent):
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://www.cci.fr',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.cci.fr/web/trouver-un-professionnel-de-l-immobilier/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        }

    @staticmethod
    def data(region):
        return {
            'nomentreprise': '',
            '_CAIM_Recherche_WAR_CAIM_Rechercheportlet_INSTANCE_jA2G_enseigne': '',
            '_CAIM_Recherche_WAR_CAIM_Rechercheportlet_INSTANCE_jA2G_siren': '',
            '_CAIM_Recherche_WAR_CAIM_Rechercheportlet_INSTANCE_jA2G_numerocarte': '',
            '_CAIM_Recherche_WAR_CAIM_Rechercheportlet_INSTANCE_jA2G_region': REGION_CODES[region],
            '_CAIM_Recherche_WAR_CAIM_Rechercheportlet_INSTANCE_jA2G_ville': '',
            '_CAIM_Recherche_WAR_CAIM_Rechercheportlet_INSTANCE_jA2G_codepostal': '',
            '_CAIM_Recherche_WAR_CAIM_Rechercheportlet_INSTANCE_jA2G_nompersonne': ''
        }


class RESULTS_PAGE_REQUEST:
    @staticmethod
    def get_page_url(page):
        if page == 0:
            return DOMAIN + "/web/trouver-un-professionnel-de-l-immobilier/resultats"
        return DOMAIN + "/web/trouver-un-professionnel-de-l-immobilier/resultats/-/resultats/%d" % page

    @staticmethod
    def url(page):
        return RESULTS_PAGE_REQUEST.get_page_url(page)

    @staticmethod
    def headers(page, user_agent):
        return {
            "Host": "www.cci.fr",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer": RESULTS_PAGE_REQUEST.get_page_url(page - 1),
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        }
