import requests
from bs4 import BeautifulSoup

URL = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
r = requests.get(URL)

soup = BeautifulSoup(r.text, 'html.parser')

number = soup.find('td', class_='titleColumn').contents[0]#.strip()
film_name = soup.find('td', class_='titleColumn').find('a').text
year = soup.find('td', class_='titleColumn').find('span', class_='secondaryInfo').text
rate = soup.find('td', class_='ratingColumn imdbRating').text.strip()
link = 'https://www.imdb.com/'+soup.find('td', class_='titleColumn').find('a').get('href')

films = soup.findAll('td', class_='titleColumn')
rates = soup.findAll('td', class_='ratingColumn imdbRating')

top250_IMDB = []

for i, j in zip(films, rates):
    number = i.contents[0].strip()
    film_name = i.find('a').text
    year = i.find('span', class_='secondaryInfo').text
    rate = f'Рейтинг-{j.text.strip()}'
    link = 'https://www.imdb.com/'+ i.find('a').get('href')
    top250_IMDB.append([number, film_name, year, rate, link])

#print(top250_IMDB)














