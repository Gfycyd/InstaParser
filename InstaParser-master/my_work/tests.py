from django.test import TestCase

# Create your tests here.
import excel_writer
import my_work.insta_parser as parser
def test_create():
    excel_writer.create_list('https://docs.google.com/spreadsheets/d/17yrMltdIA4UOPePk5ZDSjPhHbhqi3-w6X9Zuby198OU/edit#gid=0', 'test1')
def test_hashtag_search():
    parser.search("hashtag", 'шугаринг', "https://docs.google.com/spreadsheets/d/1deGTmHr8QI2mslRIHFmzotVQyGcUBdgUxmquJu0B2Tk/edit#gid=1989556831", '7')
def test_login_search():
    parser.search("login", 'katya', "https://docs.google.com/spreadsheets/d/1deGTmHr8QI2mslRIHFmzotVQyGcUBdgUxmquJu0B2Tk/edit#gid=1989556831", 7)