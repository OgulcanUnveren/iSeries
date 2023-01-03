#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import os
import shutil
import traceback
import time
URL = 'https://yabancidizi.co/kesfet'
def getsezonvebolum(page,title):
    soup = BeautifulSoup(page.content, 'html.parser')
    #results = soup.findAll("h2", {"class": "truncate"})
    dom = etree.HTML(str(soup))
    cats = dom.xpath ('//*[@id="seasons-menu"]/div/a/@href')
    i = 1
    epss = 1
    for sezon in cats:
        print("Sezon "+str(i)+"\n")
        print(str(sezon)+"| sending values")
        data = {
                
                "title":str(title),
                "seasondata":str(title) + " " + "Sezon "+str(i),
                "sequence":str(i),
            }
        print(data)
        
        x = requests.post("http://localhost:8000/series/seasonadd/" ,data=data)
        
        print(x.status_code)
        print(x.text)
        time.sleep(3)
        page = requests.get("https://yabancidizi.co/"+str(sezon))
        soup = BeautifulSoup(page.content, 'html.parser')
    #results = soup.findAll("h2", {"class": "truncate"})
        dom = etree.HTML(str(soup))
        eps = dom.xpath ('//*[@id="table-episodes-title"]/h6/a')
        for ep in eps:
            
            
            data = {
                
                "episode_title":"Dizi Bölüm"+str(epss)+":"+ep.text,
                'episode_slug':slugmake(str(ep.text)),
                'episode_position':epss,
                "seasondata":str(title) + " " + "Sezon "+str(i),
                
            }
            print(data)
        
            x = requests.post("http://localhost:8000/series/addepisode/" ,data=data)
            print(x.status_code)
            print(x.text)
            time.sleep(3)
            epss+=1
        i+=1
        epss = 1

def getpageinfo(page):

    soup = BeautifulSoup(page.content, 'html.parser')
    #results = soup.findAll("h2", {"class": "truncate"})
    dom = etree.HTML(str(soup))
    pi = 1
    
    
    while pi < 13:
        try:
            cat_array = []
            param = "["+str(pi)+"]"
            title = dom.xpath ('//*[@id="discover-response"]/ul/li{}/div[1]/div/div/div/a/h2'.format(param))
            desc = dom.xpath ('//*[@id="discover-response"]/ul/li{}/div[1]/div/p'.format(param))
            print("title:"+title[0].text+"\n")
            print("slug:"+slugmake(title[0].text)+"\n")
            print("desc:"+desc[0].text+"\n")
            cats = dom.xpath('//*[@id="discover-response"]/ul/li{}/div[1]/div/div/div/p/span[1]'.format(param))
            lin = dom.xpath('//*[@id="discover-response"]/ul/li{}/div[1]/div/div/div/a/@href'.format(param))
            lin = "https://yabancidizi.co/"+str(lin[0])
            print("link:"+str(lin))
            page = requests.get(str(lin))
              
            sess = requests.Session()
            r = sess.get("http://localhost:8000")
            my_csrf_token = r"sadasdasd"

            images = dom.xpath('//*[@id="discover-response"]/ul/li{}/div[1]/a/img/@src'.format(param))
#            # to save it locally

# ## Set u   p the image URL and filename
            image_url = "https://yabancidizi.co/"+str(images[0])
            filename = slugmake(title[0].text)+".jpg"

# # Open t   he url image, set stream to True, this will return the stream content.
            r = requests.get(image_url, stream = True)

# # Check    if the image was retrieved successfully
            if r.status_code == 200:
#     # Se   t decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
    
#     # Op   en a local file with wb ( write binary ) permission.
                with open(filename,'wb') as f:
                    shutil.copyfileobj(r.raw, f)
        
                print('Image successfully Downloaded: ',filename)
            else:
                print('Image Couldn\'t be retreived')


            data = {
                
                "title":title[0].text,
                "slug":slugmake(title[0].text),
                "desc":desc[0].text,
                "cat_title":cats[0].text,
            }
            files = {'serie_image': open(filename,'rb')}
            print(data)
            

            x = requests.post("http://localhost:8000/series/bulkadd/", files=files ,data=data)
           # print(requests.Request('POST',"http://localhost:8000/series/bulkadd/", files=files ,data=data).prepare().body.decode('ascii'))
            print(x.status_code)
            print(x.text)
            print("------sezona geldim\n-------")
            getsezonvebolum(page,title[0].text)
            time.sleep(5)
#                   
        except:
            traceback.print_exc()
        finally:
            pi+=1
        
    

def getcats(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    #results = soup.findAll("h2", {"class": "truncate"})
    dom = etree.HTML(str(soup))
    cats = dom.xpath ('//*[@id="filter-sidebar"]/div[8]/div/div/a/h2')
    for cat in cats:
        print("cat:"+cat.text)
        sess = requests.Session()
        r = sess.get("http://localhost:8000")
        my_csrf_token = r"sadasdasd"
        print(my_csrf_token)
        data = {
            "csrfmiddlewaretoken": my_csrf_token,
            "cat_title":cat.text,
        }

        x = requests.post("http://localhost:8000/series/bulkcatadd/", data = data)
        print(x.status_code)
        print(x.text)
    



def slugmake(text):
    text = text.replace(" ","-")
    text = text.replace("/","-")
    text = text.lower()
    return text
def runit():
    i = 1
    while i <= 212:
        page = requests.get(URL+"/"+str(i))
        getpageinfo(page)
        i+=1
    
def runcats():
    page = requests.get(URL)
    getcats(page)   

runit()



runframe()