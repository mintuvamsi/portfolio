import streamlit as st
import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from dotenv import load_dotenv
load_dotenv()


# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
OPENAI_API_KEY = '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'
st.set_page_config(layout='wide')
st.title('Welcome to Data Analysis and Visualization App')

input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

if input_csv is not None:

    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("Data Uploaded Successfully")
        data = pd.read_csv(input_csv)
        st.dataframe(data, use_container_width=True)

    with col2:
        st.info("Chat Section")
        
        input_text = st.text_area("Enter your query")

        if input_text is not None:
            if st.button("Chat with PandasAI"):
                st.info("User: " + input_text)
                # Instantiate a LLM
                llm = OpenAI(api_token=OPENAI_API_KEY)
                df = SmartDataframe(data, config={"llm": llm})

                # Chat with PandasAI
                response = df.chat(input_text)

                # # Display response
                st.write(response)

                # # Additional features: Plotting or other actions based on the query
                # if "plot" in input_text.lower():
                #     column_name = st.text_input("Enter column name for frequency plot:")
                #     if st.button("Plot Frequency Plot"):
                #         try:
                #             st.pyplot(df.plot.frequencyplot(column_name, bins=10))
                #         except Exception as e:
                #             st.error(f"Error plotting: {e}")
