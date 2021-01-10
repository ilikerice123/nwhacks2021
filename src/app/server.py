from flask import Flask, request
import sys
sys.path.insert(1, "./..")
from demo import get_ingredients

# To run, do the following:
# export FLASK_APP=server.py
# `flask run`
app = Flask(__name__)

@app.route("/")
def hello():
    print("SKLDJFLSJDFSDF")
    return "Hello World!"

# localhost:5000/transcribe?video=[url]
@app.route("/transcribe", methods=['GET'])
def transcribe():
    print("HELLO??????")
    arg1 = request.args['data']
    print(arg1)
    res = get_ingredients(arg1, True)
    print(res)
    return res

if __name__ == "__main__":
    app.run(debug=True)
