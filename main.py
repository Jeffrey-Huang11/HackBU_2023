from bs4 import BeautifulSoup
import requests
import socket as s
from tld import get_tld
from textblob import TextBlob
import csv


# gets all outgoing links on website with bs4
def getData(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser") # parses to html
    text = soup.get_text()

    len = 0
    safe = 0

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and "http" in href:
            # print(href)
            len += 1
            if "https" in href: safe += 1

    # print("Number of links: {0}".format(size))
    # print("Number of safe links (https): {0}".format(safe))
    # print("Number of non-safe links (http): {0}".format(size - safe)

    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    return [len, safe, len - safe, text, sentiment]

'''
# gets all text on a website with bs4
def getText(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser") # parses to html

    # print(text)
    # print("Number of words: {0}".format(len(text.split())))
    return len(soup.get_text())

'''

# gets current status of website
def getStatus(url):
    response = requests.get(url)

    if response.status_code == 200:
        return 1
    else:
        return 0


# gets domain name of url
def getTLD(url):
    # print(f"TLD: {tld}")
    return get_tld(url)

'''
# checks sentiment of a text using textblob
def sentiment(url):
    text = getText(url)
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    if sentiment > 0:
        print("Positive")
    elif sentiment == 0:
        print("Neutral")
    else:
        print("Negative")

   
    return sentiment
'''
    

def runAll(url):
    try: getStatus(url)
    except Exception: return
   
    data = getData(url)
    totalLinks = data[0]
    safeLinks = data[1]
    nonSafeLinks = data[2]

    text = data[3]
    status = getStatus(url)
    tld = getTLD(url)
    senti = data[4]

    # name of the file
    filename = "data.csv"

    # new data to add to the file
    new_data = {'url': url, 'url_length': len(url), 'https': 1 if "https" in url else 0,
                'total_links': totalLinks, 'safe_links': safeLinks, 'non_safe_links': nonSafeLinks,
                'length': len(text), 'status': status, 'tld': tld, 'sentiment': senti}

    # field names for the header
    fieldnames = ['url', 'url_length', 'https', 'total_links', 'safe_links', 'non_safe_links', 'length', 'status', 'tld', 'sentiment']

    with open(filename, 'a', newline='') as file:
        # create a CSV writer object
        writer = csv.DictWriter(file, fieldnames=fieldnames)
   
        # write the new data
        writer.writerow(new_data)


filename = "input.csv"
column_index = 1
with open(filename, 'r') as file:
    # create a CSV reader object
    reader = csv.reader(file)
   
    # skip the header row
    next(reader)
   
    index = 0
    # iterate over the rows in the file
    for row in reader:
        # add the value in the specified column to the list
        runAll(row[column_index])
        index += 1
