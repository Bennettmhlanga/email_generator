import streamlit as st
import requests
import json
import pandas as pd
from fuzzywuzzy import process

# Function to load the CSV file into a DataFrame
def load_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

# Load the CSV file
csv_file_path = "output.csv" # Update this path to your CSV file
df = load_csv_file(csv_file_path)

# Function to perform FuzzyWuzzy search and return the query and its corresponding "SENT" message
def semantic_search(query, limit=1):
    # Use FuzzyWuzzy to look up the "RECEIVED" message
    best_match = process.extractOne(query, df['RECEIVED'])
    if isinstance(best_match, tuple) and len(best_match) >= 2:
        matched_text, score, *_ = best_match # Unpack the first two elements and ignore the rest
        # Find the row in the DataFrame that contains the matched text
        matched_row = df[df['RECEIVED'] == matched_text]
        # Return the query and the corresponding "SENT" message
        return query, matched_row['SENT'].values[0]
    else:
        return query, None

# Function to draft emails
def draftingemails(email, openai_api_key, search_results):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "gpt-3.5-turbo"

    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    # Include the search results in the system message
    system_message = f"""
                    You are a skilled email assistant, here to ensure email replies are accurate and well-crafted. When given an email, your job is to check if {message_pair} is an appropriate response. 
                    
                    If {message_pair} is suitable:
                    - Use {message_pair} as a reply to the email input ALWAYS.
                    - Use it to make your own reply around it, take its context and important points to create your reply.
                    - REMEMBER: AS LONG AS {message_pair} IS SUTABLE USE IT!!!.
                    - Do not add additional content that is not related/not stated in: {message_pair}, {message_pair} is our key.
                    - If the: {message_pair} message is starting by hi, hello [Name], note that is your name you need it to put it after your salutations, and the name after salutations is the name of the message sender, you can use it for greeting the sender of the message.
                    - Position your name clearly and separately at the end of the email.
                    - Sign off with 'Warm regards' or 'Best regards', leaving a blank line before your name, which should be on a separate line.
                    - Ensure the reply is concise, addressing all points with a positive closure.
                    
                    If not:
                    - Compose a reply that matches the original email's tone. Follow these guidelines:
                        1. Understand the main message of the email. Avoid unnecessary details.
                        2. Respond in a relaxed, conversational tone. Include a fitting subject line.
                        3. Begin with a suitable greeting, then move directly into your reply.
                        4. Ensure the reply is concise, addressing all points with a positive closure.
                        5. Sign off with 'Warm regards' or 'Best regards', leaving a blank line before your name, which should be on a separate line.
                        6. Your response should be straightforward, polite, and avoid exaggeration.
                        7. If responding to a congratulatory message, express gratitude and positive sentiment.
                        8. Keep replies relevant and to the point, avoiding excessive detail.
                        9. Write with respect, emotional understanding, and from a first-person perspective.
                        10. Do not repeat information from the original email; focus on providing a direct reply.
                        11. Avoid scheduling actions; simply indicate a future discussion.
                        12. Tailor your tone to the email's context, considering the relationship and purpose.
                        13. Do not draft replies to emails instructing no response.
                        14. Use the recipient's name appropriately based on the email context.
                        15. Differentiate between your organization and the sender's, especially in professional contexts.
                        16. For congratulatory emails, thank the sender without reciprocating congratulations.
                        17. Carefully consider whether to end the conversation or suggest further contact.
                    
                    Remember:
                    - The sender's text address is where you'll send your reply.
                    - Position your name clearly and separately at the end of the email.
                    - Use 'Warm regards' or 'Best regards' for salutations.
                    - Ensure the reply is meaningful and adheres to these instructions.
                        """
    data = {
        "model": model_name,
        "temperature":0.3,
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": sample_email
            }
        ]
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        return f"Error: Received status code {response.status_code} from OpenAI API."

    try:
        information = response.json()
        if 'choices' in information and information['choices']:
            info = information['choices'][0]['message']['content']
            return info
        else:
            return "Error: No choices found in the response."
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"

# Streamlit app
st.set_page_config(layout="wide",page_title="email automation")
st.markdown("<h1 style='text-align: center; color: white;'>EMAIL ASSISTANT</h1>", unsafe_allow_html=True)

# Create columns for input and outputs
cols = st.columns(3)

# Input box for the email in the first column
with cols[0]:
    sample_email = st.text_area("Enter your email here:", height=400)

# Perform semantic search with the email content as the query
query, message_pair = semantic_search(sample_email)

# Display the query and message pair in the second column
with cols[1]:
    st.markdown("<h3 style='text-align: center;'>Query and Message Pair:</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 400px; overflow: auto; border: 0px solid #e0e0e0; padding: 10px;background-color:#2C2C2C'>{}</div>".format(f"QUERY: {query}\nMESSAGE PAIR: {message_pair}"), unsafe_allow_html=True)

# Draft email with search results in the third column
with cols[2]:
    openai_api_key = st.secrets["openai_key"] # Replace with your actual OpenAI API key
    reply = draftingemails(sample_email, openai_api_key, [])
    st.markdown("<h3 style='text-align: center;'>GPT Output:</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 400px; overflow: auto; border: 0px solid #e0e0e0; padding: 10px;background-color:#2C2C2C'>{}</div>".format(reply), unsafe_allow_html=True)
