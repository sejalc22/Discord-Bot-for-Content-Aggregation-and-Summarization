# -*- coding: utf-8 -*-
"""
- module to find recipes based on user-entered keywords from bonappetit, allrecipes, and vegrecipesofindia
- uses selenium to enter keywords in search bar of the website
- scrapes recipe article links from the search results 
- also scrapes title and description of recipe card to display in reponse along with link

"""
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# SB : search box
# SR : search results

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36'
al ='en-US, en;q=0.5'
pp = 'interest-cohort=(*),accelerometer=(*),ambient-light-sensor=(*),autoplay=(*),battery=(*),camera=(*),cross-origin-isolated=(*),display-capture=(*),document-domain=(*),encrypted-media=(*),execution-while-not-rendered=(*),execution-while-out-of-viewport=(*),fullscreen=(*),geolocation=(*),gyroscope=(*),hid=(*),idle-detection=(*),magnetometer=(*),microphone=(*),midi=(*),navigation-override=(*),payment=(*),picture-in-picture=(*),publickey-credentials-get=(*),screen-wake-lock=(*),serial=(*),sync-xhr=(*),usb=(*),web-share=(*),xr-spatial-tracking=(*)'
    
def get_recipes(keyword_string, PATH) :
    
    successA = True
    successB = True
    urls = {"bonappetit":"https://www.bonappetit.com/",
            "allrecipes":"https://www.allrecipes.com/"}
    result_dict = {"bonappetit":[], "allrecipes":[]}
    
    try :
#------------------------------------------------------------------------------
        s = Service(PATH)
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument(f'user-agent={ua}, accept-language={al}, permissions-policy={pp}')
        driver = webdriver.Chrome(service = s, options = option)
#------------------------------------------------------------------------------
# enter keyword string in the search bar on bonappetit and get results

        driver.get(urls.get("bonappetit"))
        bonappetit_SB = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.ID, "search-form-text-field-q")))[1]
        bonappetit_SB.click()
        bonappetit_SB.send_keys(Keys.HOME)
        bonappetit_SB.send_keys(keyword_string)
        bonappetit_SB.send_keys(Keys.RETURN)
        
        res_msg = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "results-message")))
        if "Uh oh. We didn't find the search term" in  str(res_msg.text.strip()) :
            successA = False
            print(res_msg)
        
        else :
            bonappetit_SR = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "recipe-content-card")))
            
            for card in bonappetit_SR :
                title_link = card.text.splitlines()
                if len(title_link) > 2 :
                    title_link.pop(0)
                    title_link.pop(1)
                    
                    a = card.find_element(by = By.TAG_NAME, value = 'a')
                    title_link.append(str(a.get_attribute("href")))
                    
                    result_dict.get("bonappetit").append('\n'.join(tuple(title_link)))
#------------------------------------------------------------------------------

        driver.get(urls.get("allrecipes"))
        allrecipes_SB = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "search-block")))
        allrecipes_SB.click()
        allrecipes_SB.send_keys(Keys.HOME)
        allrecipes_SB.send_keys(keyword_string)
        allrecipes_SB.send_keys(Keys.RETURN)
        
        res_msg = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "search-results-total-results")))        
        if res_msg.text.strip().lower() == "0 results" :
            print(res_msg)
            successB = False
            
        else :
            allrecipes_SR = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card__detailsContainer")))
            for card in allrecipes_SR :
                title_link = []
                title_link.append(card.text.splitlines()[0])
                
                a = card.find_element(by = By.TAG_NAME, value = 'a')
                title_link.append(str(a.get_attribute("href")))
                
                result_dict.get("allrecipes").append('\n'.join(tuple(title_link)))
        
#------------------------------------------------------------------------------
        driver.close()
    
        success = successA or successB
    except Exception as e: 
        print("recipes_scraping :: get_recipes :: ", e)   
        print(traceback.format_exc())        
        success = False
    return success, result_dict   

    