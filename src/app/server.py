from flask import Flask, request, send_from_directory
import sys
sys.path.insert(1, "./..")
from demo import get_recipe

# To run, do the following:
# export FLASK_APP=server.py
# `flask run`
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# localhost:5000/transcribe?video=[url]
@app.route("/transcribe", methods=['GET'])
def transcribe():
    arg1 = request.args['data']
    print(arg1)
    res = get_recipe(arg1, True)
    print(res)
    return res

@app.route('/frames/<path:path>')
def send_js(path):
    return send_from_directory('frames', path)

if __name__ == "__main__":
    app.run(debug=True)
