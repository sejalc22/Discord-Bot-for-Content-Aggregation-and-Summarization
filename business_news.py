# -- coding: utf-8 --
"""
- module to scrape business news articles from websites :
        "https://www.theguardian.com/business/all",
        "https://www.financialexpress.com",
        "https://www.bbc.com/news/business",
- uses beautifulsoup to scrape links for articles from these website pages

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
urls = ("https://www.theguardian.com/business/all",
        "https://www.financialexpress.com",
        "https://www.bbc.com/news/business")

def get_news() :
    
    soup = get_soup(urls[0])
    result_dict['guardian'] = get_links_guardian(soup)
    
    res_list = {"links":[], "headers":[],"texts":[]}
    for section in ["/market/", "/money/", "/economy/"] :
        url = urls[1] + section
        soup = get_soup(url) 
        result = get_links_financialexpress(soup, section)
        res_list["links"].extend(result["links"])
        res_list["headers"].extend(result["headers"])
        res_list["texts"].extend(result["texts"])
    result_dict['financialexpress'] = res_list    
    
    soup = get_soup(urls[2])
    result_dict['bbc'] = get_links_bbc(soup, urls[2])
    
    return result_dict
    
def get_soup(url) :
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")    
    return soup


def get_links_guardian(soup):   
    res_list = {"links":[], "headers":[],"texts":[]}
    containers = soup.find_all("div", class_= "fc-item__container")
    for container in containers:
        link = container.find("a", href=True)['href']
        if(link[28:36] == "business"):
            res_list["links"].append(link)
        
    for url in res_list["links"]:
        article = get_article_guardian(url)
        res_list["headers"].append(article[0])  
        res_list["texts"].append(article[1])  
    return res_list

def get_article_guardian(url):
    res_list=[]
    soup=get_soup(url)
    
    header=soup.find("h1").text.strip().strip('\n').strip('\t')
   
    paras=soup.find("div",class_="dcr-1jw1u7l").find_all("p")
    for p in paras:
        res_list.append(p.text.strip().strip('\n').strip('\t'))
    return header, "".join(res_list)


def get_links_bbc(soup, url):
    res_list = {"links":[], "headers":[],"texts":[]}
    
    headline = soup.find("a", class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-paragon-bold gs-u-mt+ nw-o-link-split__anchor")
    link = headline['href']
    if(link[:len("/news/business")] == "/news/business"):
        res_list['links'].append("https://www.bbc.com" + link)
        
    block = soup.find("div", class_="gel-layout gel-layout--equal")
    links = block.find_all("a", class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor" )
    for link in links :
        if(link['href'][:len("/news/business")] == "/news/business"):
            res_list['links'].append("https://www.bbc.com" + link['href'])
            
    blocks = soup.find_all("div", class_="nw-c-5-slice gel-layout gel-layout--equal b-pw-1280")

    for block in blocks :
        links = block.find_all("a", class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor" )
        for link in links :
            if(link['href'][:len("/news/business")] == "/news/business"):
                res_list['links'].append("https://www.bbc.com" + link['href'])
        
    for url in res_list['links']:
        article = get_article_text_bbc(url)
        res_list["headers"].append(article[0])
        res_list["texts"].append(article[1]) 
    return res_list

def get_article_text_bbc(url):
    soup=get_soup(url)
    res_list=[]
    
    header=soup.find(attrs={"id":"main-heading"}).text.strip().strip('\n').strip('\t')      #,class_="ssrcss-s5w35y-HeadingWrapper e1nh2i2l5").text
   
    sub_soup=soup.find_all(attrs={"data-component":"text-block"})
    
    for i in sub_soup:
        res_list.append(i.text.strip().strip('\n').strip('\t'))
    return header, "".join(res_list)


def get_links_financialexpress(soup, section):   
    res_list = {"links":[], "headers":[],"texts":[]}
    links = soup.find_all("a", rel= "bookmark")
    for link in links:
        link = link['href']        
        if(link not in res_list and section in link) :            
            res_list["links"].append(link)
            
    for url in res_list["links"]:
        article = get_article_financialexpress(url)
        res_list["headers"].append(article[0])
        res_list["texts"].append(article[1])
       
    return res_list

def get_article_financialexpress(url):
    soup=get_soup(url)
    res_list=[]
    
    header=soup.find("h1", class_="wp-block-post-title").text.strip().strip('\n').strip('\t')
    
    content = soup.find("div", id="pcl-full-content")
    for p in content.find_all("p") :
        res_list.append(p.text.strip().strip('\n').strip('\t'))

    return header, "".join(res_list).strip().strip('\n').strip('\t')
        