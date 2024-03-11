#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[2]:


from dotenv import load_dotenv, find_dotenv


# In[5]:


import base64


# In[19]:


import requests


# In[3]:


file_path = "/Users/preethamvignesh/Desktop/Savor/"
load_dotenv(file_path + ".env")


# In[4]:


from openai import OpenAI


# In[6]:


def image_encoder(path):
    with open(path, "rb"):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")


# In[7]:


local_img_path = "/Users/preethamvignesh/Desktop/Savor/Pepperoni-Pizza-Recipe-Sip-Bite-Go.jpg"
base64_encoded_img = image_encoder(local_img_path)


# In[8]:


openai_api_key = os.getenv("OPENAI_API_KEY")


# In[31]:


headers_for_model = {"Content-Type": "application/json",
                    "Authorization":f"Bearer {openai_api_key}"}



# In[32]:


image_identifier = OpenAI()
food_label = {
    "model":"gpt-4-vision-preview",
    "messages":[
        {
        "role":"user",
              "content": [
                  {"type": "text", "text": "GIve me a food name of the following image, that's it without any punctuation at the end."},
                  {"type": "image_url", "image_url": {"url":f"data:image/jpeg;base64,{base64_encoded_img}"}}
              ]
        }
    ]
}


# In[33]:


final_answer = requests.post("https://api.openai.com/v1/chat/completions", headers=headers_for_model, json=food_label)
print(final_answer.json())


# In[34]:


print(final_answer.json()['choices'][0]['message']['content'])


# In[ ]:




