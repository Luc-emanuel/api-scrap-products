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
			return { '_res': 'api tá on!!!' }
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			return { '_res': 'error', 'data': { 'erro': erro } }
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
			return { '_res': 'ok', 'data': res }
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			return { '_res': 'error', 'data': { 'erro': erro } }
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
			data = ''
			if name != "":
				if tipo == 'db':
					client.drop_database(name)
					data = 'ok'
				elif tipo == 'col':
					db.drop_collection(name)
					data = 'ok'
				else:
					data = 'set_type'
			else:
				if tipo != 'db' or tipo != 'col':
					data = 'set_name_and_type'
				else:
					data = 'set_name'
			#
			return { '_res': 'ok', 'data': data }
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			tb = exc_tb.tb_lineno
			erro = { 'exc_tipo': str(exc_type), 'exc_objeto': str(exc_obj), 'objeto': str(exc_tb), 'linha': int(tb) }
			return { '_res': 'error', 'data': { 'erro': erro } }
		#
	#
#
