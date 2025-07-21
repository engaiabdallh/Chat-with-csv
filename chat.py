from langchain_experimental.agents import create_csv_agent
from langchain.llms import OpenAI
from langchain_core.messages import AIMessage,HumanMessage
from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image

def main():
    load_dotenv(override=True)

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")
    st.set_page_config(page_title="Chatbot")
    image = Image.open("assets/chat.jpeg")
    resized_image = image.resize((1300, 350))

    st.image(resized_image)
    # st.header("Ask your Facilities Data 📈",align='center')
    st.markdown("<h2 style='text-align: center;'>Ask About Facilities Data 📈</h2>", unsafe_allow_html=True)
    st.write('---')

    if 'chat_history' not in st.session_state:

        #initialize chat_history varaible 
        st.session_state.chat_history=[
            # AIMessage(content="Hello! I'm Gen Ai Model. Ask Me anything...")
        ]
    #upload file
    csv_file = st.file_uploader("Upload a CSV file", type="csv",accept_multiple_files=True)
    if csv_file is not None:

        # model 
        agent = create_csv_agent(
            OpenAI(temperature=0), csv_file, verbose=True,allow_dangerous_code=True,)
        
        # user_question = st.text_input("Ask a question: ")
        user_query=st.chat_input('Type a Message.....')  # input box

        if user_query is not None and user_query != "":
            with st.spinner(text="In progress..."):
                result=agent.run(user_query)                

                if user_query is not None and user_query.strip() !="":# ensures that the user query is not none or whitespace.
                    st.session_state.chat_history.append(HumanMessage(content=user_query))
                    st.session_state.chat_history.append(AIMessage(content=result))
                    

                for message in st.session_state.chat_history:
                    if isinstance(message,AIMessage):
                        with st.chat_message("AI"):#label of message
                            st.markdown(message.content)
                    elif isinstance(message,HumanMessage):
                        with st.chat_message("Human"):#label of message
                            st.markdown(message.content)


if __name__ == "__main__":
    main()
