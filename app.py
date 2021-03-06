# -*- coding: utf-8 -*-
from flask import  Flask, render_template, jsonify, redirect
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import json

app = Flask(__name__)

#MongoDB client and db, change it to add data in your own db.
client = MongoClient('localhost')
db = client['pangaea']



# Convert MongoDB to JSON
def to_json(data):
    return dumps(data)


@app.route('/')
def index():
    greenhouses = db.greenhouse.find()
    greenhouses_list = list(greenhouses)
    houses = dumps(greenhouses_list)
    return render_template('index.html', houses = greenhouses_list)

#Add thing to db as W3C standardisation of a thing with a revised description for a thing in a greenhouse.
@app.route('/add')
def add_to_db():
    
    add_desc = {
    			"@context": ["https://155.4.72.38:5000/karlskrona/bth/vilan"],
    			"@type": ["vaxthus"],
    			"name": "Vilan",
    			"city": "Karlskrona",
    			"location": "BTH",
    			"interaction": [{
        			"@type": [{
                  			"humiditysensor": "True"
                  			}],
        			"name": "status",
        			"schema": {"type": "string"},
        			"writable": False,
        			"observable": True,
        			"form": [{
            				"href": "https://155.4.72.38:5000/karlskrona/bth/vilan/status",
            				"mediaType": "application/json"
        				}]
    				}]
			}
    result = db.greenhouse.insert(add_desc)
    return "added"

#show thing collection as Json
@app.route('/things/', methods=['GET'])
def get_thing():
	# Get the thing collection
    things_collection = db.greenhouse.find()
    # Create JSON-data from collection via a Python list
    things_list = list(things_collection)
    things = dumps(things_list)
    return things

#show city with greenhouses
@app.route('/<city>/', methods=['GET'])
def get_city(city):
    city = db.greenhouse.find({"city": city})
    if city.count() <= 0:
        return "No city found"

    city_list = list(city)
    cityData = dumps(city_list)
    return render_template('vaxthus.html', cityData = city_list)

#show a specific grenhouse´s name, location and city where it is located
@app.route('/<city>/<location>/<name>/', methods=['GET'])
def get_url(city, location, name):
    url = db.greenhouse.find({"$and": [{"city": city, "location": location, "name": name}]})
    if url.count() <= 0:
        return render_template('vaxthusFalse.html')

    url_list = list(url)
    urlData = dumps(url_list)
    return render_template('vaxthusTrue.html', urlData = url_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
