import re
import lxml
import requests
from datetime import datetime
from bs4 import BeautifulSoup

start_script = datetime.now()

URL = 'http://hrinchenko.com/alfavit.html'
HEADERS = {'user-agent':'Mozilla/5.0 \
    (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'accept':'*/*'}

def get_requests(Url):
    response = requests.get(url=Url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_list_of_letters():
    soup = get_requests(URL)
    list_of_letters = soup.find('div', class_='list_of_letters').find_all('a')
    link_of_letters = []
    for list in list_of_letters:
        link_of_letters.append(URL.rpartition('/')[0] + list.get('href'))
    return link_of_letters

def get_words():
    links = get_list_of_letters()
    words = []
    for link in links[5:6]:
        soup = get_requests(link)
        pagination = soup.find('div', class_='list_pagination')
        if pagination:
            len_pagination = len(pagination.find_all('a'))
            for k in range(1, len_pagination+1):
                lin = re.sub(r'\d', str(k), link)
                soup2 = get_requests(lin)
                word = soup2.find('table', class_='list_of_words').find_all('a')
                letter = word[0].get_text()[0]
                for v in word:
                    words.append(v.get_text())
                print('scraping letter', letter, 'page', re.sub(r'\D', '', lin))
        elif not pagination:
            word = soup.find('table', class_='list_of_words').find_all('a')
            letter = word[0].get_text()[0]
            for j in word:
                words.append(j.get_text())
            print('scraping page', re.sub(r'\D', '', link), 'letter', letter)
    return words


get_words()
print('Time worked', datetime.now() - start_script)