from __future__ import print_function
import gspread
import datetime
from config import path, auth


# создаёт новый лист для запроса в начале таблицы, имя + дата создания, чтобы не было коллизий
def create_list(url, name):
    try:
        creds = auth()
        gc = gspread.authorize(creds)

        spread_sheet = gc.open_by_url(url)
        if name[0] == '%':
            name = 'Info data  '
        name = name + ' '
        date = str(datetime.datetime.today().strftime("%m.%d %H.%M.%S"))
        for i in date:
            if i == ":":
                i = '.'
            if i == "/":
                i = '.'
            name = name + i
        spread_sheet.worksheet('template').duplicate(insert_sheet_index=0, new_sheet_name=name)
        return name
    except:
        print('Сделай лист с template в таблице по адресу: ', url)

#добавляет колонку
def add_row(html, row, name):
    creds = auth()
    gc = gspread.authorize(creds)
    # sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/17yrMltdIA4UOPePk5ZDSjPhHbhqi3-w6X9Zuby198OU/edit#gid=0').sheet1
    sheet = gc.open_by_url(html)
    row[2] = row[2].replace('\\','')
    row[4] = row[4].replace('\\','')
    sheet.worksheet(name).insert_row(row,2)
    # sheet.delete_row(5)

#delete
def delete(html):
    creds = auth()
    gc = gspread.authorize(creds)
    sheet = gc.open_by_url(html).sheet1
    while sheet.row_values(2) != []:
        sheet.delete_row(2)

# add_row(['Логин', 'Имя', 'Бизнес аккаунт?','Биография','Телефон','E-mail','Address','Followers', 'Following', 'Ссылка'])
