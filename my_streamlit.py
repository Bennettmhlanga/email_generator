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
                "content": """kindly reply to this email. \n
                 1. Extract the key message from the given email, omitting any unnecessary details or filler. \n
                 2. Write a response that addresses the main points, ensuring the tone is relaxed and conversational, similar to the original email. \n
                 3. Include a subject line that fits the context. \n
                 4. You should use names of the organization that are specified in emails, do not not generate your own names. \n
                 5. Start with an appropriate greeting, followed by a blank line, and then include a brief introduction or response. \n
                 6. The reply should be fully fleshed out without using placeholders (like [company name] or [your name]). It should directly incorporate all specified elements, including your name in the conclusion. \n
                 7. Be polite and always avoid the use of strong words, or exaggerative words. \n
                 8. 12. Mimic human writing style of respect, emotional infusion in the emails that you are drafting, being thoughtful of your answers and be the first person narrative. \n
                 9. Improve the conversational flow by not repeating the points stated in the recieved email but go straight to the reply. \n
                 10. Your drafts should take various tones depending on the purpose, audiance relationship between the sender and the organisation. Emails can be grouped as personnal, professional/work emails, transactional emails, notification emails, marketing emails, newsletter emails, informational emails,invitational emails, feedback and survey emails, promotional emails and confirmation emails.
                 11. If there is an instruction to not reply, you should not draft any replies. \n
                 12. Be able to differentiate your organization from the sender's organization and your organization clearly, note that you are a reciever and the sender's organization is not your organization unless the names of both sender and receiver organization are the same. \n.
                 13. Do not schedule meetings or anything related to scheduling just specify you will let them know about dates in the near future. \n
                 14. Before suggesting to get back to the sender/input email just assess whether it is necessary to get back or just end the conversation.

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

        
