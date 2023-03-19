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

    classTags = [
        {
            'username': 'Test',
            'text': "HIII",
            'time': '26/5/32',
            'image': 'https://media.discordapp.net/attachments/757730257150279742/1080660938249736244/image.png?width=156&height=222'
        },
        {
            'username': 'Test',
            'text': "HIII",
            'time': '26/5/32'
        },
        {
            'username': 'AADADA',
            'text': "HIII",
            'time': '26/5/32'
        }
    ]

    # Do Something
    print(text_data)

    return classTags

if __name__ == "__main__":
    app.run(debug=True)