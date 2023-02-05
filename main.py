from bs4 import BeautifulSoup
import requests
import socket as s
from tld import get_tld
from textblob import TextBlob
import csv

# gets data of website with bs4
def getData(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser") # parses to html
    text = soup.get_text() # gets all text content

    len = 0 # total number of links
    safe = 0 # number of safe links

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and "http" in href:
            len += 1
            if "https" in href: safe += 1

    blob = TextBlob(text) # used for sentiment analysis
    sentiment = blob.sentiment.polarity

    return [len, safe, len - safe, text, sentiment]

# gets current status of website, up (1) or down (0)
def getStatus(url):
    response = requests.get(url) # GET request 

    if response.status_code == 200: return 1
    else: return 0

# gets domain name of url (com, org, etc.)
def getTLD(url):
    # print(f"TLD: {tld}")
    return get_tld(url)

def runAll(url):
    # checks to see if there is error when getting info from url
    # if yes, then skip the website 
    try: getStatus(url)     
    except Exception: return
   
    # gets all the metrics
    data = getData(url)
    totalLinks = data[0]
    safeLinks = data[1]
    nonSafeLinks = data[2]
    text = data[3]
    status = getStatus(url)
    tld = getTLD(url)
    senti = data[4]

    # name of the file to create
    filename = "bad.csv"

    # new data to add to the file
    new_data = {'url': url, 'url_length': len(url), 'https': 1 if "https" in url else 0,
                'total_links': totalLinks, 'safe_links': safeLinks, 'non_safe_links': nonSafeLinks,
                'length': len(text), 'status': status, 'tld': tld, 'sentiment': senti, 'label': 0} # label is 0 for the bad dataset and 1 for the good dataset

    # field names for the header
    fieldnames = ['url', 'url_length', 'https', 'total_links', 'safe_links', 'non_safe_links', 'length', 'status', 'tld', 'sentiment', 'label']

    with open(filename, 'a', newline='') as file:
        # create a CSV writer object
        writer = csv.DictWriter(file, fieldnames=fieldnames)
   
        # write the new data
        writer.writerow(new_data)

# filename containing urls 
filename = "900mal.csv"

# index of urls
column_index = 0

with open(filename, 'r') as file:
    # create a CSV reader object
    reader = csv.reader(file)
   
    # skip the header row
    next(reader)

    # iterate over the rows in the file
    for i, row in enumerate(reader):
        # add the value in the specified column to the list
        runAll(row[column_index])
