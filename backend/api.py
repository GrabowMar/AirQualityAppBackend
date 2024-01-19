import os
import time
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from dbmanager import DBManager

server = Flask(__name__)
CORS(server)

@server.route('/api/time')
def get_current_time():
        return jsonify({'time': time.time()})

@server.route('/api/gios-data')
def get_gios_data():
        try:
                response = requests.get('https://api.gios.gov.pl/pjp-api/rest/station/findAll')
                response.raise_for_status()
                data = response.json()
                return jsonify(data)
        except requests.RequestException as e:
                return jsonify({'error': str(e)}), 500

@server.route('/api/air-quality-index/<int:stationId>')
def get_air_quality_index(stationId):
        try:
                response = requests.get(f'https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{stationId}')
                response.raise_for_status()
                data = response.json()
                return jsonify(data)
        except requests.RequestException as e:
                return jsonify({'error': str(e)}), 500

@server.route('/')
def listBlog():
    global conn
    if not conn:
        conn = DBManager()
        conn.populate_db()
    rec = conn.query_titles()

    response = ''
    for c in rec:
        response = response  + '<div>   Hello  ' + c + '</div>'
    return response

if __name__ == '__main__':
        server.run(debug=True)