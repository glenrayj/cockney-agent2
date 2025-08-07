from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
# Allow your domains (add both naked + www)
CORS(app, resources={
    r"/api/*": {"origins": ["https://bencockney.rocks", "https://www.bencockney.rocks"]}
})
# For quick testing you can do: CORS(app)  # but tighten later

# Load base map
with open("cockney_slang.json", "r") as f:
    cockney_dict = json.load(f)

# Try to load variants if you built them
try:
    with open("cockney_slang_variants.json", "r") as f:
        cockney_variants = json.load(f)
except FileNotFoundError:
    cockney_variants = {k: [v] for k, v in cockney_dict.items()}

@app.route("/api/slang")
def get_slang():
    return jsonify(cockney_dict)

@app.route("/api/slang_variants")
def get_slang_variants():
    return jsonify(cockney_variants)

@app.route("/health")
def health():
    return {"ok": True, "entries": len(cockney_dict), "variants": len(cockney_variants)}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)