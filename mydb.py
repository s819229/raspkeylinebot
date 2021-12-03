import os
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import requests
from flask import Flask, request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


def Book_reservation():
    book_name = "暫定"
    book_number = "12345"
    now = datetime.datetime.today()
    date_ = str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    time_ = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    doc = {
        "username": username,
        'date': date_,
        'time': time_,
        '還書日期': "明天",
        "書名":book_name,
        "書籍編號":book_number,
    }
    collection_ref = db.collection("user")
    collection_ref.add(doc)

def get_chrome():
    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--headless")
    op.add_argument("--disable-dev-shm-usage")
    op.add_argument("--no-sandbox")
    op.add_argument('--disable-gpu')  #1119 add


    return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)    

def get_book():
    username=""
    password=""
    sskey='python'

    driver = webdriver.Chrome("chromedriver.exe")
    #driver = get_chrome()

    #driver.maximize_window()
    driver.get('https://www.library.ntpc.gov.tw/loginControl/')

    driver.find_element_by_class_name('card-login').click()
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("parole").send_keys(password)
    driver.find_element_by_class_name("btn.btn-primary").click()
    #sleep(1)
    #driver.find_element_by_xpath('//*[@id="hot-service"]/ul/li[1]/a').click()
    driver.get('https://webpac.tphcc.gov.tw/webpac/search.cfm')
    driver.find_element_by_id("ss_keyword").send_keys(sskey)
    driver.find_element_by_name("searchBtn").click()
    #sleep(1)
    #driver.get('https://webpac.tphcc.gov.tw/webpac/search.cfm?m=ss&k0='&sskey &'&list_num=100&current_page=1')

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    driver.quit()

    book_box=soup.select(".book-box")
    re='查詢結果\n'
    for i,book in enumerate(book_box):            
        re+=str(i)+'\t'
        re+= book.select('.cover')[0].find('a').get('title').replace("/", "") +'\n'        
        #r+=str(book.select('.cover')[0].find('a').get('title'))+'\n'
        #print('https://webpac.tphcc.gov.tw/webpac/'+ str(book.select('.cover')[0].find('a').get('href')))
        #print(book.select('.cover')[0].find('img').get('src'))    
    return re






