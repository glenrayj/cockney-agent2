from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load the slang dictionary
with open("cockney_slang.json", "r") as f:
    cockney_dict = json.load(f)

@app.route("/api/slang")
def get_slang():
    return jsonify(cockney_dict)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)