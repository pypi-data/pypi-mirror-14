import requests
from bs4 import BeautifulSoup

def api(keyword="",category="apps",format="dict"):
    
    response = {"status":"OK","error":None,"results":[]}
    payload = {'q': keyword, 'c': category}
    url = "https://play.google.com/store/search?"
    htmlresponse = requests.get(url,params = payload)

    try:
        htmlresponse.raise_for_status()
    except Exception as e:
        response["error"] = e
        response["status"] = "Failed"
        return response
    
    htmlresponse = BeautifulSoup(htmlresponse.text, 'html.parser')

    contents = htmlresponse.find("div", { "class" : "card-list two-cards" }).findAll("div", { "class" : "card-content id-track-click id-track-impression" })
    
    for content in contents:
    	result = {}
    	result["name"] = content.find("a", {"class":"title"})["title"]
    	result["id"] = content.find("span", {"class":"preview-overlay-container"})["data-docid"]
    	result["developer"] = content.find("a", {"class":"subtitle"})["title"]
    	result["description"] = content.find("div", {"class":"description"}).getText()
    	result["rating"] = content.find("div", {"class":"tiny-star star-rating-non-editable-container"})["aria-label"]
    	result["price"] = content.findAll("span", {"class":"display-price"})[0].getText()
    	response["results"].append(result)
    return response