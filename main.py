from flask import Flask, jsonify, request
from flask_cors import CORS
from scrapetweet import scrape_by_keywords, scrape_by_username
import sys
import cohere
#from cohere.classify import Example
import pandas as pd

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

app = Flask(__name__)
CORS(app)


'''
Gets a username from the Front-End site and runs it through Co:here's API
'''
@app.route("/getAccount", methods=['GET','POST'])
def checkAccount():
    username = request.get_json()['username']

    tweetByUsernames = scrape_by_username(username).head(90)
    totalTweets = len(tweetByUsernames.index)

    #Set trigger words
    triggerWords = ['mixed', 'muslims', 'nigga', 'chinese', 'jews', 'monkey', 'white', 'lesbian', 'black', 'nigger','immigrant','cunt']

    #Make sure content of tweet contains trigger words instead of username
    deleteIndex = []

    for index,row in tweetByUsernames.iterrows():
        hasTriggerWord = False

        for word in row['Text'].split():
            if word in triggerWords:
                hasTriggerWord = True

        if not (hasTriggerWord):
            deleteIndex.append(index)

    #Drop all non malicious tweets
    tweetByUsernames.drop(deleteIndex, axis=0, inplace=True)
    #Store all potentially malicious accounts from tweets
    potentialMalicious = tweetByUsernames[['Datetime','Text','Username']]

    potentialMalicious.to_csv('test2.csv')
    potentialMaliciousList = []

    if(len(potentialMalicious) == 0):
        return [{
        'image': "https://media.discordapp.net/attachments/757730257150279742/1080660938249736244/image.png?width=156&height=222",
        'username': username,
        'percentRacist': 0,
        'percentHate': 0,
        'percentNeutral': 1
    }]

    for index,row in potentialMalicious.iterrows():
        potentialMaliciousList.append(row['Text'])

    co = cohere.Client('c2fGtXEdjVrQGYsS8rCNTRRLjn9wHCRBunYa2S8V') # This is your trial API key
    response = co.classify(
    model='623232f3-320c-4baf-a830-2972ec7d8bb3-ft',
    inputs=potentialMaliciousList)

    racistCommentScore = 0
    hateCommentScore = 0
    neutralCommentScore = 0

    blablabla = pd.DataFrame(response.classifications)
    blablabla.to_csv('test6.csv')

    resultsdf = pd.DataFrame(columns=['labels','confidence'])

    for x in range(0,blablabla.shape[0]):
        resultsdf.loc[x] = [response[x].prediction,response[x].confidence]
    
    resultsdf.to_csv('test8.csv')

    for idx,rows in resultsdf.iterrows():
        if rows['labels'] == 'racism':
            racistCommentScore += rows['confidence']
        elif rows['labels'] == 'hate':
            hateCommentScore += rows['confidence']
        elif rows['labels'] == 'nothate':
            neutralCommentScore += rows['confidence']

    racistCommentScore /= totalTweets
    hateCommentScore /= totalTweets
    neutralCommentScore = 1 - racistCommentScore - hateCommentScore
    scoresList = [racistCommentScore,hateCommentScore,neutralCommentScore]

    df = pd.DataFrame(scoresList, columns=['scores'], index=['racist', 'hate', 'neutral'])
    df.to_csv('test7.csv')
    
    # Store all potentially malicious accounts from tweets
    return [{
        'image': "https://media.discordapp.net/attachments/757730257150279742/1080660938249736244/image.png?width=156&height=222",
        'username': username,
        'percentRacist': racistCommentScore,
        'percentHate': hateCommentScore,
        'percentNeutral': neutralCommentScore
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

    potentialMalicious.to_csv('test1.csv')

    twitterToReturn = list(range(len(potentialMalicious)))

    for i in range(len(potentialMalicious)):
        twitterToReturn[i] = {
            'image': 'https://scontent-yyz1-1.xx.fbcdn.net/v/t39.30808-6/308487577_523808733083795_2015773722187850021_n.png?_nc_cat=107&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=uXF-ArkDCnAAX9_bgtN&_nc_ht=scontent-yyz1-1.xx&oh=00_AfCJAxcfz92uwXUBP6GtYx4FDuIqWT6pEdgG6p8ryq5m_Q&oe=641C4E94',
            'username': potentialMalicious.iloc[i]['username'],
            'text': potentialMalicious.iloc[i]['content'],
            'time': potentialMalicious.iloc[i]['date']
        }
    return twitterToReturn

if __name__ == "__main__":
    app.run(debug=True)