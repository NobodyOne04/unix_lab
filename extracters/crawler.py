from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import os
#from user_agent import generate_user_agent
import time

films = list()

numb = 1

dirName = 'data'
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")
for page in range(1, 100000):
    page += 1
    
    string_page = '0'*(7 - len(str(page)))+str(page)
    url = f'https://www.imdb.com/title/tt'+string_page
    try:
        html = urlopen(url)
    except:
        continue
    #data = requests.get(url)
    #print(data.text)

    #
    bs = BeautifulSoup(html.read(), 'html.parser')

    div = bs.find('div', {'class': 'redesign'})
    with open(f"data/{numb}.txt", "w", encoding = "utf-8") as f:
       f.write(str(div))
    numb += 1
    #title = div.h1.text
    #print(page, title)
    
    #films.append({'title': title})
    
