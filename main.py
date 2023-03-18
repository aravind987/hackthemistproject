from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/getClass", methods=['GET','POST'])
def classifyText():
    text_data = request.get_json()['text']

    classTags = ["Returning from Python"]

    # Do Something
    print(text_data)

    return classTags

if __name__ == "__main__":
    app.run(debug=True)