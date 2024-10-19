from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up MongoDB connection
client = MongoClient("mongodb+srv://imshu1:imshu1@cluster0.cagck.mongodb.net/")
db = client.dashboard_db  # Database
collection = db.insights  # Collection

@app.route('/load-data',methods=['GET'])
def load_data():
    try:
        # Load JSON file
        with open('data/jsondata.json', 'r') as file:
            data = json.load(file)

        # Insert data into MongoDB collection
        collection.insert_many(data)

        return jsonify({'message': 'Data loaded successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API route to get all data
@app.route('/api/data', methods=['GET'])
def get_all_data():
    try:
        # Fetch all data from MongoDB
        data = list(collection.find({}, {"_id": 0}))  # Avoid returning MongoDB _id field
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

