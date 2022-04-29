import lxml
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

start_script = datetime.now()

HEADERS = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}

alphabet = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'

def genering_links():
    links = {}
    for i in alphabet:
        URL = f'https://slova.com.ua/letter/{i}/page/'
        links[i] = URL
    return links

def get_content():
    dict_links = genering_links()
    words =[]
    for i in alphabet:
        j = 1
        while True:
            response = requests.get(dict_links[i] + str(j), headers=HEADERS)
            if response:
                soup = BeautifulSoup(response.text, 'lxml')
                lin = soup.find_all('div', class_='col-lg-3 col-xs-6 col-sm-4 wordLink')
                for l in lin:
                    words.append(l.get_text())
            else:
                break
            print('Scraping letter', i.capitalize(), 'page number', j)
            j += 1
    return words

def get_save_data():
    words_list = get_content()
    with open('ukrain_word_dict.json', 'w') as file:
        json.dump(words_list, file)
get_save_data()
print(len(get_content()))
print('Time work', datetime.now() - start_script)