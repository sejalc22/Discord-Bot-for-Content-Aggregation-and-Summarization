# -- coding: utf-8 --
"""
Module to format message in form Header -> Link -> Summary
"""

from summarization import summarize

def to_string(input_dict, name):
    #Converts dict to string of Header, Link and Summary 
    result=[]
    word=""
    
    links=input_dict['links']
    texts=input_dict['texts']
    headers=input_dict['headers']
    
    
    for link,header,article in zip(links,headers,texts):
        word=""
        word+=("---------{}----------\n".format(name))
        word+=(link+"\n")
        word+=("->"+header+"\n")
        word+=(summarize(article)+"\n")
        result.append(word)
    print(result)
    return result

#Returns a list of news with each string consisting of Header, Link and Summary.
def international_news(news_dict):
    result=[]
    result+=(to_string(news_dict['bbc'],"BBC"))
    result+=(to_string(news_dict['guardian'],"Guardian"))
    result+=(to_string(news_dict['reuters'],"Reuters"))
    return result
def business_news(news_dict):
    result=[]
    result+=(to_string(news_dict['guardian'],"Guardian"))
    result+=(to_string(news_dict['financialexpress'],"FinancialExpress"))
    result+=(to_string(news_dict['bbc'],"BBC"))
    return result
def indian_news(news_dict):
    result=[]
    result+=(to_string(news_dict['toi'],"TOI"))
    result+=(to_string(news_dict['firstpost'],"FirstPost"))
    result+=(to_string(news_dict['thequint'],"TheQuint"))
    return result
def sports_news(news_dict):
    result=[]
    result+=(to_string(news_dict['espn'],"ESPN"))
    result+=(to_string(news_dict['guardian'],"Guardian"))
    return result