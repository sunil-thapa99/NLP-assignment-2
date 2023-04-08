import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import requests
# Path: scrap/scrap_selenium.py
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


BASE_URL = 'https://www.kijiji.ca/'

start_page = 1

def get_original_url(address: str, sorting: str=None, page_num: int=1) -> str:
    if sorting:
        if 'low' in sorting or 'asc' in sorting:
            sorting = 'priceAsc'
        elif 'high' in sorting or 'desc' in sorting:
            sorting = 'priceDesc'
        room_and_rental_term_url = BASE_URL + f'b-for-rent/city-of-toronto/{address}/page-{page_num}/k0c30349001l1700273?sort={sorting}'
    else:
        room_and_rental_term_url = BASE_URL + f'b-for-rent/city-of-toronto/{address}/page-{page_num}/k0c30349001l1700273'
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

def get_context(soup) -> None:
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
  

# scrap kijiji rents
def scrap_kijiji_rents(driver, link):
    # Path: scrap/scrap_selenium.py
    driver.get(link)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    return get_context(soup)

if __name__ == '__main__':
    df = pd.DataFrame(columns=["title", "price", "description", "date_posted", "address", "url"])
    long_term_list = []
    address = ['brampton', 'mississauga', 'don mills', 'Toronto', 'Ajax', 'scarborough', 'north york', 'markham',
               'vaughan', 'vancouver', 'winnipeg', 'east york', 'calgary',
               'edmonton', 'montreal', 'ottawa', 'quebec city', 'saskatoon', 'regina', 'halifax', 'st. johns']
    for i in range(0, len(address)):
        for j in range(1,10):
            url = get_original_url(address[i], page_num=j)
            links = get_links(url=url)
            long_term_list.extend(links)
            print(len(links), address[i])
    print(len(long_term_list))
    # print(long_term_list, len(long_term_list))
    # url = get_original_url(address)
    # long_term_list = get_links(url=url)
    # chr_options = Options()
    # chr_options.add_experimental_option("detach", True)
    # driver = webdriver.Chrome(executable_path="/Users/sunilthapa/Desktop/AIMT/AML 2304/assignment-2/actions/chromedriver_mac_arm64/chromedriver", options=chr_options)
    # print('-----------')
    # for i in long_term_list:
    #     result = scrap_kijiji_rents(driver, i)
    #     # result = get_context(i)
    #     df = df.append(result, ignore_index=True)
    #     time.sleep(2)
    # df.to_csv('kijiji_toronto_apartments.csv', index=False)
