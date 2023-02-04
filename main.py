from bs4 import BeautifulSoup
import requests
import socket as s

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

    print("Number of links: {0}".format(len(links)))
    print("Number of safe links (https): {0}".format(safe))
    print("Number of non-safe links (http): {0}".format(len(links) - safe))
    return links

def getText(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser") # parses to html

    # gets all text from url
    text = soup.get_text() 
    # print(text)
    print(len(text.split()))
    return text


def obf(url):
    


    print("bleh")


'''
def getIP(url):
    s.gethostbyname(url)
    print(s)

'''
def getIP(url):
    s.gethostbyname(url)
    print(s)

url = input("Enter url: ")
links = getLinks(url)
text = getText(url)
getIP(url)








