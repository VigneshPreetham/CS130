from dotenv import load_dotenv
import os
import base64
from io import BytesIO
from openai import OpenAI
import requests


load_dotenv()

class ChatGPT:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def image_identifier(self, image):
       
       # encoded_image = self.image_encoder(image)
        headers_for_model = {"Content-Type": "application/json",
                            "Authorization":f"Bearer {self.api_key}"}
        
        image_identifier = OpenAI()

        food_label = {
            "model":"gpt-4-vision-preview",
            "messages":[
                {
                "role":"user",
                    "content": [
                        {"type": "text", "text": "Give me a food name of the following image, that's it without any punctuation at the end."},
                        {"type": "image_url", "image_url": {"url":f"data:image/jpeg;base64,{image}"}}
                    ]
                }
            ]
        }

        final_answer = requests.post("https://api.openai.com/v1/chat/completions", headers=headers_for_model, json=food_label)
        # print(final_answer.text)
        #print(final_answer.json()['choices'][0]['message']['content'])
        return (final_answer.json()['choices'][0]['message']['content'])
        #print(final_answer.text)
    
    def generate_recipe(self, recipe_name):
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system", "content": "You are a writer that specializes in writing recipes and cookbooks."},
                {"role":"user", "content":"Give me a well formatted list of ingredient and the recipe for how to create the following dish: " + recipe_name}
            ]


        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content 







    # def image_encoder(self, file_storage):
    #     file_storage.seek(0) 
    #     file_content = file_storage.read()
    #     encoded_string = base64.b64encode(file_content).decode('utf-8')
    #     return encoded_string



