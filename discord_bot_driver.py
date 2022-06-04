# -- coding: utf-8 --
"""
Module that drives discord bot
url to add bot to server : 
    https://discord.com/api/oauth2/authorize?client_id=975339401037103154&permissions=534723950656&scope=bot
chromedriver path :
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    
    parent directory : D:\Ishani\College\TYSem2\JOCP\miniproject\bot
"""

import nest_asyncio
nest_asyncio.apply()

import discord
import recipes
import movie_scraping
import jokes
import articleFormatting
import business_news
import international_news
import india_politics
import sports_news
import music
import github
import random

# TOKEN = "OTU4MzI4NTIwODIyNjQwNjUx.YkLu_A.Hp3fgou6dyUgLKXr3jlSpOeKlto"
TOKEN = "OTc1MzM5NDAxMDM3MTAzMTU0.G61nqV.xYx-HqDEdGjCzr6DpRMLyAzMqdFkuMcAjqLnAY"
PATH = "C:\Program Files (x86)\chromedriver.exe"

BASE_MENU = """
->->->

-> Type "news" to get summarized news articles!

-> Type "recipes" to get recipe suggestions!

-> Type "movies" to get movie recommendations!

-> Type "github" to get links to top repositories from trending topics!

-> Type "jokes" if you'd like me to tell you a joke!

-> Type "music" to find out today's trending songs and playlists!

->->->
"""

NEWS_FOLLOW_UP = """
Serving summarized news articles!

-> Type "business" if you'd like to read the latest business news

-> Type "international" if you'd like to read the latest world news

-> Type "indian politics" if you'd like to read the latest political news

-> Type "sports" if you'd like to read the latest sports news
"""

RECIPES_FOLLOW_UP = "What do you want to cook today?"
MOVIES_FOLLOW_UP = "Enter your preference of genres in the form of a comma separated list : Action/Adventure/Comedy/Drama/History/Horror/Mystery"
GITHUB_FOLLOW_UP = "Enter appropriate index to view top repositories of the topic!"
GREETING_MSG = "Hello! I'm your content aggregation bot!"
PARTING_MSG = "Wake me up by saying 'hey bot', whenever you need me!"
INVALID_RESPONSE_MSG = "I don't understand what you're saying, sorry!"
PROCESSING_MSG = "Hang on, this may take a bit of time!"
NO_RES_MSG = "I'm afraid I could not find any results for you!"

global first_message            
first_message = True

class MyClient(discord.Client):
    
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))

    async def on_message(self,message):

        if message.author == client.user:
            return
        
        global first_message
        if first_message :
            await message.channel.send(GREETING_MSG)
            await message.channel.send(PARTING_MSG)            
            first_message = False
            return
                 
        user_msg_history = []
        bot_msg_history = []
        
        history_thread = message.channel.history(limit = 20)

        async for msg in history_thread:
            if (msg.author == client.user):
                bot_msg_history.append(msg)
            else:
                user_msg_history.append(msg)
                
        current_user_msg = str(user_msg_history[0].content)
        last_bot_msg = str(bot_msg_history[0].content.strip())
        
        """
        This means that the bot completed one cycle (served some content in last bot message and interaction ended) 
        and now is being called again from the top ==>
        """
        
        if (last_bot_msg != BASE_MENU.strip() 
            and last_bot_msg != NEWS_FOLLOW_UP.strip() 
            and last_bot_msg != RECIPES_FOLLOW_UP.strip() 
            and last_bot_msg != MOVIES_FOLLOW_UP.strip() 
            and last_bot_msg != GITHUB_FOLLOW_UP.strip()) :
            
            if current_user_msg.lower().strip() == "hey bot" :
                await message.channel.send(GREETING_MSG + "\n")
                await message.channel.send(BASE_MENU)
            return
        
        """
        At this point in the code, we know that an interaction is ongoing
        """
        active_user = ""
        active_thread = []
        
        """
        Find out with which user the interaction is ongoing (active_user) ==>
        """
        
        for msg in user_msg_history :
            if msg.content.lower().strip() == 'hey bot' :
                active_user = msg.author
                break
                
        """
        If the author of the current message isn't the active_user then ignore message and return
        """
        if active_user != message.author :
            return
        """
        Get the active_user's past messages
        """
        
        for msg in user_msg_history :
            if msg.author == active_user :
                active_thread.append(msg)
                
        current_msg = str(active_thread[0].content.lower())
        
        if last_bot_msg == BASE_MENU.strip() :            
            if current_msg == "news" :
                await message.channel.send(NEWS_FOLLOW_UP)
            elif current_msg == "recipes" :
                await message.channel.send(RECIPES_FOLLOW_UP)
            elif current_msg == "movies" :
                await message.channel.send(MOVIES_FOLLOW_UP)
            elif current_msg == "jokes" :
                await message.channel.send("Here's one : " + "\n")
                await message.channel.send(str(jokes.dad_joke()))
                await message.channel.send("Hope it made you laugh out loud!")
            elif current_msg == "github" :                
                await message.channel.send(github.get_trending_topics())
                await message.channel.send(GITHUB_FOLLOW_UP)
            elif current_msg == "music" :
                await message.channel.send(PROCESSING_MSG)                
                results = music.music()
                await message.channel.send("Here's your music update!")
                await message.channel.send(results[0])
                await message.channel.send(results[1])
            else :
                await message.channel.send(INVALID_RESPONSE_MSG)
                
        elif last_bot_msg == NEWS_FOLLOW_UP.strip() :
            try :
                if current_msg == "business" :
                    await message.channel.send('Getting business news')
                    await message.channel.send(PROCESSING_MSG)
                    news = business_news.get_news()
                    results = {"bbc" : {}, "guardian": {}, "financialexpress": {}}

                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['guardian']['links'])), 3)            
                    for i in ind :
                        result_dict["links"].append(news['guardian']['links'][i])
                        result_dict["headers"].append(news['guardian']['headers'][i])
                        result_dict["texts"].append(news['guardian']['texts'][i])
                    results['guardian'] = result_dict
                    
                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['bbc']['links'])), 3)                
                    for i in ind :
                        result_dict["links"].append(news['bbc']['links'][i])
                        result_dict["headers"].append(news['bbc']['headers'][i])
                        result_dict["texts"].append(news['bbc']['texts'][i])
                    results['bbc'] = result_dict
                    
                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['financialexpress']['links'])), 3)            
                    for i in ind :
                        result_dict["links"].append(news['financialexpress']['links'][i])
                        result_dict["headers"].append(news['financialexpress']['headers'][i])
                        result_dict["texts"].append(news['financialexpress']['texts'][i])
                    results['financialexpress'] = result_dict
                                    
                    msg_list = articleFormatting.business_news(results)
                    print(len(msg_list))
                    print('\n\n')
                    for msg in msg_list:
                        await message.channel.send(msg)
                    await message.channel.send("Here you go!")
                    
                elif current_msg == "international" :
                    await message.channel.send('Getting international news')
                    await message.channel.send(PROCESSING_MSG)
                    news = international_news.get_news()     
                    results = {"bbc" : {}, "guardian": {}, "financialexpress": {}}

                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['guardian']['links'])), 3)            
                    for i in ind :
                        result_dict["links"].append(news['guardian']['links'][i])
                        result_dict["headers"].append(news['guardian']['headers'][i])
                        result_dict["texts"].append(news['guardian']['texts'][i])
                    results['guardian'] = result_dict
                    
                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['bbc']['links'])), 3)                
                    for i in ind :
                        result_dict["links"].append(news['bbc']['links'][i])
                        result_dict["headers"].append(news['bbc']['headers'][i])
                        result_dict["texts"].append(news['bbc']['texts'][i])
                    results['bbc'] = result_dict
                    
                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['reuters']['links'])), 3)            
                    for i in ind :
                        result_dict["links"].append(news['reuters']['links'][i])
                        result_dict["headers"].append(news['reuters']['headers'][i])
                        result_dict["texts"].append(news['reuters']['texts'][i])
                    results['reuters'] = result_dict
                    
                    msg_list = articleFormatting.international_news(results)
                    print(len(msg_list))
                    print('\n\n')
                    for msg in msg_list:
                        await message.channel.send(msg)
                        
                    await message.channel.send("Here you go!")
                    
                elif current_msg == "indian politics" :
                    await message.channel.send('Getting indian politics news')
                    await message.channel.send(PROCESSING_MSG)
                    news = india_politics.get_news()
                    results = {"toi" : {}, "firstpost": {}, "thequint": {}}

                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['toi']['links'])), min(3, len(news['toi']['links'])))            
                    for i in ind :
                        result_dict["links"].append(news['toi']['links'][i])
                        result_dict["headers"].append(news['toi']['headers'][i])
                        result_dict["texts"].append(news['toi']['texts'][i])
                    results['toi'] = result_dict
                    
                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['firstpost']['links'])), min(3, len(news['toi']['links'])))                
                    for i in ind :
                        result_dict["links"].append(news['firstpost']['links'][i])
                        result_dict["headers"].append(news['firstpost']['headers'][i])
                        result_dict["texts"].append(news['firstpost']['texts'][i])
                    results['firstpost'] = result_dict
                    
                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['thequint']['links'])), min(3, len(news['toi']['links'])))            
                    for i in ind :
                        result_dict["links"].append(news['thequint']['links'][i])
                        result_dict["headers"].append(news['thequint']['headers'][i])
                        result_dict["texts"].append(news['thequint']['texts'][i])
                    results['thequint'] = result_dict        
                    
                    msg_list = articleFormatting.indian_news(results)
                    print(len(msg_list))
                    print('\n\n')
                    for msg in msg_list:
                        await message.channel.send(msg)
                        
                    await message.channel.send("Here you go!")
                    
                elif current_msg == "sports" :
                    await message.channel.send('Getting sports news')
                    await message.channel.send(PROCESSING_MSG)
                    news = sports_news.get_news()
                    results = {"espn" : {}, "guardian": {}}

                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['guardian']['links'])), 3)            
                    for i in ind :
                        result_dict["links"].append(news['guardian']['links'][i])
                        result_dict["headers"].append(news['guardian']['headers'][i])
                        result_dict["texts"].append(news['guardian']['texts'][i])
                    results['guardian'] = result_dict
                    
                    result_dict = {"links":[], "headers":[],"texts":[]}
                    ind = random.sample(range(len(news['espn']['links'])), 3)                
                    for i in ind :
                        result_dict["links"].append(news['espn']['links'][i])
                        result_dict["headers"].append(news['espn']['headers'][i])
                        result_dict["texts"].append(news['espn']['texts'][i])
                    results['espn'] = result_dict
                    msg_list = articleFormatting.sports_news(results)
                    print(len(msg_list))
                    print('\n\n')
                    for msg in msg_list:
                        await message.channel.send(msg)
                        
                    await message.channel.send("Here you go!")

                else :
                    await message.channel.send(INVALID_RESPONSE_MSG)
            except Exception as e : 
                print(e)
                await message.channel.send(NO_RES_MSG)
                
        elif last_bot_msg == RECIPES_FOLLOW_UP.strip() :
            keywords = current_msg.strip()
            msg = 'Looking for '+ keywords + ' recipes'
            await message.channel.send(msg)
            await message.channel.send(PROCESSING_MSG)
            success, results = recipes.get_recipes(keywords, PATH)            
            
            if not success :
                await message.channel.send(NO_RES_MSG)
            else :
                result_msg = []
                len_b = len(results["bonappetit"])
                len_a = len(results["allrecipes"])

                for i in range(5) :
                    if not i > len_a :
                        result_msg.append(results["allrecipes"][i])
                    if not i > len_b :
                        result_msg.append(results["bonappetit"][i])   
                        
                if len(result_msg) == 0 :
                    await message.channel.send(NO_RES_MSG)
                
                else :
                    for msg in result_msg :
                        await message.channel.send(msg)
                        
                    await message.channel.send("Here you go!")                                
                        
        elif last_bot_msg == MOVIES_FOLLOW_UP.strip() :            
            await message.channel.send('Getting movie recommendations')
            await message.channel.send(PROCESSING_MSG)
            split = current_msg.split(',')
            genres = [genre.strip().lower() for genre in split]
            
            result_df, success = movie_scraping.get_movies(PATH, genres)
            if not success :
                await message.channel.send(NO_RES_MSG)
            else :
                for i in range(10) :                
                    results = list(result_df.loc[i])
                    msg = results[0] + " (" + results[1] + ") " + "\n" + results[2] + "% rating"
                    await message.channel.send(msg)

        elif last_bot_msg == GITHUB_FOLLOW_UP.strip() :
            try :                
                index = int(current_msg.strip())
                await message.channel.send("Getting top repositories!")
                if index not in range(1,11) :
                    await message.channel.send("Invalid index!")
                else :
                    await message.channel.send(str(github.get_repo_links(index)))
            except :
                await message.channel.send("Invalid index!")


client = MyClient()
client.run(TOKEN)