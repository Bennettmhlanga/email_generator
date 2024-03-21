import requests
import json
import streamlit as st

def draftingemails(email, openai_api_key):
    # Call GPT-3
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "ft:gpt-3.5-turbo-0125:personal:email1:94rrUSGA"

    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    query = f"{email}"
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": """
                Hello you are provided with an email, your job is to reply to the email, within context.
                 Follow these steps:
                 1. Always use context to reply the emails.
                 2. Do not generate your own names use the names that are provided in the email.
                 3. Do not generate what is not asked.
                """

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

# Ask the user for their OpenAI API Key
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

c1, c2 = st.columns(2)
with c1:
    sample_email = st.text_area("UPLOAD YOUR EMAIL HERE", height=350)
    generate_reply_button = st.button("Generate Reply")

with c2:
    try:
        if generate_reply_button and openai_api_key:
            reply = draftingemails(sample_email, openai_api_key)
            st.info(reply)
        elif generate_reply_button and not openai_api_key:
            st.error("Please enter your OpenAI API Key to generate a reply.")
    except Exception as e:
            st.warning(e)

        
