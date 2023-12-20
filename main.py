from openai import AzureOpenAI
#from lxml import html
#import wikipediaapi
import requests
import json
import os
import urllib

client = AzureOpenAI(
	api_key = os.getenv("AZURE_OPENAI_KEY"),
	azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
	api_version = "2023-12-01-preview"
)

# client_2 = AzureOpenAI(
#     api_key = os.getenv("AZURE_OPENAI_KEY_2"),
#     azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_2"),
#     api_version = "2023-12-01-preview"
# )

with open("historical_key.txt", "r") as f:
    key = f.read()

#wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')
wiki_wiki = wikipediaapi.Wikipedia('English')
page_py = wiki_wiki.page("Vincent_Willem_van_Gogh")
#print("Page - Summary: %s" % page_py.summary[0:8000])
#print(page_py.summary[0:8000])

#print("Page text: %s" % page_py.text[:60])

#prompts = ["Translate the following English text to Korean:", "Summarize the given paragraph"]
#combined_prompt = "\n".join(prompts)
#prompt = "Translate the following English text to Korean:"

#prompts = [page_py.text[:60], "Based on the previous prompt information, write and talke like Vincent_Willem_van_Gogh"]
#combined_prompt = "\n".join(prompts)

#wiki_wiki = wikipediaapi.Wikipedia(
    #user_agent='MyProjectName (merlin@example.com)',
        #language='en',
        #extract_format=wikipediaapi.ExtractFormat.WIKI
#)

#p_wiki = wiki_wiki.page("Vincent van Gogh")
#print(p_wiki.text)

# def hist_event(event): #year
#     text = 'the internet' #user input here
#     api_url = 'https://api.api-ninjas.com/v1/historicalevents?text={}'.format(text)
#     hist_response = requests.get(api_url, headers={'X-Api-Key': key})
#     output = hist_response.json()
#     getting_event = output[0]['event']
#     #print(event) # this is working
#     return f"{event} occured before {getting_event}"


# # Formatting a chat-gpt question to fit inside another API
# # could add month, year, day later
# functions= [
#     {
#         "type": "function",
#         "function": {
#             # This will be name of our function
#             # We need to write this function!
#             "name": "hist_event",
#             "description": "Retrieve the historical event",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "event": {
#                           # getting the historical event itself, that is inputed by the user
#                         "type": "string",
#                         "description": "The name of the historical event" #Here are the following events we can use:
#                     },
                    
#                 },
#                 "required": ["event"],
#             },
#         },
#     }
# ]

def enter_prompt(f_artist, s_artist, question):
    #art = str(input("type your first artist:"))
    #art2 = str(input("type your second artist:"))
    first_art = f_artist
    second_art = s_artist

    text = question #user input here
    api_url = 'https://api.api-ninjas.com/v1/historicalevents?text={}'.format(text)
    hist_response = requests.get(api_url, headers={'X-Api-Key': key})
    output = hist_response.json()
    getting_event = output[0]['event']
    print(getting_event)

    my_messages = [
        #{"role": "system", "content": "Get trained by the information: {page_py.summary[0:8000]}"},
        {"role": "system", "content": "If I type something failed safety systme, can you reword it."},
        {"role": "user", "content": "Here is the {getting_event}, can you make a photo" + f"Can you make a Dalle prompt with the styles of the artists: {first_art} and {second_art}"},
        #{"role": "system", "content": "Combine the styles of the artists: {first_art} and {second_art}"}

        #{"role":"user", "content": str(getting_event)} #Send the data to the Chat-GPT
    ]


    #completion = client.completions.create(
        #model= "text-embedding-ada-002",
        #prompt= combined_prompt
    #)

    response = client.chat.completions.create(
        model= "gpt-4",
        #prompt= combined_prompt,
        messages = my_messages,
        #tools = functions,
        #tool_choice = "auto"
    )

    #print(response.choices[0].message.content)

    #embedding = client.embeddings.create(
        #input= prompt,
        #model= "text-embedding-ada-002"
    #)

    response02 = client.images.generate(
      model="dalle3",
      prompt= str(response.choices[0].message.content),
      size="1024x1024",
      quality="hd",
      n=1,
    )

    image_url = response02.data[0].url

    #return [response.choices[0].message.content, image_url]
    return image_url