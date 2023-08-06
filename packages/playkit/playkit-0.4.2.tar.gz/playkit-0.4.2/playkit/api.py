import requests

from bs4 import BeautifulSoup


def search(keyword="",category="apps",pricing="all",rating="all",format="dict",proxies=None):
    requests.packages.urllib3.disable_warnings()
    priceMap = {"all":0,"free":1,"paid":2,"All":0,"Free":1,"Paid":2}
    ratingsMap = {"all":0,"4+":1,"All":0}
    response = {"status":"OK","error":None,"results":[]}
    try:
        payload = {'q': keyword, 'c': category,"price":priceMap[pricing],"rating":ratingsMap[rating]}
    except KeyError as e:
        response = {"status":"Failed","error":e,"results":[]}
        return response


    
    url = "https://play.google.com/store/search?"
    try:
        if proxies:
            htmlresponse = requests.get(url,params = payload,proxies=proxies)
        else:
            htmlresponse = requests.get(url,params = payload)
        
        htmlresponse = BeautifulSoup(htmlresponse.text, 'html.parser')

        contents = htmlresponse.find("div", { "class" : "id-card-list card-list two-cards" }).findAll("div", { "class" : "card-content id-track-click id-track-impression" })
        
        for content in contents:
            result = {}
            result["name"] = content.find("a", {"class":"title"})["title"]
            result["id"] = content.find("span", {"class":"preview-overlay-container"})["data-docid"]
            result["developer"] = content.find("a", {"class":"subtitle"})["title"]
            result["description"] = content.find("div", {"class":"description"}).getText()
            try:
                result["rating"] = content.find("div", {"class":"tiny-star star-rating-non-editable-container"})["aria-label"]
            except TypeError:
                result["rating"] = "Not rated"
            result["price"] = content.findAll("span", {"class":"display-price"})[0].getText()
            result["largeImageUrl"] = content.find("img", {"class":"cover-image"})["data-cover-large"]
            result["smallImageUrl"] = content.find("img", {"class":"cover-image"})["data-cover-small"]
            response["results"].append(result)
        return response
    except Exception as e:
            response["error"] = e
            response["status"] = "Failed"
            return response


