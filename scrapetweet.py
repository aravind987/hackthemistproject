import snscrape.modules.twitter as sntwitter
import pandas as pd
import itertools
import sys

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")


def scrape_by_keywords(list1, list2):
    """
    returns a dataframe containing the at least one keyword from each list of
    keywords. The capitalization of keywords does not matter.
    :param list1: the first list of keywords
    :param list2: the second list of keywords
    :return: dataframe containing 'date', 'id', 'content', 'username', and 'url'
    of the tweets that have at least one keyword from each list of keywords
    """
    products_list = list(itertools.product(list1, list2))
    data = []
    for i in products_list:
        keyword = i[0] + "  "+ i[1]
        tweets = sntwitter.\
            TwitterSearchScraper(keyword +' since:2021-07-11 until:2021-07-12'+'lang:en').get_items()
        for tweet in tweets:
            data.append({
                'date': tweet.date,
                'content': tweet.content,
                'username': tweet.user.username
            })

    df = pd.DataFrame(data)
    pd.set_option('display.max_colwidth', None)
    return df


def scrape_by_username(un):
    """
    returns a dataframe containing tweets from a specific user
    :param un: username of the user
    :return: a dataframe containing the 'Datetime', 'Text Id', 'Text', and
    'Username' of the tweets from a specific user.
    """
    tweets_list1 = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:{}'.format(un)).get_items()):
        if i > 100:
            break
        tweets_list1.append([tweet.date, tweet.id, tweet.content,
                             tweet.user.username])

    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id',
                                                     'Text', 'Username'])

    return tweets_df1


if __name__ == "__main__":
    text_data = ['rashford']

    #Set trigger words
    triggerWords = ['black']

    #Get tweets from keyword
    tweetsFromKeyword = scrape_by_keywords(text_data, triggerWords).head(50)
    tweetInfo = tweetsFromKeyword[['content','username']].copy()

    #Make sure content of tweet contains both keyword and trigger words instead of username
    deleteIndex = []

    for index,row in tweetInfo.iterrows():
        hasKeyword = False
        hasTriggerWord = False

        for word in row['content'].split():
            if word in text_data:
                hasKeyword = True
            if word in triggerWords:
                hasTriggerWord = True

        if not (hasKeyword and hasTriggerWord):
            deleteIndex.append(index)
    
    tweetInfo.drop(deleteIndex, axis=0, inplace=True)

    potentialMaliciousAccounts = tweetInfo['username']
    print(potentialMaliciousAccounts)
