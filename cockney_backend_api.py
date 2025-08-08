from flask import Flask, jsonify, request
from flask_cors import CORS
import json, os

app = Flask(__name__)

# Allow your domains (naked + www)
CORS(
    app,
    resources={r"/api/*": {"origins": ["https://bencockney.rocks", "https://www.bencockney.rocks"]}},
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/api/slang_base")
def slang_base():
    return jsonify(load_json("cockney_slang.json"))

@app.route("/api/slang_index")
def slang_index():
    return jsonify(load_json("cockney_slang_index.json"))

@app.route("/api/slang_variants")
def slang_variants():
    # Always read the file fresh so updates are picked up without a restart
    return jsonify(load_json("cockney_slang_variants.json"))

@app.after_request
def add_no_cache_headers(resp):
    # Prevent stale JSON in browsers/CDNs
    if request.path.startswith("/api/"):
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
    return resp

@app.route("/health")
def health():
    base = load_json("cockney_slang.json")
    variants = load_json("cockney_slang_variants.json")
    index = load_json("cockney_slang_index.json")
    return {
        "ok": True,
        "entries": len(base),
        "variants": len(variants),
        "index": len(index),
    }

if __name__ == "__main__":
    # Render uses the startCommand; this block is for local dev
    app.run(debug=True, host="0.0.0.0", port=5000)
