from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


'''
Gets a username from the Front-End site and runs it through Co:here's API
'''
@app.route("/getAccount", methods=['GET','POST'])
def checkAccount():
    username = request.get_json()['username']
    return [{
        'image': "https://media.discordapp.net/attachments/757730257150279742/1080660938249736244/image.png?width=156&height=222",
        'username': username,
        'percentRacist': 0.4,
        'percentHate': 0.4,
        'percentNeutral': 0.2
    }]

@app.route("/getClass", methods=['GET','POST'])
def classifyText():
    text_data = request.get_json()['keywords']

    # Do Something
    print(text_data)

    return comments


def convertDFtoObject(dataFrame):



if __name__ == "__main__":
    app.run(debug=True)