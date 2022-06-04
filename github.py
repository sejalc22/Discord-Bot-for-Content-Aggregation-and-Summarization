"""
Module to get top trending topics on github and top repositories from particular topic
"""

import requests
from bs4 import BeautifulSoup

topics_url='https://github.com/topics'
response=requests.get(topics_url)
page_contents=response.text
doc= BeautifulSoup(page_contents,'html.parser')
li_tags=doc.find_all('li',class_='d-inline-block')

def get_trending_topics():
    trending_topics=[]
    for i in li_tags:
        trending_topics.append(i.text.strip())
    #return trending_topics
    str_menu=print_menu(trending_topics)
    return str_menu


#printing the menu
def print_menu(trending_topics):
    menu=''
    print('Trending topics on github:')
    counter=0
    for i in trending_topics:
        counter=counter+1
        menu=menu + (str(counter)+' -> '+i+' \n')
    return menu


#get all topic links
def get_topic_links(li_tags):
    a_tag_list=[]
    for i in range(len(li_tags)):
        a_tag_list.append(li_tags[i].find_all('a',class_='topic-tag topic-tag-link f6 my-1'))
    trending_topic_url=[]
    base_url='https://github.com'
    for i in a_tag_list:
        trending_topic_url.append(base_url+i[0]['href'])
    return trending_topic_url



#get repo links of topic chosen
def get_repo_links(index_of_topic):
    trending_topic_url=get_topic_links(li_tags)
    link_to_be_extracted=trending_topic_url[index_of_topic-1]

    response=requests.get(link_to_be_extracted)
    topic_doc=BeautifulSoup(response.text,'html.parser')

    repo_tags=topic_doc.find_all('h3',class_='f3 color-fg-muted text-normal lh-condensed')

    counter=0
    final_list='Top repository links:\n'

    while(counter<5):
        repo_url='https://github.com'+ repo_tags[counter].find_all('a')[1]['href']
        counter=counter+1
        final_list=final_list+str(counter)+' -> '+repo_url+' \n'

    print('final_list : ', final_list)
    return final_list
