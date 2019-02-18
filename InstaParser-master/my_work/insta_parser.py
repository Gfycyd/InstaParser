from config import table, array, link, tag, tagging, pat,next_page,pattern,p
import re
import time
from time import strftime, gmtime
from urllib.request import quote
from urllib.request import urlopen

import requests

import excel_writer


class COUNT:
    i = 0
    all = 0
    ups = 0
    name = ''
def build_from_u(text):
    for u, c in zip(array.keys(), array.values()):
        text = text.replace(u, c)

    pattern = re.compile(r'\\u[0-9a-f][0-9a-f][0-9a-f][0-9a-f]')
    subs = pattern.findall(text)
    for s in subs:
        text = text.replace(s, '')
    text.replace('\\\n', ' ')
    print(text)
    text.replace('\\', '')

    return text

def account_info(type, s, l):
    URL = s
    r = requests.get(URL)
    html = r.text
    # URL = link + 'sugaring_moskvina'
    request = requests.get(URL)
    if request.status_code == 200:
        pass
    else:
        return ""
    r = requests.get(URL)
    html = r.text
    #html = urlopen(URL).read().decode('utf-8')
    # table information
    table = {'procent': '', 'login': '', 'Name': '', 'Business': '', 'Bio': '', 'Phone': '', 'E-mail': '', 'Address': '',
             'Followers': '', 'Following': '', 'Link': '', 'Data' : strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'priv': ""}
    # followers
    pattern = re.compile('"edge_followed_by":{"count":[0-9]*')
    temp =  pattern.findall(html)
    if len(temp) > 0:
        table['Followers'] = temp[0]
        table['Followers'] = table['Followers'][28:len(table['Followers'])]
    else:
        table['Followers'] = ''
    # following
    pattern = re.compile('"edge_follow":{"count":[0-9]*')
    temp =  pattern.findall(html)
    if len(temp) > 0:
        table['Following'] = temp[0]
        table['Following'] = table['Following'][23:len(table['Following'])]
    else:
        table['Following'] = ''


    #is_ptivate?
    pattern = re.compile('"is_private":[^,]*')
    temp = pattern.findall(html)
    if len(temp) > 0:
        table['priv'] = temp[0]
        table['priv'] = table['priv'][13:len(table['priv'])]
        if table['priv'] == 'true':
            table['priv'] = 'да'
        if table['priv'] == 'false':
            table['priv'] = 'нет'
    else:
        table['priv'] = ''
    # is_business?
    pattern = re.compile('"is_business_account":[truefals]*')
    temp = pattern.findall(html)
    if len(temp) > 0:
        table['Business'] = temp[0]
        table['Business'] = table['Business'][22:len(table['Business'])]
        if table['Business'] == 'true':
            table['Business'] = 'да'
        if table['Business'] == 'false':
            table['Business'] = 'нет'
    else:
        table['Business'] = ""
    # login
    table['login'] = l

    # name
    #"full_name": "\u0428\u0443\u0433\u0430\u0440\u0438\u043d\u0433 \u0432 \u0411\u0440\u044f\u043d\u0441\u043a\u0435"
    pattern = re.compile('"full_name":"[^"]*')
    temp = pattern.findall(html)
    if (len(temp) > 0 ):
        table['Name'] = temp[0]
        table['Name'] = build_from_u(table['Name'][13:len(table['Name'])])
    # e-mail
    #pattern = re.compile('"business_email":"\w*\S\w*\S\w*\S\w*"')
    pattern = re.compile('"business_email":"[^"]*')
    temp = pattern.findall(html)
    if len(temp) > 0:

        table['E-mail'] = pattern.findall(html)[0]
        table['E-mail'] = table['E-mail'][18:len(table['E-mail'])]
    else:
        table['E-mail'] = ''
    # bio
    pattern = re.compile('{"biography":"[^"]*')
    temp = pattern.findall(html)
    if (len(temp) > 0):
        temp = temp[0]

        table['Bio'] = build_from_u(temp[14:len(temp)])
    else:
        table['Bio'] = ""
    # phone
    #pattern = re.compile('"business_phone_number":"\S\d*"')
    pattern = re.compile('"business_phone_number":"[^"]*')
    temp = pattern.findall(html)
    if len(temp) > 0:
        table['Phone'] = temp[0]
        table['Phone'] = table['Phone'][25:len(table['Phone'])]
    else:
        table['Phone'] = ""

    # address
    ##"business_address_json":"{\"street_address\": \"\", \"zip_code\": \"\", \"city_name\": \"Bryansk\", \"region_name\": \"\", \"country_code\": \"RU\"}"
    pattern = re.compile('"business_address_json":"[^}]*')
    temp = pattern.findall(html)
    if len(temp) > 0:
        temp = temp[0].replace("\\", '')
        temp = temp.replace("\"",'')

        temp = temp[23:len(temp)]
        temp = temp.replace("street_address: ",'')
        temp = temp.replace("zip_code: ","")
        temp = temp.replace("city_name: ", "")
        temp = temp.replace("region_name: ", "")
        temp = temp.replace("country_code: ", "")
        temp = temp.replace(" ", "")
        temp = temp.replace(",,", ",")
        table['Address'] = build_from_u(temp)
    else:
        table['Address'] = ""
    # link
    pattern = re.compile('"external_url":"https://[^"]*')
    temp = pattern.findall(html)
    if len(temp) > 0:
        temp = temp[0]
        temp = temp[16:len(temp)]
        table['Link'] = temp
    else:
        table['Link'] = ""
    ls = table
    return ls
def find_logins_page(temp,s,h,i):
    if COUNT.i == COUNT.ups:
        return -1
    URL = temp.replace("link", i)

    r = requests.get(URL)

    html = r.text
    # html = urlopen(URL).read().decode('utf-8')
    pattern = re.compile('meta property="og:description"[^:]*')
    login = pattern.findall(html)
    m = re.search('@[^ ]*', login[0])
    login = m.group(0).replace('@', "")
    if (login[len(login) - 1] == ")"):
        login = login[0:len(login) - 1]
    links = link + login + "/"
    table = account_info("@", links, login)
    COUNT.i = COUNT.i + 1
    if COUNT.i % 1 == 0:
        table['procent'] = str(round(float((COUNT.i)/COUNT.ups*100))) + "%"
    else:
        table['procent'] = '-'
    excel_writer.add_row(h, list(table.values()), COUNT.name)
    return 7
def login_encod(log,s,h):

    for i in range(len(log)):
        log[i] = log[i][12:len(log[i])]
    temp = tagging + s
    log = set(log)
    for i in log:
        try:
            res = find_logins_page(temp,s,h,i)
            if res == -1:
                return -1
        except:
            time.sleep(3)
            res = find_logins_page(temp, s, h, i)
            if res == -1:
                return -1

    return 7

def search(type, s, h, count):
    if type == "login":
        l = s
        s = link + s + "/"
        ls = account_info(type, s, l)
        ls['procent'] = '-'
        ls = ls.values()

        ls = list(ls)
        excel_writer.add_row(h, ls, 'Логины')
    if type == "hashtag":
        COUNT.i = 0
        s = quote(s.encode('utf-8'))
        URL = (tag + s + "/?__a=1")
        html = urlopen(URL).read().decode('utf-8')
        all = p.findall(html)[0]
        all = all[32:len(all)]
        c1 = 0
        mult = 10
        print(all)
        for i in all:
            c1 = c1*mult + int(i)
        COUNT.all = c1
        c1 = 0
        mult = 10
        for i in count:
            c1 = c1*mult + int(i)
        count = c1
        print(COUNT.all)
        if count<=0 or (count > COUNT.all):
            COUNT.ups = COUNT.all
        else:
            COUNT.ups = count
        print(s)
        COUNT.name = excel_writer.create_list(h, s)
        valid = "true"
        while(valid == "true"):
            time.sleep(2)
            log = pattern.findall(html)
            res = login_encod(log, s, h)
            if res == -1:
                return

            n_p = next_page.findall(html)
            if len(n_p) != 0:
                valid = pat.findall(html)[0]
                valid = valid[15:len(valid)]
                n_p = n_p[0]
                n_p = n_p[13:len(n_p)]
                html = urlopen(URL + "&max_id="+n_p).read().decode('utf-8')
            else:
                break


