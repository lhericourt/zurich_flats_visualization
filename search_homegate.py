import bs4
import urllib
import ast
import pandas as pd

##############################
### Params                 ###
##############################
NB_ROOMS_MIN = 2
NB_ROOMS_MAX = 3
PRICE_MIN = 1000
PRICE_MAX = 2200

BASE_URL = "https://www.homegate.ch"

URL = BASE_URL + "/louer/appartement/lieu-zurich/liste-annonces?ag=" + str(PRICE_MIN) + "&ah=" + str(PRICE_MAX)\
      + "&ac=" + str(NB_ROOMS_MIN) + "&ad=" + str(NB_ROOMS_MAX) + "&tab=list"

##############################
### Methods                ###
##############################
def get_one_flat_coord(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opener.addheaders = [('Host', 'www.homegate.ch')]
    html = opener.open(url)
    soup = bs4.BeautifulSoup(html)
    div_with_geo = soup.findAll("div", attrs={"class": "map-container"})[0]
    return {"lat": float(div_with_geo["data-coords-lat"]), "lng": float(div_with_geo["data-coords-lon"])}

def get_all_flats_coord(list_url):
    list_coord = []
    for url in list_url:
        list_coord.append(get_one_flat_coord(url))
    return list_coord


def get_url_flat_one_page(url_search):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opener.addheaders = [('Host', 'www.homegate.ch')]
    html = opener.open(url_search)
    soup = bs4.BeautifulSoup(html)
    flat_url_list = []
    #print(url_search)
    links_one_page = soup.findAll("a", attrs={"class": "detail-page-link box-row--link"})
    #print(links_one_page)
    for link in links_one_page:
        flat_url_list.append(BASE_URL + str(link["href"].encode('ascii', 'ignore').decode("utf-8")) + "/proximite")
    return flat_url_list


def get_all_urls_flat(url):
    flat_url_list = []
    for i in range(1, 30):
        url_page = url + "&ep=" + str(i)
        print(url_page)
        last_page = get_last_page(url_page)
        flat_url_list += get_url_flat_one_page(url_page)
        if (i >= last_page):
            break
    return flat_url_list


def get_last_page(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opener.addheaders = [('Host', 'www.homegate.ch')]
    html = opener.open(url)
    soup = bs4.BeautifulSoup(html)
    max_page = 0
    links_one_page = soup.findAll("li", attrs={"class": "page-link"})
    for link in links_one_page:
        try:
            page_number = int(link.findAll("a")[0].getText())
            if page_number > max_page:
                max_page = page_number
        except:
            pass
    return max_page

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
    list_url_flat = get_all_urls_flat(URL)
    list_coords = get_all_flats_coord(list_url_flat)
    save_flat("appart_zurich_homegate.csv", list_url_flat, list_coords)