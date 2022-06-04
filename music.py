"""
Module to get today's top songs and playlists from Jio Saavn platform
"""

import requests
from bs4 import BeautifulSoup


topics_url='https://www.jiosaavn.com/new-releases/english'
playlists_url='https://www.jiosaavn.com/featured-playlists/english'

def music():
    response=requests.get(topics_url)
    r2=requests.get(playlists_url)

    page_contents=response.text
    page_contents2=r2.text

    doc= BeautifulSoup(page_contents,'html.parser')
    doc2= BeautifulSoup(page_contents2,'html.parser')
    a_tags=doc.find_all('a',class_='u-ellipsis u-color-js-gray')
    a_playlist_tags=doc2.find_all('a',class_='u-ellipsis u-color-js-gray')

    counter=1
    string1='___Top 10 Trending Songs___\n'
    for i in a_tags[:10]:
        string1=string1+str(counter)+' -> '+i.text+'\n'
        counter=counter+1

    counter=1
    string2='___Top 10 Trending Playlists___\n'
    for i in a_playlist_tags[:10]:
        string2=string2+str(counter)+' -> '+i.text+'\n'
        counter=counter+1
   
    return string1,string2 
