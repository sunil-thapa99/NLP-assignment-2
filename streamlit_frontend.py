import streamlit as st
import nltk
nltk.download('punkt') # Download necessary tokenizer data for NLTK

# Import necessary NLTK libraries for text pre-processing
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle 
import pandas as pd
import re
import requests
import json

# Initialize NLTK's WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# # Define function for pre-processing user input
# def preprocess(text):
#     # Tokenize input text
#     tokens = word_tokenize(text.lower())
    
#     # Remove stop words from tokens
#     stop_words = set(stopwords.words('english'))
#     tokens = [token for token in tokens if token not in stop_words]
    
#     # Lemmatize tokens
#     tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
#     # Return pre-processed text as a string
#     return ' '.join(tokens)


def preprocess(textdata):
    processedText = []
    
    # Create Lemmatizer and Stemmer.
    wordLemm = WordNetLemmatizer()
    
    # Defining regex patterns.
    urlPattern        = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern       = '@[^\s]+'
    alphaPattern      = "[^a-zA-Z0-9]"
    sequencePattern   = r"(.)\1\1+"
    seqReplacePattern = r"\1\1"
    
    for tweet in textdata:
        tweet = tweet.lower()
        
        # Replace all URls with 'URL'
        tweet = re.sub(urlPattern,' URL',tweet)
              
        # Replace @USERNAME to 'USER'.
        tweet = re.sub(userPattern,' USER', tweet)        
        # Replace all non alphabets.
        tweet = re.sub(alphaPattern, " ", tweet)
        # Replace 3 or more consecutive letters by 2 letter.
        tweet = re.sub(sequencePattern, seqReplacePattern, tweet)

        tweetwords = ''
        for word in tweet.split():
            # Checking if the word is a stopword.
            #if word not in stopwordlist:
            if len(word)>1:
                # Lemmatizing the word.
                word = wordLemm.lemmatize(word)
                tweetwords += (word+' ')
            
        processedText.append(tweetwords)
        
    return processedText

def load_models():
    '''
    Replace '..path/' by the path of the saved models.
    '''
    
    # Load the vectoriser.
    file = open('../train/new-vectoriser-ngram-(1,2).pickle', 'rb')
    vectoriser = pickle.load(file)
    file.close()
    # Load the LR Model.
    file = open('../train/new-Sentiment-LR.pickle', 'rb')
    LRmodel = pickle.load(file)
    file.close()
    
    return vectoriser, LRmodel

def predict(vectoriser, model, text):
    # Predict the sentiment
    textdata = vectoriser.transform(preprocess(text))
    sentiment = model.predict(textdata)
    return sentiment
    # print(sentiment, '123123123123123123123')
    
    # # Make a list of text with sentiment.
    # data = []
    # for text, pred in zip(text, sentiment):
    #     data.append((text,pred))
        
    # # Convert the list into a Pandas DataFrame.
    # df = pd.DataFrame(data, columns = ['text','sentiment'])
    # df = df.replace([0,1], ["Negative","Positive"])
    # return df

# Define function for generating bot response
def generate_response(text):
    # Pre-process user input text
    vectoriser, model = load_models()
    preprocessed_text = predict(vectoriser, model, [text])
    return preprocessed_text if preprocessed_text else 'Hello, This is chatbot!'



def get_intent_name(message):
    url = 'http://localhost:5005/model/parse'
    r = requests.post(url, json={"text": message})
    intent_name = r.json()['intent']['name']
    return intent_name
    

# Create Streamlit app
def app():
    st.title('Chatbot')
    
    # Get user input text
    user_input = st.text_area('You: ')
    
    # Generate and display bot response
    button_clicked = st.button("Check response")
    if button_clicked:
        bot_response = generate_response(user_input)
        st.text_area('Bot:', value=bot_response, height=100)

# Run Streamlit app
if __name__ == '__main__':
    app()
