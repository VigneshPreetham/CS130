#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import os


# In[2]:


from dotenv import load_dotenv, find_dotenv


# In[3]:


#the format: https://api.spoonacular.com/food/products/search?query=yogurt&apiKey=API-KEY


# In[4]:


file_path = "/Users/preethamvignesh/Desktop/Savor/"
load_dotenv(file_path + ".env")


# In[5]:


food_name = "pepperoni pizza"
api_key = os.getenv("SPOONACULAR_API_KEY")


# In[6]:


response = requests.get("https://api.spoonacular.com/recipes/search?query="+food_name+"&apiKey="+api_key)


# In[7]:


print("Here is the response: ",response.json())


# In[8]:


list_recipes = response.json()


# In[9]:


recipe_info = list_recipes['results'][0]


# In[10]:


recipe_url = recipe_info['sourceUrl']
print(recipe_url)


# In[11]:


entire_recipe = requests.get("https://api.spoonacular.com/recipes/extract?url="+recipe_url+"&apiKey="+api_key)


# In[12]:


print("Status: ", entire_recipe)


# In[13]:


all_info = entire_recipe.json()
print(all_info)


# In[25]:


recipe_instructions = all_info['instructions']
recipe_ingredients = all_info['extendedIngredients']
print(recipe_instructions)


# In[15]:


print(recipe_ingredients)


# In[29]:


ingredient_list = ""
for idx in range(len(recipe_ingredients)):
    ingredient = recipe_ingredients[idx]
    #print(ingredient['original'])
    actual_ingredient = ingredient['original']
    if idx != 0:
        ingredient_list = ingredient_list + ". " + actual_ingredient 
    else:
        ingredient_list = actual_ingredient
    

#print(recipe_ingredients[0]['original'])
print(ingredient_list)


# In[17]:


#cause there seem to be repeats in the ingredients, removing repeats:
#some preprocessing as well
ingredient_list = []
i = 0
while i < len(recipe_ingredients):
  ingredient_desc = recipe_ingredients[i]['original']
  complex_condition = ingredient_desc[0] == 'A' and ingredient_desc[1] == ' '
  if not ingredient_desc[0].isnumeric() and (not complex_condition):
    ingredient_desc = "A "+ ingredient_desc.lower()

  if (not ingredient_list) or (ingredient_desc.lower() != ingredient_list[-1]):
    if ingredient_desc[0].isnumeric():
      ingredient_list.append(ingredient_desc.lower())
    else:
      ingredient_list.append(ingredient_desc)


  i += 1



# In[18]:


#formatting the instructions in recipe_instructions
recipe_instructions = (recipe_instructions[3:-4])
print(recipe_instructions)


# In[19]:


bound = 0
recipe_inst_list = []
while i < len(recipe_instructions):
  if recipe_instructions[i] == '.':
    if recipe_instructions and i + 1 < len(recipe_instructions):
      if not (recipe_instructions[i-1].isnumeric() and recipe_instructions[i+1].isnumeric()):
        recipe_inst_list.append(recipe_instructions[bound: i+1])
        bound = i + 1
  i += 1
if bound < len(recipe_instructions):
  recipe_inst_list.append(recipe_instructions[bound:]+'.')




# In[20]:


print(recipe_inst_list)


# In[21]:


i = 0
print(type(recipe_inst_list[0]))
while i < len(recipe_inst_list):
  recipe_inst_list[i] = (recipe_inst_list[i].lstrip().capitalize())[:-1]
  i += 1


# In[22]:


print(recipe_inst_list)


# In[23]:


#the official ingredients is stored in the ingredient_list
#the official recipe (set of instructions is stored in recipe_inst_list)
print("Here are the ingredients: ")
for ingredient in ingredient_list:
  print(ingredient)
print("\n")
print("Here is the recipe: ")
for i in range(len(recipe_inst_list)):
  print(str(i+1)+". "+recipe_inst_list[i])


# In[24]:


#some fixes are to the recipe (word)
openai_api_key = os.getenv("OPENAI_API_KEY")


# In[30]:


from openai import OpenAI
client = OpenAI()
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system", "content": "You are a writer that specializes in writing recipes and cookbooks."},
        {"role":"user", "content": "format these ingredients: "+ ingredient_list + " and format these recipe instructions: "+ recipe_instructions +" into a well formatted recipe and add in or replace to make more sense."}
    ]


)


# In[34]:


print(completion.choices[0].message.content)


# In[ ]:




