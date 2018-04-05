import bs4
import urllib2
import urllib
import ast
import pandas as pd

##############################
### Params                 ###
##############################
Q_SMIN= "50"

PRICE_MIN = "1000"
PRICE_MAX = "3000"

BASE_URL = "https://housing.justlanded.com"

URL = BASE_URL + "/en/Switzerland_Zurich/For-Rent_Apartments/"

values = {"q_cid":"77",
        "q_cid":"77",
        "q_ppid":"5",
        "q_ppid":"5",
        "q_pmin":PRICE_MIN,
        "q_pmax":PRICE_MAX,
        "q_b":"1,5",
        "range":"1,5",
        "q_au":"1",
        "q_smin":Q_SMIN,
        "q_smax":"",
        "more_options":"true",
        "cb_list":"115",
        "q_t[]":"115",
        "q_l_opt":"some",
        "cb_list":"en",
        "q_l[]":"en"}

data = urllib.urlencode(values)
req = urllib2.Request(URL, data)
html = urllib2.urlopen(req)
soup = bs4.BeautifulSoup(html)
print(soup)

##############################
### Methods                ###
##############################
def get_one_flat_coord(url):
    opener = urllib2.build_opener()
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
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opener.addheaders = [('Host', 'www.homegate.ch')]
    html = opener.open(url_search)
    soup = bs4.BeautifulSoup(html)
    flat_url_list = []
    #print(url_search)
    links_one_page = soup.findAll("section", attrs={"class": "search-results__list"})[0]
    #print(links_one_page)
    for link in links_one_page.findAll("a"):
        flat_url_list.append(BASE_URL + link["href"].encode('ascii', 'ignore'))
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
    opener = urllib2.build_opener()
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