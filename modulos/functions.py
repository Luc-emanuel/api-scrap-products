import io, json, time, sys
from datetime import datetime, timedelta
from pymongo import MongoClient
import requests as reqs
from colorama import Fore, Back, Style, init

init()

def gravarJson(path, dicio):
	if '.json' not in path:
		path = path + '.json'
	else:
		pass
	with io.open(path, "w", encoding='utf-8') as outfile:
		json.dump(dicio, outfile, indent=4, ensure_ascii=False, sort_keys=False)
	outfile.close()

def abrirJson(path):
	try:
		if '.json' not in path:
			path = path + '.json'
		else:
			pass
		with io.open(path, 'r', encoding='utf-8') as outfile:
			dicionario = json.load(outfile)
		outfile.close()
		return dicionario
	except:
		return {}

def clear(array, query_):
	array2, queryS = [], query_.split('-')
	for iten in array:
		title = iten['titulo'].lower().replace(" ", "")
		cont = 0
		for que in queryS:
			if que in title:
				cont += 1
		if cont == len(queryS):
			array2.append(
				{
					'status': iten['status'],
					'titulo': iten['titulo'],
					'categoria': iten['categoria'],
					'preco': iten['preco'],
					'lastpreco': round(float(iten['preco'][-1][0]), 2),
					'loja': iten['loja'],
					'link': iten['link'],
					'query': iten['query'],
					'image': iten['image'],
					'create': iten['create'],
					'update': iten['update']
				}
			)
	return array2

def updateArray(array, arrayDB):
	drop = 0
	for item in array:
		itemLink, control = item['link'], 0
		for item2 in arrayDB:
			if itemLink == item2['link']:
				last = round(float(item2['preco'][-1][0]), 2)
				atual = round(float(item['preco'][-1][0]), 2)
				diff = abs(atual-last)
				if diff >= 1:
					item2['preco'].append(item['preco'][-1])
					item2['lastpreco']=round(float(item['preco'][-1][0]), 2)
					item2['update']=time.time()
					drop += 1
				control = 1
				break
		if control == 0:
			arrayDB.append(item)
			drop += 1
		#
	return arrayDB, drop

def jsonF(file):
	dcc = {}
	for uc in file:
		if uc == "_id":
			dcc[str(uc)]=str(file[uc])
		else:
			dcc[str(uc)]=file[uc]
	return dcc

def convertImageUrl(urlImage):
	try:
		b = urlImage.split(".")[0]+"9"
		c = urlImage.split("images")[-1]
		d = c.split(".")
		e = d[-2][:-1]+"g"
		d = b+'.'.join(d[:-2])+"."+e+"."+d[-1]
		return d
	except:
		return urlImage

def convert(tempo, dt=0):
	a = datetime.fromtimestamp(tempo)
	b = 0
	if dt == 1:
		b = str(a - timedelta(hours=3))
	else:
		b = str(a)
	data, hora = b.split(' ')
	ano, mes, dia = data.split('-')
	hora, minuto, segundo = hora.split(':')
	segundo = segundo.split('.')[0]
	b = '{0}-{1}-{2} {3}:{4}:{5}'.format( dia, mes, ano, hora, minuto, segundo )
	return b

def get(filename):
	file = open(filename, "r", encoding="utf-8")
	lista = [ item.replace("\n", "") for item in file ]
	file.close()
	return lista

def save(filename, string, type="w"):
	with open(filename, type, encoding='utf-8') as file:
		file.write(string)
	file.close()

def getHTML(url, cabecalho):
	res = reqs.get(url, headers=cabecalho)
	html = res.text
	return str(html.replace("\n", "")), html

def saveProducts(array, database):
	#
	colecao = database['products']
	all = colecao.find({})
	lista = []
	for item in all:
		lista.append(jsonF(item))
	#
	newProdutos, drop_ = updateArray(array, lista)
	#
	if drop_ > 0:
		print(' ', Fore.GREEN+'{} produtos atualizados'.format(drop_)+Style.RESET_ALL)
		database.drop_collection('products')
		colecao = database['products']
		colecao.insert_many(newProdutos)
		return drop_
	else:
		print(' ', Fore.CYAN+'sem atualizações'+Style.RESET_ALL)
		return 0

def saveLog(nameFile, error):
	save("./logs/"+nameFile+".txt", "{} -- {}\n".format(convert(time.time()), error), type="a")
