#
from time import time

class verify():
	name = ""
	def __init__(self, name):
		self.name = name
	#
	def run(self, args):
		if self.name == "kabum":
			return self.kabum(args)
		else:
			print(" ", "function '{}' not found".format(self.name))
			return None
	#
	def kabum(self, args):
		html_, tagName_, url_, categoria = args
		produtos, parada, check = [], 0, []
		verificar = 1
		if tagName_[0] not in html_:
			verificar = 0
		#
		if verificar == 1:
			maxProds = int(html_.split(tagName_[1])[1].split('<b>')[1].split('</b>')[0])
			line2 = html_.split(tagName_[2])[1:]
			if len(line2) > 1:
				valors = [ len(ip) for ip in line2[:-1] ]
				valors.sort()
				line2[-1]=line2[-1][:int(valors[-1]*1.1)]
			#
			for indi, item in enumerate(line2):
				if tagName_[7][0] in item and tagName_[7][1] not in item and tagName_[7][2] not in item:
					image = item.split(tagName_[3])[1].split('title')[0].replace('"', '').replace(' ', '')
					link = item.split(tagName_[4])[0]
					titulo = item.split(tagName_[5])[1].split('<')[0]
					preco = item.split(tagName_[6])[1].split('<')[0].split('\xa0')[1].replace('.', '').replace(',', '.')
					produtos.append(
						{
							'status': 1,
							'titulo': titulo,
							'categoria': categoria,
							'preco': [[preco, time()]],
							'lastpreco': round(float(preco), 2),
							'loja': self.name,
							'link': '{}{}'.format(tagName_[8], link),
							'query': url_,
							'image': image,
							'create': time(),
							'update': time()
						}
					)
				else:
					check.append(item)
					parada = 1
				#
			#
		else:
			produtos = []
			maxProds = 0
			parada = 1
		#
		return produtos, parada, maxProds