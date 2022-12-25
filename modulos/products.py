import sys, time, random
from flask_cors import cross_origin
from flask import request
from bson import ObjectId

from functions import jsonF, convertImageUrl, saveLog
from verifys import verify
import scrap

def initRouters(app, db):
	@app.route('/products/scrap', methods=['POST'])
	@cross_origin()
	def scrapProducts():
		try:
			body = request.json
			loja = body["loja"]
			lista = body["produtos"]
			config_bot = app.config["DRIVERS"][loja]
			objeto = verify(loja)
			response = 0
			for indice, item in enumerate(lista):
				print(' ', '{}/{}'.format(indice+1, len(lista)))
				if item['run'] == True:
					args = [ item['filtro'], item['produto'], item['categoria']]
					ress = scrap.bot(config_bot, args, objeto, db)
					response += ress[1]
					if ress[0] == None:
						time.sleep( random.randint(1, 3) )
					else:
						saveLog("log_{}".format(loja), ress[0])
						time.sleep( random.randint(2, 5) )
					#
				#
			#
			return { '_res': 'ok', 'data': '{} produtos atualizados!'.format(response) }
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			return { '_res': 'error', 'data': { 'erro': erro } }
		#
	#
	#
	#
	@app.route('/products/list', methods=['GET'])
	@cross_origin()
	def listProducts():
		try:
			colecao = db['products']
			all = colecao.find({})
			#
			array = []
			for itemp in all:
				itemp2 = jsonF(itemp)
				itemp2["image"]=convertImageUrl(itemp2["image"])
				array.append(itemp2)
			#
			return { '_res': 'ok', '_total': len(array), 'data': array }
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			return { '_res': 'error', 'data': { 'erro': erro } }
		#
	#
	#
	#
	@app.route('/products/getproduct/<id>', methods=['GET'])
	@cross_origin()
	def getproduct(id):
		try:
			#
			colecao = db['products']
			#
			res = colecao.find_one({ '_id': ObjectId(id) })
			if res == None:
				res = colecao.find_one({ '_id': id })
				if res == None:
					return { '_res': 'ok', 'data': 'product_not_found' }
				#
			#
			if res != None:
				res = jsonF(res)
				res['tipo']=0
				res["image"]=convertImageUrl(res["image"])
				return { '_res': 'ok', 'data': res }
			else:
				return { '_res': 'ok', 'data': 'product_not_found' }
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			return { '_res': 'error', 'data': { 'erro': erro } }
	#
	#
	#