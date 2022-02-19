from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import json
import time


def obtener_titulos(urls):
	"""Obtiene todos los titulos de las peliculas."""
	global contador_titulos
	for url in urls:
		request = requests.get(url)
		soup = bs(request.text, 'lxml')
		titulos_por_pagina = soup.find_all('a', class_='browse-movie-title')
		for titulo in titulos_por_pagina:
			titulos[contador_titulos] = {'titulo': titulo.get_text()}
			print(contador_titulos)
			contador_titulos += 1


def obtener_datos(url):
	"""Obtiene y almacena los datos de una pelicula en el diccionario peliculas."""
	global contador_peliculas
	time.sleep(3)
	driver.get(url)
	soup = bs(driver.page_source, 'lxml')
	info = soup.find('div', id='movie-info')
	try:
		titulo = info.h1.string
		comentarios = [comentario.p.text.replace('"', "'") for comentario in soup.find_all('div', class_='comment-text')]
		anio = info.h2
		generos = anio.find_next_sibling('h2').string.split(' / ')
		director = soup.find('div', class_='directors').find('span', {'itemprop': 'name'}).get_text()
		elenco = [miembro.get_text() for miembro in soup.find_all('span', {'itemprop': 'actor'})]
		likes = info.find('span', id='movie-likes').string
		rating_imdb = info.find('span', {'itemprop': 'ratingValue'}).string
		sinopsis = soup.find('div', id='synopsis').p.string
		peliculas[contador_peliculas] = {'titulo': titulo, 'anio': anio.get_text(), 'generos': generos, 'director': director, 'elenco': elenco, 'sinopsis': sinopsis.replace('"', "'"), 'likes': int(likes), 'rating': float(rating_imdb), 'comentarios': comentarios}
		print(contador_peliculas)
		contador_peliculas += 1
	except:
		print('Error')
		pass
	

def obtener_enlaces(url):
	"""Obtiene los enlances de cada pelicula en la pagina actual."""
	request = requests.get(url)
	soup = bs(request.text, 'lxml')
	enlaces = soup.find_all('a', class_='browse-movie-link')
	for enlace in enlaces:
		link = enlace['href']
		obtener_datos(link)


# Crea una lista de urls hasta el segundo parametro excluido dado a range
urls = ['https://yts.mx/browse-movies?page={}'.format(str(i)) for i in range(1,1960)]


# Uso de webdriver PhantomJS para lograr obtener contenido cargado con JS
driver = webdriver.PhantomJS()

titulos = {}
contador_titulos = 0

peliculas = {}
contador_peliculas = 0

obtener_titulos(urls)

# Almaceno los titulos de cada pelicula en un documento json
with open('titulos.json', 'w', encoding='utf8') as file:
	json.dump(titulos, file, ensure_ascii=False)
	file.close()

for url in urls:
	obtener_enlaces(url)

# Almaceno los datos obtenidos de cada pelicula en un documento json
with open('metadata2.json', 'w', encoding='utf8') as file:
	json.dump(peliculas, file, ensure_ascii=False)
	file.close()

