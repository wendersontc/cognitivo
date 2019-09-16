from flask import Flask
from flask_restful import Resource, Api
import csv
import json
from datetime import datetime
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from models.store import Store
from models.identify import Identify
from utils.encoder import Encoder

# Instantiate the app
app = Flask(__name__)
api = Api(app)

connection = psycopg2.connect("user='postgres' host='db' password='postgres'")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS identify')
cursor.execute('DROP DATABASE IF EXISTS db')
cursor.execute("CREATE DATABASE db")
cursor.execute("CREATE TABLE IF NOT EXISTS identify (id int primary key, name varchar, rating_amount int, size int, currency varchar, genre varchar)")


class NewsResource(Resource):
    def get(self):
        genres = ['News']
        apps = []

        with open('./csv/AppleStore.csv') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                apps.append(Store(row))

        filteredGenres = list(filter(lambda x: x.genre in genres, apps))
        filteredGenres.sort(key=lambda x: x.rating_amount, reverse=True)

        identifys = []

        for filtered in filteredGenres[:1]:
            identifys.append(Identify(filtered.id, filtered.name, filtered.rating_amount,
                                      filtered.size, filtered.currency, filtered.genre))

        return json.dumps(identifys, cls=Encoder)


class MusicBookResource(Resource):
    def get(self):
        genres = ['Book', 'Music']
        apps = []

        with open('./csv/AppleStore.csv') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                apps.append(Store(row))

        filteredGenres = list(filter(lambda x: x.genre in genres, apps))
        filteredGenres.sort(key=lambda x: x.rating_amount, reverse=True)

        identifys = []

        for filtered in filteredGenres[:10]:
            identifys.append(Identify(filtered.id, filtered.name, filtered.rating_amount,
                                      filtered.size, filtered.currency, filtered.genre))

        csv.register_dialect('myDialect', delimiter='|',
                             quoting=csv.QUOTE_NONE, quotechar='')
        titles = ['id', 'name', 'rating_amount', 'size', 'currency', 'genre']
        myFile = open('./csv/Identify.csv', 'w')
        sql = "INSERT INTO identify (id, name, rating_amount, size, currency, genre) VALUES (%s, %s, %s, %s, %s, %s)"
        with myFile:
            writer = csv.writer(myFile, dialect='myDialect')
            writer.writerow(titles)
            for s in identifys:
                writer.writerow([s.id, s.track_name, s.n_citacoes,
                                 s.size_bytes, s.price, s.prime_genre])
                cursor.execute(sql, (s.id, s.track_name, s.n_citacoes,
                                     s.size_bytes, s.price, s.prime_genre))

        return json.dumps(identifys, cls=Encoder)


class MusicBookQuotesResource(Resource):
    def get(self):
        genres = ['Book', 'Music']
        apps = []

        cursor.execute("SELECT * FROM identify")
        myresult = cursor.fetchall()

        filteredGenres = list(filter(lambda x: x[5] in genres, myresult))
        filteredGenres.sort(key=lambda x: x[2], reverse=True)

        identifys = []

        for filtered in filteredGenres[:1]:
            identifys.append(filtered)

        serialized = json.dumps(identifys, cls=Encoder)

        return serialized


# Create routes
api.add_resource(NewsResource, '/news/avaliations/')
api.add_resource(MusicBookResource, '/book/music/avaliations/')
api.add_resource(MusicBookQuotesResource, '/book/music/quotes')


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
