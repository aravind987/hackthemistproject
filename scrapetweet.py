import snscrape.modules.twitter as sntwitter
import pandas as pd
import itertools


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
            TwitterSearchScraper(keyword +' since:2020-12-01 until:2020-12-18').get_items()
        for tweet in tweets:
            data.append({
                'date': tweet.date,
                'id': tweet.id,
                'content': tweet.content,
                'username': tweet.user.username,
                'url': tweet.url
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
    a = ['Rashford', 'vini', 'Vinicius', "Alexander-Arnold", "Naby Keita",
         "zlatan", "ibrahimovic"]
    b = ['nigga', 'black']
    print(scrape_by_keywords(a, b)[['content', 'username']].head(10))
    print(scrape_by_username('jack')['Text'].head(10))
