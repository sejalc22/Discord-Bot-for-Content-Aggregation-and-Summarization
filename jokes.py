"""
Getting JSON response with random joke as attachment
"""

import requests
def dad_joke():
    response=requests.get('https://icanhazdadjoke.com/slack')
    res=response.json()
    return res['attachments'][0]['fallback']
