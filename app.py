from flask import  Flask, render_template, jsonify, redirect
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient('localhost')
db = client['pangaea']

# Convert MongoDB to JSON
def to_json(data):
    return dumps(data)

@app.route('/')
def index():
    greenhouses = db.greenhous.find()
    greenhouses_list = list(greenhouses)
    houses = dumps(greenhouses_list)
    return render_template('index.html', houses = greenhouses_list)

#Add thing to db as W3C standard
@app.route('/add')
def add_to_db():

        initial_things = {
    			"@context": ["https://tillsammansodling/karlshamn/bth/gaia"],
    			"@type": ["vaxthus"],
    			"name": "gaia",
    			"city": "Karlshamn",
    			"location": "bth",
    			"interaction": [{
        			"@type": [{"lightsensor": "1",
                  			"humiditysensor": "2",
                  			"moisturesensor": "3"}],
        			"name": "status",
        			"schema": {"type": "string"},
        			"writable": False,
        			"observable": True,
        			"form": [{
            				"href": "tillsammansodling/karlshamn/gaia/status",
            				"mediaType": "application/json"
        				}]
    				}]
			}
        result = db.greenhous.insert_one(initial_things)
        #print result.inserted_ids
	return "added"

#show thing collection as Json
@app.route('/things/', methods=['GET'])
def get_thing():
	# Get the thing collection
        things_collection = db.greenhous.find()
    # Create JSON-data from collection via a Python list
        things_list = list(things_collection)
        things = dumps(things_list)
        return things


if __name__ == '__main__':
    app.run(host='0.0.0.0')