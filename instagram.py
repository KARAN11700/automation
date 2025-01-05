#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import feedparser
import requests
from bs4 import BeautifulSoup
#from PIL import Image
#from io import BytesIO
import openai  
import json
import os
from configparser import ConfigParser

config = ConfigParser()
config.read("config2.ini")

OPENAI_API_KEY = config.get("Keys","OPENAI_API_KEY_1")
access_token = config.get("keys", "access_token_1")


def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    return feed.entries

rss_feed_url = "https://news.google.com/rss/search?q=Business+News&hl=en-US&gl=US&ceid=US:en"
articles = fetch_rss_feed(rss_feed_url)

for article in articles:
    print(f"Title: {article.title}")
    print(f"Link: {article.link}")
    print(f"Published: {article.published}\n")

def extract_article_details(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the title of the article
    title = soup.find('title').get_text() if soup.find('title') else "No title found"
    
    # Extract the first 3 paragraphs of the article
    content = " ".join([p.get_text() for p in soup.find_all('p')[:3]])
    
    return title, content

article_url = "https://edition.cnn.com/2025/01/02/media/trump-new-orleans-attack-migrants-fox-news/index.html"

title, content = extract_article_details(article_url)

print("Title:", title)
print("Content:", content)

def generate_caption(content):
    openai.api_key = OPENAI_API_KEY
    prompt = f"Write a 2-3 sentence caption for the following content:\n\n{content}"
    response = openai.Completion.create(
        engine="text-davinci-003", #use 'gpt-4'  model also
        prompt=prompt,
        max_tokens=60
    )
    return response['choices'][0]['text'].strip()
)
#print(response)

config = ConfigParser()
config.read("config1.ini")
OPENAI_API_KEY = config.get("Keys", "OPENAI_API_KEY_1")


openai.api_key = OPENAI_API_KEY
prompt= "content"
try:
    response = openai.Image.create(
        prompt="content",
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    print(f"Generated Image URL: {image_url}")
except Exception as e:
    print(f"Error: {e}")

import requests

def upload_to_instagram(caption, image_url, access_token, instagram_account_id):
    upload_url = f"https://graph.facebook.com/v15.0/{instagram_account_id}/media"
    
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }

    try:
        response = requests.post(upload_url, data=payload)
        response.raise_for_status()
        media_id = response.json()["id"]
        publish_url = f"https://graph.facebook.com/v15.0/{instagram_account_id}/media_publish"
        publish_payload = {
            "creation_id": media_id,
            "access_token": access_token
        }
        
        publish_response = requests.post(publish_url, data=publish_payload)
        publish_response.raise_for_status()
        return "Image uploaded successfully"
    
    except requests.exceptions.RequestException as e:
        print(f"Error uploading to Instagram: {e}")
        return f"Error uploading to Instagram: {e}"

def main():
    rss_feed_url = https://news.google.com/rss/search?q=Business+News&hl=en-US&gl=US&ceid=US:en" 
    articles = fetch_rss_feed(rss_feed_url)
    
    for article in articles[:1]: 
        article_url = article.link
        title, content = extract_article_details(article_url)
        
        caption = generate_caption(content)
        #short_url = shorten_url(article_url)
        #full_caption = f"{caption} Read more: {short_url}"
        
        image_url = generate_image(content)
        status_code = upload_to_instagram(caption, image_url)
        
        if status_code == 200:
            print(f"Successfully uploaded article: {title}")
        else:
            print(f"Failed to upload article: {title}")

if __name__ == "__main__":
    main()

