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
PRICE_MAX = 2800.0

BASE_URL = "https://www.home.ch"

URL = BASE_URL + "/en/rent/f/apartment_and_house/at-zurich/price-" + str(PRICE_MIN) + "-" + str(PRICE_MAX)\
      + "/rooms-" + str(NB_ROOMS_MIN) + "-" + str(NB_ROOMS_MAX)

##############################
### Methods                ###
##############################
def get_one_flat_coord(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opener.addheaders = [('Host', 'www.homegate.ch')]
    html = opener.open(url)
    soup = bs4.BeautifulSoup(html)
    div_with_geo = soup.findAll("div", attrs={"class": "map"})[0]
    geo = ast.literal_eval(div_with_geo.findAll("div")[0]["data-location"])
    return geo

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
    links_one_page = soup.findAll("section", attrs={"class": "search-results__list"})[0]
    for link in links_one_page.findAll("a"):
        flat_url_list.append(BASE_URL + str(link["href"].encode('ascii', 'ignore').decode("utf-8")))
    return flat_url_list


def get_all_urls_flat(url):
    flat_url_list = []
    for i in range(1, 30):
        url_page = url + "?pageNum=" + str(i) + "&view=list"
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
    links_one_page = soup.findAll("nav", attrs={"class": "pagination"})[0]
    for link in links_one_page.findAll("a"):
        try:
            page_number = int(link.getText())
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
    save_flat("appart_zurich_home.csv", list_url_flat, list_coords)