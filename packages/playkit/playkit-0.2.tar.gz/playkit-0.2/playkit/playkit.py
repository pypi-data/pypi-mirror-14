import requests
from bs4 import BeautifulSoup

def getapps(keyword=""):
    payload = {'q': keyword, 'c': "apps"}
    url = "https://play.google.com/store/search?"
    response = requests.get(url,params = payload)
    response = BeautifulSoup(response.text, 'html.parser')

    apps = response.find("div", { "class" : "card-list two-cards" }).findAll("div", { "class" : "card-content id-track-click id-track-impression" })
    appList = []
    for app in apps:
    	appcontent = {}
    	appcontent["name"] = app.find("a", {"class":"title"})["title"]
    	appcontent["id"] = app.find("span", {"class":"preview-overlay-container"})["data-docid"]
    	appcontent["developer"] = app.find("a", {"class":"subtitle"})["title"]
    	appcontent["description"] = app.find("div", {"class":"description"}).getText()
    	appcontent["rating"] = app.find("div", {"class":"tiny-star star-rating-non-editable-container"})["aria-label"]
    	appcontent["price"] = app.findAll("span", {"class":"display-price"})[0].getText()
    	appList.append(appcontent)
    return appList