import streamlit as st
import pandas as pd
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
import warnings 

warnings.filterwarnings("ignore") 

# Initialize OpenAI's language model
llm = OpenAI(api_token='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')

# App title
st.set_page_config(page_title="Experimental Dashboards")
st.title("Experimental Dashboards")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file")

# Check if file is uploaded
if uploaded_file is not None:
    # Read uploaded CSV file into a pandas DataFrame
    data = pd.read_csv(uploaded_file)
    # Create SmartDataframe object for AI interaction
    df = SmartDataframe(data, config={"llm": llm})

    # Function to generate AI response
    def generate_response(prompt):
        res = df.chat(prompt)
        return res

    # Initialize chat messages if not already present
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Handle user input
    if prompt := st.chat_input("Enter a question"):
        # Add user input to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Check if the last message was not from the assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Looking up information..."):
                    res = generate_response(prompt=prompt)
                    st.markdown(res)
            # Add AI response to chat history
            message = {"role": "assistant", "content": res}
            st.session_state.messages.append(message)
