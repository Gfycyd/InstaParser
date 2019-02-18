import urllib.parse
import requests
import json
access_token="1344954667.dd220e6.dab89449f8694bf1aa025b00f5ac5f8a"
hashtag_recent = 'https://api.instagram.com/v1/tags/tag-name/media/recent?access_token=' + access_token
login = "https://api.instagram.com/v1/users/3539629240/?access_token=1344954667.dd220e6.dab89449f8694bf1aa025b00f5ac5f8a"


text = "#innopolis"
type = "hashtag"
table = {'login':'', 'Name':'', 'Business':'','Bio':'','Phone':'','E-mail':'','Address':'','Followers':'', 'Following':'', 'Link':''}
def search(type,query):
    if type == "hashtag":
        hash = hashtag_recent.replace("tag-name", query[1:len(query)])
        json_data = requests.get(hash).json()
        json_data = json_data["data"]
        k = list()
        for i in json_data:
            p = i["id"]
            l = str(p).find("_")
            k.append(str(p)[l+1:len(str(p))])
        now = dict.fromkeys(k)
        k = list()
        for val in now.keys():
            log = login.replace("self", val)
            js = requests.get(log).json()["data"]
            table = {'login':js["username"], 'Name':js["full_name"], 'Business':js["is_business"],'Bio':js["bio"],'Followers':js["counts"]["followed_by"], 'Following':js["counts"]["follows"], 'Link':js["website"]}
            k.append(table)

        return k
print((search(type,text)))