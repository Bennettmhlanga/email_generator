import msal
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import streamlit as st

def draftingemails(email):
    # Call GPT-3
    url = "https://api.openai.com/v1/chat/completions"
    openai_api_key = "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"
    model_name = "gpt-3.5-turbo"  

    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    query =f"""You are an expert email assistant with diverse background in crafting emails for different domains and situations. \n
    Craft a reply to a given email :{email}:, mirroring its tone. Here are the steps:
    1. Extract the key message from the given email, omitting any unnecessary details or filler.
    2. Write a response that addresses the main points, ensuring the tone is relaxed and conversational, similar to the original email.
    3. Include a subject line that fits the context.
    4. Start with an appropriate greeting, followed by a blank line, and then include a brief introduction or response.
    5. Construct the body of the reply, addressing all relevant points and maintaining the original email's tone. Conclude the body of the email with a positive note or a thank you.
    6. End with a closing that matches the email's tone, followed by a blank line. Then, ensure your name is placed on its own in the last sentence, effectively serving as a personalized sign-off.
    7. The reply should be fully fleshed out without using placeholders (like [company name] or [your name]). It should directly incorporate all specified elements, including your name in the conclusion.
    8. Ensure the language is straightforward, with minimal jargon.
    9. Be polite and always avoid the use of strong words, or exagerative words.
    

    Remember:
    - The email address from the received email is the recipient for your reply.
    - Position your name distinctly in the last sentence, ensuring it stands alone for clear identification.
    -make sure your name is in the last line and there is a blank space on top of it no other text must be in the same line with your name
    -make sure for the salutation use warm regards and best regard only
"""



    ###
   
    ###
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "Hello, how can I assist you?"
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }
    
    response = requests.post(url, json=data, headers=headers)
    information = json.loads(response.text)
    info = information['choices'][0]['message']['content']
    return info

st.set_page_config(layout="wide")


st.markdown("<h1 style='text-align: center;'>EMAIL AUTOMATION</h1>", unsafe_allow_html=True)
c1,c2 = st.columns(2)
with c1:

    sample_email= st.text_area("UPLOAD YOUR EMAIL HERE",height = 350)
    x= st.button("generate Reply")
with c2:
    
    if x:
        reply = st.info(draftingemails(sample_email))
