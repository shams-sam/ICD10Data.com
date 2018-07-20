
# coding: utf-8

# # Imports

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm_notebook as tqdm
from urllib.request import urlopen
from urllib import request
import re
import sys


# # Site Configuration

# In[2]:


ROOT_URL = 'http://www.icd10data.com'
BASE_URL = 'http://www.icd10data.com/ICD10CM/Codes'


# # Utility Functions

# In[3]:


def build_request(url, header):
    req = request.Request(url,headers=header)
    return req


# In[40]:


def get_page(url):
    page = urlopen(url, timeout=10)
    page = page.read()
    return page


# In[23]:


def get_page_soup(page):
    page = BeautifulSoup(page, 'html.parser')
    return page


# In[5]:


def get_links(page):
    list_texts_l1 = []
    list_hrefs_l1 = []
    list_texts_l2 = []
    list_hrefs_l2 = []
    count = 0
    for _ in page.find_all('a', attrs={'class':'identifier'}):
        text = _.get_text()
        href = _.get_attribute_list('href')[0]
        count += 1
        if len(re.findall('\/', href)) == 3:
            list_texts_l1.append(text)
            list_hrefs_l1.append(href)
        else:
            list_texts_l2.append(text)
            list_hrefs_l2.append(href)
    assert len(list_texts_l1) == len(list_hrefs_l1)
    assert len(list_texts_l2) == len(list_hrefs_l2)
    assert len(list_texts_l1) + len(list_texts_l2) == count
    return (
        pd.DataFrame({'text': list_texts_l1, 'href': list_hrefs_l1}),
        pd.DataFrame({'text': list_texts_l2, 'href': list_hrefs_l2}),
    )

import _pickle as pkl
l4 = pd.read_csv('level_4_links.csv')


# In[35]:


l4_pages = {}
for url in l4.href.tolist():
    l4_pages[url] = False
def count():
    count = 0
    for key, value in l4_pages.items():
        if value == False:
            count += 1
    return count


# In[ ]:

if __name__ == "__main__":
    print(sys.argv)
# while count() > 0:
#     c = count()
#     print(c)
#     for url in tqdm(l4_pages, total=len(l4_pages)):
#         if not l4_pages[url]:
#             link = ROOT_URL + url
#             page = get_page(link)
#             html = 'html' in str(page)
#             if html:
#                 l4_pages[url]=html
#                 pkl.dump(page, open('./bs4_l4_dump/' + url.replace("/", "_") + ".pkl", "wb"))

