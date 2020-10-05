from urllib.request import Request, urlopen
from http.client import IncompleteRead
from urllib.error import HTTPError
import sys
from bs4 import BeautifulSoup as soup
from cleantext import clean
import pandas as pd
import json

persons = []

num = 1
userid = 1
for webpage in range(1,5):

	if webpage == 1: 
		url = "https://www.99.co/id/directory/"
	else:
		url = "https://www.99.co/id/directory/agent?page="+str(webpage)

	try:
		req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
	except IncompleteRead:
		print('IncompleteRead coba lagi...')
		continue
	try:
		page_soup = soup(webpage, "html.parser")
	except AttributeError as e:
		print('AttributeError coba lagi...')
		continue
	listgroup = page_soup.find_all('div', class_='agent-card')
	for person in listgroup:
		"""
		phone1 = clean(getattr(person.find('li', class_='contact telephone'), 'text', None))
		phone2 = clean(getattr(person.find('li', class_='contact telephone2'), 'text', None))
		
		phone = {
			"phone1": phone1,
			"phone2": phone2
		}
		"""
		phones = person.find('div', class_='col-xs-7')

		phone = []
		for a in phones.find_all('li'):
			phone2 = clean(getattr(a, 'text', None))
			phone.append({"phone":phone2})


		fullname = clean(getattr(person.find('h3', class_='agent-card__name'), 'text', None))
		company = clean(getattr(person.find('h5', class_='agent-card__company'), 'text', None))
		verified = person.find('span', class_='verified')
		if verified is not None and 'title' in verified.attrs:
			verified = verified.get('title')
		#verified = verifiedq.get('title', Null)
		#verified = verifiedw.get('title', '')
		areas = person.find('div', class_='agent-card__area-specialization')

		area = []
		for r in areas.find_all('li'):
			area.append({"area":r.text})

		infos = person.find('ul', class_='agent-card__info')
		info = []
		for s in infos.find_all('li'):
			jml = clean(getattr(s.find('h5'), 'text', None))
			key = clean(getattr(s.find('p'), 'text', None))
			info.append({key:jml})
		#print(info)


		photo = person.find('img', itemprop='image')
		
		#print(phone)
		#print(fullname)
		#print(compny)
		#print(photo.get("src"))

		persons.append({
			"userid": userid,
			"page": num,
			"fullname": fullname,
			"phone": phone,
			"verified": verified,
			"company": company,
			"areas": area,
			"info": info,
			"photo": photo.get("src")
		})
		userid = userid+1
		print(persons)
	num = num+1

with open("99co.json", "a") as data:
	data.write(json.dumps(persons))
	data.close()