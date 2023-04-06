import time
import requests
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = 'https://www.kijiji.ca/'


start_page = 1

def get_original_url(address: str, sorting: str) -> str:
    if sorting:
        if 'low' in sorting or 'asc' in sorting:
            sorting = 'priceAsc'
        elif 'high' in sorting or 'desc' in sorting:
            sorting = 'priceDesc'
        room_and_rental_term_url = BASE_URL + f'b-for-rent/city-of-toronto/{address}/page-1/k0c30349001l1700273?sort={sorting}'
    else:
        room_and_rental_term_url = BASE_URL + f'b-for-rent/city-of-toronto/{address}/page-1/k0c30349001l1700273'
    return room_and_rental_term_url

def get_links(url: str) -> list:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    ads = soup.find_all("div", attrs={'class': 'search-item'})
    # remove third-party ad
    ads = [x for x in ads if ("cas-channel" not in x["class"]) & ("third-party" not in x["class"])]

    # create a list to store all of the URLs from the 
    ad_links = []
    for ad in ads:
        # parse the link from the ad
        link = ad.find_all("a", {"class": "title"})
        # add the link to the list
        for l in link:
            ad_links.append(BASE_URL[:-1] + l["href"])
    return ad_links

def get_context(url: str) -> None:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # get ad title
    try:
        title = soup.find("h1", class_=lambda cls: cls and 'title' in cls).text
    except AttributeError:
        
        title = None


    # get ad price
    try:
        # price = soup.find("span", attrs={"itemprop": "price"}).text
        price = soup.find("div", class_=lambda cls: cls and 'price' in cls).text
    except AttributeError:
        price = None

    # get date posted
    try:
        datetime_obj = soup.find("time")
        date_posted = datetime.fromisoformat(datetime_obj['datetime'][:-1])
    except (AttributeError, TypeError):
        date_posted = None

    # get ad description
    try:
        # description = soup.find("div", attrs={"itemprop": "description"}).text
        desc = soup.find("div", class_=lambda cls: cls and 'descriptionContainer' in cls)
        desc_html = desc.prettify()
        cleaned_text = re.sub('<.*?>', '', desc_html)
        description = re.sub(r'\n+\s+', '', cleaned_text)
    except AttributeError:
        description = None

    # get the ad city
    try:
        address = soup.find("span", attrs={"itemprop": "address"}).text
    except AttributeError:
        address = None
    # apend information to the dataframe
    result = {
        "title": title,
        "price": price,
        "description": description,
        "date_posted": date_posted,
        "address": address, 
        "url": url}
    return result
    


if __name__ == '__main__':
    df = pd.DataFrame(columns=["title", "price", "description", "date_posted", "address", "url"])
    long_term_list = []
    address = 'markham'
    url = get_original_url(address)
    long_term_list = get_links(url=url)
    for i in long_term_list[:10]:
        result = get_context(i)
        df = df.append(result, ignore_index=True)
    df.to_csv('kijiji_toronto_apartments.csv', index=False)