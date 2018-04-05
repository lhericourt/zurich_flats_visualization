import bs4
import urllib
import ast
import pandas as pd

##############################
### Params                 ###
##############################
NB_ROOMS_MIN = 2
NB_ROOMS_MAX = 3
PRICE_MIN = "1t"
PRICE_MAX = "22h"

BASE_URL = "https://www.immoscout24.ch"

URL = BASE_URL + "/fr/appartement/louer/lieu-zuerich?pf=" + str(PRICE_MIN) + "&pt=" + str(PRICE_MAX)\
      + "&nrf=" + str(NB_ROOMS_MIN) + "&nrt=" + str(NB_ROOMS_MAX)

##############################
### Methods                ###
##############################
def get_one_flat_coord(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opener.addheaders = [('Host', 'www.immoscout24.ch')]
    html = opener.open(url)
    soup = bs4.BeautifulSoup(html)
    possible_links = soup.findAll("a")
    link_to_get_geo = ""
    lat_long = ""
    for link in possible_links:
        if str(link["href"].encode('ascii', 'ignore').decode("utf-8")).startswith("https://maps.google.com/"):
            link_to_get_geo = str(link["href"].encode('ascii', 'ignore').decode("utf-8"))
            lat_long = link_to_get_geo[len("https://www.google.com/maps?q=") + 1 : ].split(",")
    return {"lat": float(lat_long[0]), "lng": float(lat_long[1])}

def get_all_flats_coord(list_url):
    list_coord = []
    for url in list_url:
        list_coord.append(get_one_flat_coord(url))
    return list_coord


def get_url_flat_one_page(url_search):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opener.addheaders = [('Host', 'www.immoscout24.ch')]
    html = opener.open(url_search)
    soup = bs4.BeautifulSoup(html)
    flat_url_list = []
    links_one_page = soup.findAll("a", attrs={"class": "item-title"})
    for link in links_one_page:
        flat_url_list.append(BASE_URL + str(link["href"].encode('ascii', 'ignore').decode("utf-8")))
    return flat_url_list


def get_all_urls_flat(url):
    flat_url_list = []
    for i in range(1, 20):
        url_page = url + "&pn=" + str(i) + "&ps=30"
        try:
            print(url_page)
            flat_url_list += get_url_flat_one_page(url_page)
        except:
            break
    return flat_url_list


def save_flat(file_name, urls, coords):
    lat = []
    lon = []
    for coord in coords:
        lat.append(coord["lat"])
        lon.append(coord["lng"])
    flat_df = pd.DataFrame({
        "url": urls,
        "lat": lat,
        "long": lon
    })
    flat_df.to_csv(file_name, index=False)


if __name__ == '__main__':
    list_url_flat = get_all_urls_flat(URL)
    list_coords = get_all_flats_coord(list_url_flat)
    save_flat("appart_zurich_immoscout.csv", list_url_flat, list_coords)