#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
from sys import argv
from threading import Thread
from queue import Queue
import datetime
import PyRSS2Gen
import hashlib
import requests
import sys
import os


class twitterParser(HTMLParser):
    """HTMLParser class object."""
    def __init__(self):
        """
        Inicialize __init__ class with some variables used later

        declared variables:
        self.recording -- int that controls if there's data recording
        self.data -- list containing the parsed HTML
        self.attributes -- list containing HTML tag's attributes
        self.tempData -- temporal list containing parsed HTML
        self.id -- string containin tag information for differentiating
        """

        HTMLParser.__init__(self, convert_charrefs=True)
        self.recording = 0
        self.data = []
        self.attributes = []
        self.tempData = []
        self.id = ''

    def handle_starttag(self, tag, attrs):
        """
        Identify when the tags of interest begins and start recording the data.

        return -- just a way for breake the loop
        """

        self.tag = tag
        if self.tag not in ['p', 'span', 'img']:
            return

        elif self.recording:
            self.recording += 1
            return

        # Key to find the tweets and identify if they are retweets.
        # It is likely to change over time, as Twitter do the same
        for name, value in attrs:
            if self.tag == 'p' and name == 'class' \
              and 'TweetTextSize TweetTextSize' in value:
                self.recording += 1
                self.attributes += attrs
                self.id = 'p'
                break
            elif self.tag == 'span' and name == 'class' \
              and 'js-retweet-text' in value:
                self.recording += 1
                self.attributes += attrs
                self.id = 'span'
                break
            elif self.tag == 'img' and name == 'class' and \
              'Emoji Emoji--forText' in value:
                self.recording += 1
                self.attributes += attrs
                self.id = 'p'
                break
            else:
                return

    def handle_endtag(self, tag):
        """Identify when the tags of interest ends and stop recording data."""
        self.tag = tag

        if tag == 'p' and self.recording:
            self.recording -= 1
        elif tag == 'span' and self.recording:
            self.recording -= 1
        elif tag == 'img' and self.id == 'p' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        """When recording, save the data."""

        if self.recording:
            self.tempData.append(data)

        elif self.tempData != []:
            if self.id == 'p':
                self.data.append(self.tempData)
                self.tempData = []

            elif self.id == 'span':
                # Random hash to identify retweets
                self.tempData += [' 59bcc3ad6775562f845953cf01624225']
                self.data.append(self.tempData)
                self.tempData = []

    def return_value(self):
        """
        Return all saved data.

        return -- list of list of chopped strings
        """
        return self.data


def retrieve_html(url):
    """
    Retrieve HTML code from url.

    url -- string containing an url to be retrieved
    return -- string containing HTML code or nothing if there's an error
    """
    try:
        code = requests.get(url).text
    except:
        return
    return code


def sanitize(tweet):
    """
    Sanitize data. Tweet is a list of chopped up strings that need to be
    reassembled. Also, it takes out some weird chars.

    tweet -- list containing chopped strings with the data
    return -- string containing sanitized tweet
    """
    final = ''
    counter = 0
    errors = ['…', '\xa0']

    for part in tweet:
        if part not in errors:
            try:
                if tweet[counter - 2] in 'https://' and part in 'https://':
                    final += ' '
                elif 'pic.twitter.com/' in part:
                    final += ' '
            except:
                pass
            final += part
        counter += 1
    print(final)
    if final:
        return final


def create_feed(user, feeds):
    """
    Create feed file.

    user -- string containing twitter's username
    feeds -- list containing tweets
    """
    user = user.strip()
    items = []

    for feed in feeds:
        i = 0
        limite = 5
        cuatro_primeras = ''
        split = feed.split()

        if len(split) <= 5:
            limite = len(split)

        for i in range(0, limite):
            cuatro_primeras += split[i] + ' '
            i += 1
        # GUID specified to improve feed readers reading
        guid = hashlib.sha1(cuatro_primeras.encode()).hexdigest()
        item = PyRSS2Gen.RSSItem(
            title='@' + user + ' says: ' + cuatro_primeras + '...',
            link='https://twitter.com/' + user,
            description=feed,
            guid=PyRSS2Gen.Guid(guid, isPermaLink=False)
        )
        items.append(item)

    rss = PyRSS2Gen.RSS2(
        title='@' + user + ' Twitter\'s feed.',
        link='https://twitter.com/' + user,
        description='@' + user + ' Twitter\'s feed.',
        lastBuildDate=datetime.datetime.now(),
        items=items
    )

    rss.write_xml(open("feeds/" + user + ".xml", "w"), encoding='utf-8')


def slave():
    """
    It creates threads and executes the __main__ part according to the
    'threads' variable defined in __main__.
    """

    while True:
        tweets = []
        user = repr(q.get())
        user = user.replace("\\n", "")
        user = user.replace("'", "")

        code = retrieve_html('https://twitter.com/' + user + '?lang=en')

        if code == "":
            q.task_done()
            break
        parser = twitterParser()
        parser.feed(code)
        data = parser.return_value()

        for tweet in data:
            tweet = sanitize(tweet)
            tweets.append(tweet)
        tweets = mark_as_retweet(tweets)
        create_feed(user, tweets)
        q.task_done()


def mark_as_retweet(tweets):
    """
    Mark tweet as retweet seeking a concrete number.

    tweets -- list of strings containing sanitized tweets
    return -- list of strings maked as retweets with the '♻' symbol
    """

    coincidence = []
    for num in enumerate(tweets):
        if '59bcc3ad6775562f845953cf01624225' in num[1]:
            coincidence.append(num[0])
    for coinc in coincidence:
        if coinc < len(tweets):
            tweets[coinc+1] = '♻' + tweets[coinc+1]
    for coinc in reversed(coincidence):
        tweets.pop(coinc)

    return tweets

if __name__ == "__main__":

    # This variable can be modified
    threads = 2
    q = Queue()

    if not os.path.exists('feeds'):
        os.mkdir(("feeds"))

    for i in range(threads):
        t = Thread(target=slave)
        t.daemon = True
        t.start()

    if len(argv) == 2:
        user = argv[1]
        q.put(user)
        # block the end of the program until all threads are finished
        q.join()

    else:
        try:
            feed_file = open('twitter_users', 'r')
        except:
            print("The file twitter_users does not exist."
                  " You must create it to continue.")
            sys.exit()

        feed = feed_file.readlines()
        feed_file.close()

        for user in feed:
            q.put(user)
        # block the end of the program until all threads are finished
        q.join()
