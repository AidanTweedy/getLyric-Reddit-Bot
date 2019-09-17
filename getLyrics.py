import praw
import pdb
import re
import os
import requests
from bs4 import BeautifulSoup

def findLyrics(artist, song):
    error = "Hey there! Something appears to have gone wrong with fetching the lyrics. 
    Please use the format **'<ARTIST>-<SONG>'**. Be cautious about the word 'The' in band names."
    art = str(artist.lower())
    son = str(song.lower())
    url = 'https://www.azlyrics.com/lyrics/' + art + '/' + son
    url = url.strip('\n')
    url = url + '.html'
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        lyrics = soup.find_all('div', attrs = {"class": None, "id": None})[0].get_text()
    except IndexError:
        return error
    except APIException:
        return error
    else:
        return lyrics


reddit = praw.Reddit('lyricbot')

if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
else:
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))


subreddit = reddit.subreddit('pythonforengineers')
r = reddit.redditor('getLyrics')

for comment in subreddit.stream.comments():
    if comment.id not in comments_replied_to:
        if re.search("!getlyrics", comment.body, re.IGNORECASE):
            request = str(comment.body)
            newRequest = request.replace("!getlyrics"," ")
            newRequest = newRequest.replace(" ", "")
            newRequest = newRequest.split('-')
            artist = newRequest[0]
            song = newRequest[1]
            songLyrics = findLyrics(artist,song)
            disclaimer = "\n \n \n \n ^^^^^^^^^^^^^^^Hi!^^^^^^^^^^^^^^^I ^^^^^^^^^^^^^^^am ^^^^^^^^^^^^^^^a ^^^^^^^^^^^^^^^bot ^^^^^^^^^^^^^^^that ^^^^^^^^^^^^^^^scrapes ^^^^^^^^^^^^^^^the ^^^^^^^^^^^^^^^web ^^^^^^^^^^^^^^^for ^^^^^^^^^^^^^^^the ^^^^^^^^^^^^^^^lyrics ^^^^^^^^^^^^^^^that ^^^^^^^^^^^^^^^you ^^^^^^^^^^^^^^^request!^^^^^^^^^^^^^^^If ^^^^^^^^^^^^^^^you ^^^^^^^^^^^^^^^have ^^^^^^^^^^^^^^^any ^^^^^^^^^^^^^^^feedback, ^^^^^^^^^^^^^^^feel ^^^^^^^^^^^^^^^free ^^^^^^^^^^^^^^^to ^^^^^^^^^^^^^^^let ^^^^^^^^^^^^^^^me ^^^^^^^^^^^^^^^know!"
            songLyrics = songLyrics + disclaimer
            comment.reply(songLyrics)
            comments_replied_to.append(comment.id)
            with open("comments_replied_to", "w") as f:
                for comment_id in comments_replied_to:
                    f.write(comment_id + "\n")
            print(artist + "," + song)
            print("Bot replying to : ", comment.body)
