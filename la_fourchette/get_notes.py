import bs4
import urllib
import ast
import pandas as pd
import unicodedata

RESTO_NAMES = ['La Marée', 'Le Tizi', 'Chez Bibi', 'Au Petit Marguery Rive Droite', 'My Boat', 'Chez Françoise', 'Café des Peupliers',"L'Entrée des Artistes", 'Guo Min', 'Il Castello','Le Petit Pasteur', 'Au Petit Marguery Rive Gauche','Le Buisson Ardent', 'Restaurant Athénais', 'Carré des Ternes','Zafran', 'Casa Paco', 'Zerda Café Paris 17','Restaurant Pharamond', 'Chez Frézet', 'Sagar Matha','Paris en Scène', 'Le Caroubier', 'Le Diamant de Paris',"L'Affineur Affiné", 'Au Goût du Monde', 'Le Montebello','La Petite Bretagne Brasserie', 'Le Bien Décidé','La Bastide Odéon', 'Les Vignes du Liban', 'Au Doux Raisin','Le Lion Indomptable', 'Le Maharajah', 'Les Cèdres du Liban','Le Viaduc Café', 'Millésimes 62', 'Jaipur Café','Les Passagers de Beyrouth']


def get_infos_resto(soup, name_resto):
    all_results = soup.findAll("h3", attrs={"class": "resultItem-name"})
    style = ""
    note = 0
    nb_advices = 0
    for one_resto in all_results:
        name_one_resto = one_resto.findAll("a")[0].get_text()
        name_one_resto = unicodedata.normalize('NFD', name_one_resto).encode('ascii', 'ignore').decode("utf-8")
        name_one_resto = name_one_resto.replace("-", "")
        name_one_resto = name_one_resto.replace(" ", "")
        name_resto = unicodedata.normalize('NFD', name_resto).encode('ascii', 'ignore').decode("utf-8")
        name_resto = name_resto.replace("-", "")
        name_resto = name_resto.replace(" ", "")
        if (name_resto.upper() in name_one_resto.upper()) or (name_one_resto.upper() in name_resto.upper()):

            style = soup.findAll("span", attrs={"restaurantTag restaurantTag--medium"})[0].get_text()
            style = unicodedata.normalize('NFD', style).encode('ascii', 'ignore').decode("utf-8")
            try:
                note = soup.findAll("span", attrs={"rating-ratingValue"})[0].get_text()[:3]
                note = float(note.replace(",", "."))
                nb_advices = soup.findAll("div", attrs={"reviewsCount reviewsCount--small"})[0].get_text()
            except:
                pass
    print({"style": style, "note": note, "nb_advices": nb_advices})
    return {"style": style, "note": note, "nb_advices": nb_advices}


if __name__ == '__main__':

    styles = []
    notes = []
    nb_advices = []

    for name in RESTO_NAMES:
        url = "https://www.lafourchette.com/search-refine/" + name + "/2017-12-22/21:00:00/2"
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        #opener.addheaders = [('Host', 'www.homegate.ch')]

        url = unicodedata.normalize('NFD', url).encode('ascii', 'ignore').decode("utf-8")
        print(url)
        html = opener.open(url)
        soup = bs4.BeautifulSoup(html, "lxml")
        infos = get_infos_resto(soup, name)
        styles.append(infos["style"])
        notes.append(infos["note"])
        nb_advices.append(infos["nb_advices"])
    RESTO_NAMES = [unicodedata.normalize('NFD', x).encode('ascii', 'ignore').decode("utf-8") for x in RESTO_NAMES]
    infos_df = pd.DataFrame({"name": RESTO_NAMES, "style": styles, "note": notes, "nb_advices": nb_advices})
    infos_df.to_csv("results_infos_restos.csv", index=False)