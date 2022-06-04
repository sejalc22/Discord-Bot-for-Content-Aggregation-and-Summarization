# -*- coding: utf-8 -*-
"""
- module to display movies based on user-entered keywords for genres
- uses selenium to interact with website
- scrapes top rate movie names

"""
from selenium import webdriver
import time, traceback
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

PATH = "C:\Program Files (x86)\chromedriver.exe"

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36'
al ='en-US, en;q=0.5'
pp = 'interest-cohort=(*),accelerometer=(*),ambient-light-sensor=(*),autoplay=(*),battery=(*),camera=(*),cross-origin-isolated=(*),display-capture=(*),document-domain=(*),encrypted-media=(*),execution-while-not-rendered=(*),execution-while-out-of-viewport=(*),fullscreen=(*),geolocation=(*),gyroscope=(*),hid=(*),idle-detection=(*),magnetometer=(*),microphone=(*),midi=(*),navigation-override=(*),payment=(*),picture-in-picture=(*),publickey-credentials-get=(*),screen-wake-lock=(*),serial=(*),sync-xhr=(*),usb=(*),web-share=(*),xr-spatial-tracking=(*)'


def get_movies(PATH, input_genre) :
    
    # input_genre = get_input_genre() #keyword_string.strip().split(",")
    success = True
    url="https://www.themoviedb.org/movie"
        
    try :
#------------------------------------------------------------------------------
        s = Service(PATH)
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument(f'user-agent={ua}, accept-language={al}, permissions-policy={pp}')
        browser = webdriver.Chrome(service = s,options = option)
        #service = s, 
        browser.get(url)

        filter_button=WebDriverWait(browser, 100).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id=\"media_v4\"]/div/div/div[2]/div[1]/div[2]/div[1]")))[0]
        filter_button.click()

#------------------------------------------------------------------------------
#       selecting genres by user input

        if("action" in input_genre):
            genre1 = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[1]"))) 
            action = ActionChains(browser)
            action.move_to_element(genre1).click().perform()
            #genre1.click()
            print("clicked action")
            time.sleep(3)
        if("adventure" in input_genre):
            genre2 = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[2]")))
            #genre2.click()
            action = ActionChains(browser)
            action.move_to_element(genre2).click().perform()
            time.sleep(3)
        if("comedy" in input_genre):
            genre3 = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[4]")))
            #genre3.click()
            action = ActionChains(browser)
            action.move_to_element(genre3).click().perform()
            print("clicked comedy")
            time.sleep(10)
        if("drama" in input_genre):
            genre4 = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[7]")))
            #WebDriverWait(browser, 100).until(EC.presence_of_all_elements_located(()))[0]
            action = ActionChains(browser)
            action.move_to_element(genre4).click().perform()
            time.sleep(3)
        if("history" in input_genre):
            genre5 = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[10]")))
            action = ActionChains(browser)
            action.move_to_element(genre5).click().perform()
            time.sleep(3)
        if("horror" in input_genre):
            genre6 = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[11]")))
            action = ActionChains(browser)
            action.move_to_element(genre6).click().perform()
            time.sleep(3)
        if("mystery" in input_genre):
            genre7 = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[13]")))
            action = ActionChains(browser)
            action.move_to_element(genre7).click().perform()
            time.sleep(3)

        print("done clicking")
#------------------------------------------------------------------------------
        #loading filtered movies
        time.sleep(3)
        search_result=browser.find_element_by_xpath("/html/body/div[1]/main/section/div/div/div/div[2]/div[1]/div[4]/p/a")#"//*[@id=\"media_v4\"]/div/div/div[2]/div[3]")
        search_result.click()      
        # action = ActionChains(browser)
        # action.move_to_element(search_result).click().perform()
        
        print("done loading")
#------------------------------------------------------------------------------
        #storing data form movie cards into dataframe
        
        card=[""]*10                    #store instance of card web element, because Stale exception
        percent=[""]*10                 #store instance of footer of card web element, because Stale exception
    
        df_list=[]                      #store list to create dataframe
    
        for i in range(len(card)):
            time.sleep(1)
            
            print("fetching data...")
            
            card[i]=browser.find_element_by_xpath("//*[@id=\"page_1\"]/div[{}]/div[2]".format(i+1))
            percent[i]=browser.find_element_by_xpath("//*[@id=\"page_1\"]/div[{}]/div[2]/div/div/div".format(i+1))
            
            movie_name=card[i].find_elements_by_tag_name("a")[0].text
            release_date=card[i].find_elements_by_tag_name("p")[0].text
            rating=percent[i].get_attribute("data-percent")
            
            df_list.append((movie_name,release_date,rating))
    
        df_movies = pd.DataFrame(df_list, columns =['Name', 'Date', 'Rating'])
        browser.close()
#------------------------------------------------------------------------------
    
    except Exception as e: 
        print("movie_scraping :: get_movies :: ",e)
        df_movies = pd.DataFrame([])
        success = False
    return df_movies, success
