import json
import urllib
from flask import request as req

def getLinks(title):
    title = title.replace(" ", "%20")
    url = "https://en.wikipedia.org/w/api.php?format=json&action=query&titles=" + title + "&prop=links&pllimit=500"
    request = urllib.request.urlopen(url).read()
    data = json.loads(request)["query"]["pages"].values()
    data = list(data)[0]["links"]
    # print(data)
    links = []
    for i in data:
        if i["ns"] == 0:
            links.append(i["title"])
    return links

def main():
    title = input("Enter a title: ")
    print(getLinks(title))

if __name__ == "__main__":
    main()