# -*- coding: utf-8 -*-
"""
Created on Sun May 29 15:45:06 2022

@author: Admin
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
urls = (
        "https://www.bbc.com/news/world",
        "https://www.theguardian.com/world",
        "https://www.reuters.com/world/the-great-reboot/"
        )

def get_news():
    soup = get_soup(urls[0])
    result_dict['bbc'] = process_bbc(soup, urls[0])
    
    soup = get_soup(urls[1])
    result_dict['guardian'] = process_guardian(soup, urls[1])
    
    soup = get_soup(urls[2])
    result_dict['reuters'] = process_reuters(soup, urls[2])
    return result_dict
    
def get_soup(url) :
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")    
    return soup

def process_bbc(soup, url):
    res_list={"links":[],"headers":[],"texts":[]}
    sub_soup=soup.find("div",class_="gel-layout__item gel-1/1 gel-3/5@xxl gs-u-display-none@xl gs-u-display-block@xxl")
    #print(sub_soup)
    links=sub_soup.find_all("div", class_="gel-layout__item gs-u-pb+@m gel-1/3@m gel-1/4@xl gel-1/3@xxl nw-o-keyline nw-o-no-keyline@m")
    for i in links:
        res_list['links'].append("https://www.bbc.com"+i.find("a",href=True)['href'])
    for url in res_list['links']:
        header,article=extract_text_bbc(url)
        res_list["headers"].append(header)
        res_list["texts"].append(article)
    return res_list

def extract_text_bbc(url):
    soup=get_soup(url)
    res_list=[]
    
    header=soup.find("h1").text        
    #res_list.append("Heading: "+header+".")
    
    sub_soup=soup.find_all(attrs={"data-component":"text-block"})
    
    for i in sub_soup:
        res_list.append(i.text)
        
    return header," ".join(res_list)

def process_guardian(soup, url):   
    res_list={"links":[],"headers":[],"texts":[]}
    sub_soup=soup.find("div", class_="js-tab-1 tabs__pane u-cf")
    containers=sub_soup.find_all("li")
    
    for container in containers:
        res_list["links"].append(container.find("a",href=True)['href'])
    for url in res_list["links"]:
        header,article=extract_guardian(url)
        res_list["headers"].append(header)
        res_list["texts"].append(article)  
    return res_list

def extract_guardian(url):
    res_list=[]
    soup=get_soup(url)
    
    header=soup.find("h1").text
    # res_list.append("Header: "+header+".")
    
    try:
        sub_soup=soup.find("div",class_="dcr-j7ihvk").find_all("p")
        for i in sub_soup:
            res_list.append(i.text.strip())
    except:
        pass
        
    return header," ".join(res_list)

def process_reuters(soup, url):   
    res_list={"links":[],"headers":[],"texts":[]}
    #
    sub_soup=soup.find("div",class_="content-layout__three_and_one_column__3MydJ")
    containers=sub_soup.find_all("div",attrs={"data-testid":"MediaStoryCard"})
    
    for container in containers:
        res_list["links"].append("https://www.reuters.com/"+container.find("a",attrs={"data-testid":"Heading"},href=True)['href'])
        
    for url in res_list["links"]:
        header,article=extract_reuters(url)
        res_list["headers"].append(header)
        res_list["texts"].append(article)
    #print(res_list['links'])
    return res_list

def extract_reuters(url):
    res_list=[]
    soup=get_soup(url)
    
    header=soup.find("h1").text
    #res_list.append("Heading:"+header+".")
    try:
        sub_soup=soup.find("div",class_="article-body__content__17Yit paywall-article").find_all("p")
        for i in sub_soup:
            res_list.append(" "+i.text.strip())
    except:
        print("error")
        pass
        
    return header, "".join(res_list)


# #helper function to check our output (A sample of 5)
# def display_5results(name):
#     count=0
#     result=get_news()[name]
#     ret1=result["links"] #its a dictionary
#     ret2=result["texts"] #its a dictionary
#     ret3=result["headers"]
    
#     for i,j,k in zip(ret1,ret3,ret2):
#         count+=1
#         print(i+"\n"+j+"\n"+k)
#         if(count==5):
#             break



# res_list=get_news()
# res_str=articleFormatting.international_news(res_list)
# print(res_str)
   
    
        
    