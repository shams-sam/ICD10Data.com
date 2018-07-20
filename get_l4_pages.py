from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from urllib.request import urlopen
from urllib import request
import re

ROOT_URL = 'http://www.icd10data.com'
BASE_URL = 'http://www.icd10data.com/ICD10CM/Codes'

def get_page_soup(url):
    page = urlopen(url)
    page = page.read()
    page = BeautifulSoup(page, 'html.parser')
    return page

l4 = pd.read_csv('./level_4_links.csv')

l4_pages = {}
for url in l4.href.tolist():
    l4_pages[url] = {'page': None, 'html':False}
def count():
    count = 0
    for key, value in l4_pages.items():
        if value['html'] == False:
            count += 1
    return count

c = 0
while count() > 0:
    print(count())
    for url in tqdm(l4_pages, total=len(l4_pages)):
        c += 1
        if c == 5:
            break
        if not l4_pages[url]['html']:
            link = ROOT_URL + url
            page = get_page_soup(link)
            html = 'html' in page
            l4_pages[url]['page']=page
            l4_pages[url]['html']=html
    break
          
import _pickle as pkl
pkl.dump(l4_pages, open('l4_pages.dump.pkl', 'wb'))