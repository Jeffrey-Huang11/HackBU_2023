from bs4 import BeautifulSoup
import requests
import socket as s
from tld import get_tld
from textblob import TextBlob
import csv


# gets all outgoing links on website with bs4
def getLinks(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser") # parses to html

    links = []
    safe = 0

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and "http" in href:
            # print(href)
            links.append(href)
            if "https" in href: safe += 1


    size = len(links)
    # print("Number of links: {0}".format(size))
    # print("Number of safe links (https): {0}".format(safe))
    # print("Number of non-safe links (http): {0}".format(size - safe))
    return [size, safe, size - safe]


# gets all text on a website with bs4
def getText(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser") # parses to html

    # gets all text from url
    text = soup.get_text()
    # print(text)
    # print("Number of words: {0}".format(len(text.split())))
    return text


# gets current status of website
def getStatus(url):
    response = requests.get(url)

    if response.status_code == 200:
        # print(f"Successful request. The website {url} is up and running.")
        return 1
    else:
        # print(f"Request failed. The website {url} is either down or unavailable.")
        return 0


# gets domain name of url
def getTLD(url):
    tld = get_tld(url)
    # print(f"TLD: {tld}")
    return tld


# checks sentiment of a text using textblob
def sentiment(url):
    text = getText(url)
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity


    '''
    if sentiment > 0:
        print("Positive")
    elif sentiment == 0:
        print("Neutral")
    else:
        print("Negative")
    '''
   
    return sentiment


def runAll(url):
    links = getLinks(url)
    totalLinks = links[0]
    safeLinks = links[1]
    nonSafeLinks = links[2]

    text = getText(url)
    status = getStatus(url)
    tld = getTLD(url)
    senti = sentiment(url)

    # name of the file
    filename = "data.csv"

    # new data to add to the file
    new_data = {'url': url, 'url_length': len(url), 'https': 1 if "https" in url else 0,
                'total_links': totalLinks, 'safe_links': safeLinks, 'non_safe_links': nonSafeLinks,
                'length': len(text), 'status': status, 'tld': tld, 'sentiment': senti}

    # field names for the header
    fieldnames = ['url', 'url_length', 'https', 'total_links', 'safe_links', 'non_safe_links', 'length', 'status', 'tld', 'sentiment']

    # flag to indicate if the header has already been written
    header_written = True

    with open(filename, 'a', newline='') as file:
        # create a CSV writer object
        writer = csv.DictWriter(file, fieldnames=fieldnames)
   
        # write the new data
        writer.writerow(new_data)


filename = "input.csv"
column_index = 0
with open(filename, 'r') as file:
    # create a CSV reader object
    reader = csv.reader(file)
   
    # skip the header row
    next(reader)
   
    index = 0
    # iterate over the rows in the file
    for row in reader:
        if index == 2: break
        # add the value in the specified column to the list
        runAll(row[column_index])
        index += 1
