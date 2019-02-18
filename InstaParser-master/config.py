import os
import re

import oauth2client.service_account

path = os.path.abspath('credentials.json')
from platform import linux_distribution

def auth():
    if linux_distribution():
        scope = ['https://spreadsheets.google.com/feeds']
        basedir = os.path.abspath(os.path.dirname(__file__))
        data_json = basedir + '/acc.json'
        creds = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name(data_json, scope)
        return creds
    else:
        scope = ['https://spreadsheets.google.com/feeds']
        basedir = os.path.abspath(os.path.dirname(__file__))
        data_json = basedir + '\\acc.json'
        creds = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name(data_json, scope)
        return creds
array = {'u0430': 'а', 'u0431': 'б', 'u0432': 'в', 'u0433': 'г', "u0434": "д", "u0435": "е", "u0451": "ё",
             "u0436": "ж", "u0437": "з", "u0438": "и",
             "u0439": "й", "u043a": "к", "u043b": "л", "u043c": "м", "u043d": "н", "u043e": "о", "u043f": "п",
             "u0440": "р", "u0441": "с", "u0442": "т", "u0443": "у", "u0444": "ф", "u0445": "х", "u0446": "ц",
             "u0447": "ч", "u0448": "ш", "u0449": "щ", "u044a": "ъ", "u044b": "ы", "u044c": "ь", "u044d": "э",
             "u044e": "ю", "u044f": "я", "u0410": "А", "u0411": "Б", "u0412": "В", "u0413": "Г", "u0414": "Д",
             "u0415": "Е", "u0401": "Ё", "u0416": "Ж", "u0417": "З", "u0418": "И", "u0419": "Й", "u041a": "К",
             "u041b": "Л", "u041c": "М", "u041d": "Н", "u041e": "О", "u041f": "П", "u0420": "Р", "u0421": "С",
             "u0422": "Т", "u0423": "У", "u0424": "Ф", "u0425": "Х", "u0426": "Ц", "u0427": "Ч", 'u0428': "Ш",
             "u0429": "Щ", "u042a": "Ъ", "u042b": "Ы", "u042c": "Ь", "u042d": "Э", "u042e": "Ю", "u042f": "Я"}
table = {'login':'', 'Name':'', 'Business':'','Bio':'','Phone':'','E-mail':'','Address':'','Followers':'', 'Following':'', 'Link':''}

link = "https://www.instagram.com/"
tag = "https://www.instagram.com/explore/tags/"
tagging = "https://www.instagram.com/p/link/?tagged="

table_excel = "https://docs.google.com/spreadsheets/d/1deGTmHr8QI2mslRIHFmzotVQyGcUBdgUxmquJu0B2Tk/edit#gid=0"

pat = re.compile('has_next_page":[falsetru]*')
pattern = re.compile('shortcode":"[^"]*')
next_page = re.compile('end_cursor":"[^"]*')
p = re.compile('edge_hashtag_to_media":{"count":[^,]*')
