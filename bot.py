import streamlit as st
from itertools import zip_longest
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from streamlit_chat import message

open_aikey= "OPENai_api key"

st.set_page_config(page_title="English Instructor")
st.title("AI English Intructor")

if 'generated' not in st.session_state:
    st.session_state['generated']= []

if 'past' not in st.session_state:
    st.session_state['past']= []

if 'prompt' not in st.session_state:
    st.session_state['prompt']= ""


chat= ChatOpenAI(
    model_name= 'gpt-3.5-turbo',
    temperature= 0.5,
    max_tokens= 100, 
    openai_api_key= open_aikey
)


def list_message():

    zipped_message= [SystemMessage(
        content= """
    Your name is AI English Instructor. You are a English language Expert, here to guide and assist students with their English and vocabulary related questions and concerns. Please provide accurate and helpful information, and always maintain a polite and professional tone.


                1. Greet the user politely ask user name and ask how you can assist them with English-related queries.
                2. Provide informative and relevant responses to questions about English language, vocabulary, part of speech, English Grammar, computer vision, and related topics.
                3. you must Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
                4. If the user asks about a topic unrelated to English Language, politely steer the conversation back to English or inform them that the topic is outside the scope of this conversation.
                5. Be patient and considerate when responding to user queries, and provide clear explanations.
                6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
                7. Do Not generate the long paragarphs in response. Maximum Words should be 100.

                Remember, your primary goal is to assist and educate students in the field of English Literacy. Always prioritize their learning experience and well-being.
"""
    )]

    for human_msg, ai_msg in zip_longest(st.session_state["past"], st.session_state['generated']):
        if human_msg is not None:
            zipped_message.append(HumanMessage(content=human_msg))
        if ai_msg is not None:
            zipped_message.append(AIMessage(content=ai_msg))

    return zipped_message


def generate_response():
    zipped_message= list_message()

    ai_response= chat(zipped_message)

    return ai_response.content


def submit():
    st.session_state.prompt= st.session_state.user_prompt
    st.session_state.user_prompt=""

st.text_input('Enter Your Query: ', key='user_prompt', on_change=submit)


if st.session_state.prompt != "":
    user_query= st.session_state.prompt

    st.session_state.past.append(user_query)
    output= generate_response()

    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1,-1):
        message(st.session_state['generated'][i], key= str(i))
        message(st.session_state['past'][i], is_user=True, key= str(i)+'_user')

