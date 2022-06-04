# -*- coding: utf-8 -*-
"""

"""
import requests
from bs4 import BeautifulSoup
import articleFormatting

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

result_dict = {}

urls = ("https://www.theguardian.com/uk/sport", "https://www.espn.in")

def get_news() :
    result_dict['guardian'] = process_guardian(get_soup(urls[0]))
    result_dict['espn'] = process_espn(get_soup(urls[1]), urls[1])
    return result_dict

def get_soup(url) :
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")    
    return soup

def process_guardian(soup):   
    res_list = {"links":[], "headers":[],"texts":[]}
  
    section = soup.find("section", id= "news-and-features")
    items = section.find_all("div", class_= "fc-item__container")
    for item in items:
        res_list["links"].append(item.find("a", href=True)['href'])  
        
    section = soup.find("section", id= "catch-up")
    items = section.find_all("div", class_= "fc-item__container")
    for item in items:
        res_list["links"].append(item.find("a", href=True)['href'])  
        
    for url in res_list['links']:
        article = get_article_guardian(url)
        res_list["headers"].append(article[0])
        res_list["texts"].append(article[1]) 
        
    return res_list

def get_article_guardian(url) :
    res_list=[]
    soup=get_soup(url)
    header=soup.find("h1").text.strip().strip('\n').strip('\t')
   
    div=soup.find("div",class_="dcr-1jw1u7l")
    if(div != None) :
        paras = div.find_all("p")
        for p in paras:
            res_list.append(p.text.strip().strip('\n').strip('\t'))
        
    return header, "".join(res_list)

def process_espn(soup, url):   
    res_list = {"links":[], "headers":[],"texts":[]}
  
    items = soup.find_all("a", href = True)
    for item in items:
        if(item.has_attr("data-id")) :
            res_list["links"].append(url+item['href'])  
        
    for url in res_list['links']:
        article = get_article_espn(url)       
        res_list["headers"].append(article[0])
        res_list["texts"].append(article[1]) 
    
    return res_list

def get_article_espn(url) :
    res_list=[]
    soup=get_soup(url)
    
    header=soup.find("header", class_="article-header")
    if header != None :
        header=header.text.strip().strip('\n').strip('\t')
        paras=soup.find("div",class_="article-body").find_all("p", recursive=False)
        for p in paras:
            if not p.has_attr("strong") :
                texts = p.find_all(text=True, recursive=False)
                for text in texts :
                    res_list.append(p.text.strip().strip('\n').strip('\t'))
            
    else :
        header=""
        
    return header, "".join(res_list)
