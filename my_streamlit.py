import requests
import json
import streamlit as st

def draftingemails(email, openai_api_key):
    # Call GPT-3
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "gpt-3.5-turbo"

    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    query = f"{email}"
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": """You are an expert email assistant with diverse background in crafting emails for different domains and situations. \n
                 You will be provided with an email, Your task is to craft a reply to a given email matching its tone. Here's how to create a reply for a specific email:

                1. Identify and focus on the main message of, ignoring irrelevant details.
                2. Your reply should directly address these main points with a tone that is casual and friendly, mirroring the original email's tone.
                3. Include a relevant subject line for your reply.
                4. Start with a fitting greeting, leave a blank line, then briefly introduce your response.
                5. Write the body of your email, covering all important points while keeping the tone consistent with the original. Finish with a positive note or expression of thanks.
                6. Conclude with a closing phrase that fits the tone, a blank line, and your name as a personalized signature, standing alone on the last line.
                7. Avoid using placeholders, unnecessary jargon, or strong language. The reply should be polite, clear, and use positive language, especially if responding to a congratulatory message.
                8. Keep your response relevant but concise, without going into excessive detail.
                9. Write with respect and empathy, in first person, ensuring your reply is thoughtful.
                10. Focus on replying directly without reiterating what was said in the original email.
                11. If options are presented, indicate you will consider them and respond later.
                12. Adapt your reply's tone based on the email's type, such as personal, professional, transactional, etc.
                13. Do not draft a reply if instructed not to in the original email.
                14. All your replies should be emotionally infused, giving human like conversation.
                15. If you are asked a preference, choosing between options, just suggest that you will look into it and come back later.
                
                Your reply should acknowledge the recipient's email address as the intended recipient. Clearly place your name at the end, separated by a blank line, and use "Warm regards" or "Best regards" as your closing salutation. This instruction is designed to help you generate a meaningful and contextually appropriate email reply.
                Remember:
                - The email address from the received email is the recipient for your reply.
                - Position your name distinctly in the last sentence, ensuring it stands alone for clear identification.
                - Make sure your name is in the last line and there is a blank space on top of it no other text must be in the same line with your name.
                - Make sure for the salutation use warm regards and best regard only.
                - Given an email input kindly reply it using the given context and generate a meaningful subject.
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
    if generate_reply_button and openai_api_key:
        reply = draftingemails(sample_email, openai_api_key)
        st.info(reply)
    elif generate_reply_button and not openai_api_key:
        st.error("Please enter your OpenAI API Key to generate a reply.")
