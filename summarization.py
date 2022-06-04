# -- coding: utf-8 --
"""
Created on Sun May 29 19:30:24 2022

@author: Admin
"""

# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

#function to clean and clear quotes
def clear_quotes(text, word_list):
    new_list=[]
    for i in word_list:
        char_text=list(i)
#     print(char_text)
        for j in char_text: 
#         print(j)
            if(j=='“' or j=='”' or j=='\\n' ):
                idx_j=char_text.index(j)
                char_text[idx_j]=' '
#               print("here")
        new_list.append(''.join(char_text))
    return ' '.join(new_list)

def summarize(text):

    summary = ''
    text= clear_quotes(text,text.split())        #function defined by us

    # Tokenizing the text
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    

    # Creating a frequency table to keep the 
    # score of each word

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()
    
    # for sentence in sentences:
    #     if("Heading:" in sentence):
    #         sentences.remove(sentence)
    #         summary+="*"+sentence.replace("Heading:","")+"*\n"

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq   
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    try:
        # Average value of a sentence from the original text
        average = int(sumValues / len(sentenceValue))
        # Storing sentences into our summary.
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.6 * average)):
                summary += " " + sentence
    except:
        pass
    
    if(len(summary)>1600):
        summary=summary[0:1600]+"..."
    #functions
    #commented out print statements are for detecting runtime errors
    return summary
