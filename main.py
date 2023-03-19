from flask import Flask, jsonify, request
from flask_cors import CORS
from scrapetweet import scrape_by_keywords, scrape_by_username
import sys

sys.stdin.reconfigure(encoding="utf-16")
sys.stdout.reconfigure(encoding="utf-16")

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

    #Set trigger words
    triggerWords = ['mixed', 'muslims', 'nigga', 'chinese', 'jews', 'monkey', 'white', 'lesbian', 'black', 'nigger','immigrant','cunt']

    #Get tweets from keyword
    tweetsFromKeyword = scrape_by_keywords(text_data, triggerWords).head(200)

    #Make sure content of tweet contains both keyword and trigger words instead of username
    deleteIndex = []

    for index,row in tweetsFromKeyword.iterrows():
        hasKeyword = False
        hasTriggerWord = False

        for word in row['content'].split():
            if word in text_data:
                hasKeyword = True
            if word in triggerWords:
                hasTriggerWord = True

        if not (hasKeyword and hasTriggerWord):
            deleteIndex.append(index)
    
    #Drop all non malicious tweets
    tweetsFromKeyword.drop(deleteIndex, axis=0, inplace=True)
    #Store all potentially malicious accounts from tweets
    potentialMalicious = tweetsFromKeyword[['date','content','username']]
    potentialMalicious.to_csv('test.csv')

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
            'username': text_data[0],
            'text': "HIII",
            'time': '26/5/32'
        }
    ]

    return classTags

if __name__ == "__main__":
    app.run(debug=True)