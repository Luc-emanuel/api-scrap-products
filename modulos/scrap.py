import os, sys, time
from functions import getHTML, convert, clear, saveProducts

def bot(config, argumentos, verif, database):
	headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0' }
	tags = config["tags"]
	page = config["page"]
	pageSize = config["pageSize"]
	filtro = config["filtro"]
	urlBase = config["urlBase"]
	#
	filter = argumentos[0]
	categoria = argumentos[2]
	busca = argumentos[1]
	pageMaximo = page+1
	#
	founds = []
	erro = None
	response = 0
	while 1:
		try:
			if page > pageMaximo:
				break
			#
			url = urlBase.format(
				busca,
				page,
				pageSize,
				filtro[filter]
			)
			print(' ', url)
			#
			html, htmlSAVE = getHTML(url, headers)
			if "enable JS" in html:
				print("ERROR", len(html))
				time.sleep(5)
			else:
				res = verif.run([html, tags, url, categoria])
				if res == None:
					break
				else:
					produtos, parada, maxProds = res
					if parada == 1 and len(produtos) <= 0:
						break
					else:
						if len(produtos) > 0:
							#
							founds += produtos
							#
							lenP = len(produtos)
							lenFounds = len(founds)
							#
							pageMaximo = int(str(maxProds/pageSize).split('.')[0])+1
							#
							diffs = maxProds - lenFounds
							#
							print(' ', '{}/{} - {} - {}/{}/{} - {}'.format(
								page,
								pageMaximo,
								convert(time.time()),
								lenP,
								lenFounds,
								maxProds,
								diffs
								)
							)
							#
							produtos = clear(produtos, busca)
							if len(produtos) > 0:
								saves = saveProducts(produtos, database)
								response += saves
							print('')
							#
							time.sleep(1)
							page += 1
						else:
							break
						#
					#
				#
			#
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			break
		#
	#
	return [erro, response]
#