from bs4 import BeautifulSoup
import requests
import socket as s
from tld import get_tld
from textblob import TextBlob
import csv

def csv_to_dict(filename):
    dic = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            dic.update({row[0]:1})
        return dic

def check_key_in_string(dictionary, string):
    for key in dictionary:
        if key in string:
            return True
    return False

# writes data into csv file
def runAll(url, dic):
    # checks to see if there is error when getting info from url
    # if yes, then skip the website 
    # try: getStatus(url)     
    # except Exception: return
   
    result = 1 if check_key_in_string(dic, url) else 0

    # name of the file to create
    filename = "bad2.csv"

    # new data to add to the file
    new_data = {'url': url, 'bad_words': result, 'label': "bad"} # label is 0 for the bad dataset and 1 for the good dataset

    # field names for the header
    fieldnames = ['url', 'bad_words', 'label']


    with open(filename, 'a', newline='') as file:
        
        # create a CSV writer object
        writer = csv.DictWriter(file, fieldnames=fieldnames)
   
        # write the new data
        writer.writerow(new_data)



# filename containing urls 
filename = "900mal.csv"
global_dic = csv_to_dict("bad-words.csv")

# index of urls
column_index = 0

with open(filename, 'r') as file:
    # create a CSV reader object
    reader = csv.reader(file)
   
    # skip the header row
    next(reader)

    # iterate over the rows in the file
    for row in reader:
        # add the value in the specified column to the list
        runAll(row[column_index], global_dic)
