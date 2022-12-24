#
import os, sys, certifi, time, random
#
pathAtual = os.getcwd()
sys.path.insert(1,  '{}\\modulos'.format(pathAtual) )
sys.path.insert(1,  '{}\\utils'.format(pathAtual) )

#
from flask import Flask
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
#
from functions import abrirJson, saveLog
from verifys import verify
import drivers
import scrap

import crudDB
import products

#
env = abrirJson('./configs/env')
STRING = env['string'].replace('<user>', env['user']).replace('<password>', env['pass']).replace('<dbname>', env['dbname'])
client = MongoClient(STRING, tlsCAFile=certifi.where())
db = client.get_database(env['dbname'])

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS']='Content-Type'
app.config['DRIVERS']=drivers.lista.copy()

@app.errorhandler(404)
@cross_origin()
def not_found(e):
	return { 'res': 'route_not_found' }

crudDB.initRouters(app, client, db)
products.initRouters(app, db)

if '__main__' == __name__:
	app.run(debug=True)
