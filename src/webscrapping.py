import requests
from bs4 import BeautifulSoup

class BS:

    def verificar_ultimo_heroi(url):
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        ids = soup.find_all('td')

        i = x = 0
        while i < len(ids):
            if x < int(ids[i].text):
                x = int(ids[i].text)
                i = i+2
            else:
                break
        return x 


