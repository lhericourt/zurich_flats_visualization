import bs4
import urllib
import ast
import pandas as pd

##############################
### Params                 ###
##############################
NB_ROOMS_MIN = 2.0
NB_ROOMS_MAX = 3.0
PRICE_MIN = 1000.0
PRICE_MAX = 2200.0

BASE_URL = "https://www.immostreet.ch"
URL = BASE_URL + "/fr/louer/appartement/a-zurich/prix-" + str(PRICE_MIN) + "-" + str(PRICE_MAX)\
      + "/pieces-" + str(NB_ROOMS_MIN) + "-" + str(NB_ROOMS_MAX)

##############################
### Methods                ###
##############################
def get_flats_one_page(url):
    html = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(html)
    flats = []
    coords = []
    flat_one_page = soup.findAll("article", attrs={"class": u"results-item"})
    for flat in flat_one_page:
        url_flat = BASE_URL + flat.findAll("a")[0]["href"]
        url_flat = str(url_flat.encode('ascii', 'ignore').decode("utf-8"))
        flats.append(url_flat)
        coord = ast.literal_eval(flat["data-map-location"])
        coords.append(coord)
    return flats, coords


def get_all_flats(url):
    list_url_flat = []
    list_coord = []
    for i in range(1, 15):
        url_page = url + "/?pageNum=" + str(i)
        try:
            flat_one_page, coord_one_page = get_flats_one_page(url_page)
            list_url_flat += flat_one_page
            list_coord += coord_one_page
        except:
            break
    return list_url_flat, list_coord



def get_all_flats_old(url):

    html = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(html)
    nav = soup.findAll("nav", attrs={"class": u"items -pages -flexed"})[0]
    list_url_flat = []
    list_coord = []
    for page in nav.findAll("a"):
        url_page = BASE_URL + page["href"]
        flat_one_page, coord_one_page = get_flats_one_page(url_page)
        list_url_flat += flat_one_page
        list_coord += coord_one_page
    return list_url_flat, list_coord


def save_flat(file_name, urls, coords):
    lat = []
    lon = []
    for coord in coords:
        lat.append(coord["lat"])
        lon.append(coord["lng"])
    flat_df = pd.DataFrame({
        "url": urls,
        "lat": lat,
        "long" : lon
    })
    flat_df.to_csv(file_name, index=False)


if __name__ == '__main__':
    list_url_flat, list_coord = get_all_flats(URL)
    save_flat("appart_zurich_immostreet.csv", list_url_flat, list_coord)