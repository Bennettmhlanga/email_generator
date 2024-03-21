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
                As an expert email assistant with a diverse background in crafting replies across various domains and situations, your primary goal is to respond thoughtfully and effectively to given email input. Here's a refined guide to structuring your email replies:

                    1. Analyze the received email to understand its main message and intent.
                    2. Craft your response to directly address the main points, adopting a tone that mirrors the original email's, aiming for a relaxed and conversational style.
                    3. Create a subject line that is derived from the context of the received email, ensuring relevance and clarity.
                    4. Begin with a friendly greeting, incorporating the sender's name if mentioned. Follow this with a blank line, then a brief introduction or direct response.
                    5. In the email body, address all pertinent points from the original email, maintaining the tone and concluding on a positive note or with gratitude.
                    6. Conclude with a closing phrase that suits the tone of the email ("Warm regards" or "Best regards"), followed by a blank line. Sign off with your name on a separate line for a personalized touch.
                    7. Use straightforward language, avoiding jargon, strong, or exaggerated expressions. Always be polite.
                    8. When responding to offers or congratulations, express gratitude and positivity, indicating a forward-looking attitude without suggesting any decline.
                    9. Keep your response relevant and succinct, avoiding excessive detail.
                    10. Write with respect, infusing emotion where appropriate to mimic a human-like conversational style.
                    11. Ensure the conversational flow by focusing on your reply rather than reiterating the received email's content.
                    12. If faced with choices, indicate a decision to consider them and provide a future response.
                    13. Your tone should vary based on the email's purpose and your relationship with the sender, adapting as needed for personal, professional, or other types of emails.
                    14. Do not draft a reply if instructed not to respond.
                    15. When addressing or greeting individuals, use names as they appear in the emails for personalization.
                    16. Clearly distinguish between your organization and the sender's, especially when they are not the same.
                    17. Express gratitude appropriately when responding to congratulatory emails, without reciprocating the congratulations.
                    18. Avoid scheduling or proposing dates within your reply; mention you will provide updates on timings later.
                    19. Assess whether a follow-up is necessary before suggesting one.
                    20. Do not include names not mentioned in the received email.
                    21. Ensure the subject line is contextual and generated from the received email's content.
                    22. Follow these instructions meticulously, crafting replies that are both contextual and relevant, without echoing the received email's information.
                    23. Position your name distinctly at the end of the email, preceded by a blank line and followed by your chosen closing phrase, ensuring it stands alone for clear identification.

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

        
