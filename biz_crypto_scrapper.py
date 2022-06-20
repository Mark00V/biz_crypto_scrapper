import requests
from bs4 import BeautifulSoup                       # To quickly search thread links
from urllib.parse import urlparse, urljoin
import time
import random
from selenium import webdriver                      # Because BS4 does not get thread links (there is probably an easier way...)
from selenium.webdriver.common.by import By
from tqdm import tqdm

#==========================================
# Global variables
"""set words to search for"""
list_searchwords = ["rvp","rose","mtv","xmr","europe ban","germany ban", "ban crypto"]
#==========================================


def randwait(): # For bots
    return(random.uniform(0.02,0.06))


def geturls_biz():
    url_list = []
    driver = webdriver.Firefox()
    driver.get(url)
    all_threads = driver.find_elements(By.CLASS_NAME,"thread")

    for element in all_threads:
        link_text = element.get_attribute("id")
        if len(link_text) > 14:
            url_list.append("https://boards.4channel.org/biz/thread/"+link_text.split("-")[1])
        else:
            continue
    driver.quit()
    return(url_list)


def list_in_list(search_in_str,list_searchwords): # Falls eines der Wörter aus der Liste list_searchwords in search_in_list vorkommt: return true
    for searchword in list_searchwords:
        if searchword in search_in_str.lower():
            return True
            break

    return False


def searchthread(url):
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    messages = soup.select("blockquote.postMessage")
    allmessages_str = "--------------------\n"
    allmessages_found_list = []
    for message in messages:
        allmessages_str += message.text+"\n--------------------\n"
        if list_in_list(message.text,list_searchwords):
            allmessages_found_list.append(message.text)
    return allmessages_found_list,allmessages_str


def searchallthreads(threadlist):
    allmessages_allthreads = []
    for url in tqdm(threadlist,total=len(threadlist),unit="threads"):
        allmessages_found_list,allmessages_str = searchthread(url)
        if allmessages_found_list: allmessages_allthreads.append(allmessages_found_list) # only append non-empty lists
    
    return allmessages_allthreads


def main():
    print("====================================")
    print("=== B  I  Z  C  R  A  W  L  E  R ===")
    print("====================================\n")
    print("Webdriver: Getting all biz threads...")
    allthreads = geturls_biz()
    print(len(allthreads),"threads found.")
    print("Scrapping all threads for keywords...")
    print("")
    allmessages_allthreads = searchallthreads(allthreads)
    print("------------------------------------")
    print("Found keywords in", len(allmessages_allthreads),"threads:")
    for message in allmessages_allthreads:
        print("------------------------------------")
        print(message,"\n")
    print("------------------------------------")

    
main()

if __name__ == '__main__':
    main()
