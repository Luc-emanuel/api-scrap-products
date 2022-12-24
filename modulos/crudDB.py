#
from flask_cors import cross_origin
import sys
from flask import request
from functions import jsonF

def initRouters(app, client, db):
	@app.route('/teste', methods=['GET'])
	@cross_origin()
	def testeServer():
		try:
			#
			return { 'res': 'api tá on!!!' }
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			rest = { 'vlr': None }
			return { 'response': { 'erro': erro, 'res': rest } }
		#
	#
	#
	#
	@app.route('/listdb', methods=['GET'])
	@cross_origin()
	def listdb():
		try:
			#
			lista = client.list_databases()
			res = []
			for item in lista:
				item2 = jsonF(item)
				if item2['name'] != 'admin' and item2['name'] != 'local' and item2['name'] != 'config':
					res.append(item2)
			#
			return { 'res': res }
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			rest = { 'vlr': None }
			return { 'response': { 'erro': erro, 'res': rest } }
		#
	#
	#
	#
	@app.route('/drop', methods=['POST'])
	@cross_origin()
	def drop():
		try:
			#
			body = request.json
			name = body['name']
			tipo = body['type']
			res = ''
			if name != "":
				if tipo == 'db':
					client.drop_database(name)
					res = 'ok'
				elif tipo == 'col':
					db.drop_collection(name)
					res = 'ok'
				else:
					res = 'set_type'
			else:
				if tipo != 'db' or tipo != 'col':
					res = 'set_name_and_type'
				else:
					res = 'set_name'
			#
			return { 'res': res }
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			rest = { 'vlr': None }
			return { 'response': { 'erro': erro, 'res': rest } }
		#
	#
#
