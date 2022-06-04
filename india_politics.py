# -*- coding: utf-8 -*-
"""
- module to scrape indian politics news articles from websites :
        "https://timesofindia.indiatimes.com/politics/news",
        "https://www.firstpost.com/category/politics",
        "https://www.thequint.com/news/politics/"
- uses beautifulsoup to scrape links for articles from these website pages

"""
import requests
import articleFormatting
from bs4 import BeautifulSoup

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

result_dict = {}

urls = ("https://timesofindia.indiatimes.com/politics/news",
        "https://www.firstpost.com/category/politics",
        "https://www.thequint.com/news/politics/")

def get_news() :
    result_dict['toi'] = get_links_toi(get_soup(urls[0]), urls[0])
    result_dict['firstpost'] = get_links_firstpost(get_soup(urls[1]))
    result_dict['thequint'] = get_links_thequint(get_soup(urls[2] + str(1)))
    result_dict['thequint']["links"].extend(get_links_thequint(get_soup(urls[2] + str(2)))["links"])
    result_dict['thequint']["headers"].extend(get_links_thequint(get_soup(urls[2] + str(2)))["headers"])
    result_dict['thequint']["texts"].extend(get_links_thequint(get_soup(urls[2] + str(2)))["texts"])

    return result_dict

def get_soup(url) :
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")    
    return soup

def get_links_toi(soup, url):   
    res_list = {"links":[], "headers":[],"texts":[]}
  
    list = soup.find("ul", class_="top-newslist")
    links = list.find_all("li")
    for link in links:
        res_list["links"].append(url + link.find("a", href=True)['href'])  
        
    for url in res_list['links']:
        article = get_article_toi(url)
        res_list["headers"].append(article[0])
        res_list["texts"].append(article[1]) 
        
    return res_list

def get_article_toi(url):
    soup=get_soup(url)
    
    header=soup.find("h1", class_="_23498").text.strip().strip('\n').strip('\t')
   
    text=soup.find("div", class_="ga-headlines").text.strip().strip('\n').strip('\t')
    
    return header, text

def get_links_firstpost(soup):   
    res_list = {"links":[], "headers":[],"texts":[]}
  
    list = soup.find_all("div", class_="big-thumb")    
    for card in list:
        res_list["links"].append(card.find("a", href=True)['href'])  
    
    for url in res_list['links']:
        article = get_article_firstpost(url)
        res_list["headers"].append(article[0])
        res_list["texts"].append(article[1])
        
    return res_list

def get_article_firstpost(url):
    soup=get_soup(url)
    text = []
    
    header=soup.find("h1", class_="inner-main-title").text.strip().strip('\n').strip('\t')
   
    paras=soup.find("div", class_="inner-copy article-full-content").find_all("p", recursive = False)
    paras.pop()
    paras.pop()
    for p in paras :
        text.append(p.text.strip().strip('\n').strip('\t'))
    
    return header, "".join(text)

def get_links_thequint(soup):   
    res_list = {"links":[], "headers":[],"texts":[]}
  
    headline = soup.find("a", class_="_1kbmI", href = True)
    link = headline['href']   
    if(link[30:38] == "politics") :
        res_list["links"].append(link)
    list = soup.find_all("a", class_="headline-link _3aBL6", href = True)
    for url in list:
        link = url['href']
        if(link[30:38] == "politics"):
            res_list["links"].append(link)  
    
    for url in res_list['links']:
        article = get_article_thequint(url)
        res_list["headers"].append(article[0])
        res_list["texts"].append(article[1])
        
    return res_list

def get_article_thequint(url):
    soup=get_soup(url)
    text = []
    
    header=soup.find("div", class_="headline").text.strip().strip('\n').strip('\t')
    paras=soup.find("div", id="story-body-wrapper").find_all("p")
    paras.pop()
    for p in paras :
        text.append(p.text.strip().strip('\n').strip('\t'))
    
    return header, "".join(text)