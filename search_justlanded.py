import bs4
import urllib
import ast
import pandas as pd
import requests

##############################
### Params                 ###
##############################
PRICE_MIN = "1000"
PRICE_MAX = "3000"
SQM_MIN = "50"
SQM_MAX = "100"

BASE_URL = "https://housing.justlanded.com"

URL = BASE_URL + "/en/Switzerland_Zurich/For-Rent_Apartments"

VALUES = {
    "q_cid":"77",
    "q_cid":"77",
    "q_ppid":"5",
    "q_ppid":"5",
    "q_pmin": PRICE_MIN,
    "q_pmax": PRICE_MAX,
    "q_b":"1,5",
    "range":"1,5",
    "q_au":"1",
    "q_smin": SQM_MIN,
    "q_smax": SQM_MAX,
    "more_options": "false",
    "cb_list": "115",
    "q_t[]": "115",
    "q_l_opt": "all",
    "cb_list": "en",
    "q_l[]": "en"
}

##############################
### Methods                ###
##############################
def get_one_flat_coord(url):
    r = requests.post(url, data=VALUES)
    soup = bs4.BeautifulSoup(r.content)


    div_with_geo = soup.findAll("li", attrs={"class": "margin-bottom item-browse-box item f_s  "})[0]

    geo = ast.literal_eval(div_with_geo.findAll("div")[0]["data-location"])
    return geo

def get_all_flats_coord(list_url):
    list_coord = []
    for url in list_url:
        list_coord.append(get_one_flat_coord(url))
    return list_coord


def get_url_flat_one_page(url):
    r = requests.post(url, data=VALUES)
    soup = bs4.BeautifulSoup(r.content)

    flat_url_list = []
    links_one_page = soup.findAll("ul", attrs={"class": "item_list listings"})[0]
    for link in links_one_page.findAll("li"):
        try:
            flat_url_list.append(str(link.attrs["data-url"].encode('ascii', 'ignore').decode("utf-8")))
        except:
            pass

    return flat_url_list


def get_all_urls_flat(url):
    flat_url_list = []
    last_page = get_last_page(url)
    for i in range(1, 30):
        url_page = url if i == 1 else url + "/" + str(i)
        print(url_page)
        flat_url_list += get_url_flat_one_page(url_page)
        if (i >= last_page):
            break
        last_page = get_last_page(url)
    return flat_url_list


def get_last_page(url):
    r = requests.post(url, data=VALUES)
    soup = bs4.BeautifulSoup(r.content)
    max_page = 0
    links_one_page = []
    try:
        section_pagination = soup.findAll("div", attrs={"class": "pagination"})[0]
        links_one_page = section_pagination.findAll("a")
    except:
          pass

    for link in links_one_page:
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
        "long": lon
    })
    flat_df.to_csv(file_name, index=False)


if __name__ == '__main__':
    list_url_flat = get_all_urls_flat(URL)
    list_coords = get_all_flats_coord(list_url_flat)
    save_flat("appart_zurcih_justlanded.csv", list_url_flat, list_coords)