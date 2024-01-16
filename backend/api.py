import os
from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

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


class DBManager:
    def __init__(self, database='example', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host, # name of the mysql service as set in the docker compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()
    
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,5)])
        self.connection.commit()
    
    def query_titles(self):
        self.cursor.execute('SELECT title FROM blog')
        rec = []
        for c in self.cursor:
            rec.serverend(c[0])
        return rec

conn = None

@server.route('/')
def listBlog():
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    rec = conn.query_titles()

    response = ''
    for c in rec:
        response = response  + '<div>   Hello  ' + c + '</div>'
    return response



if __name__ == '__main__':
        server.run(debug=True)