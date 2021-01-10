from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
import sys
import os
sys.path.insert(1, "./..")
from demo import get_recipe

# To run, do the following:
# export FLASK_APP=server.py
# `flask run`
app = Flask(__name__, static_folder='../../ui/build')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route("/")
# def hello():
#     return "Hello World!"

# localhost:5000/transcribe?video=[url]
@app.route("/transcribe", methods=['GET'])
def transcribe():
    arg1 = request.args['data']
    res = get_recipe(arg1, True)
    return res

@app.route('/frames/<path:path>')
def serve_frames(path):
    return send_from_directory('frames', path)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
