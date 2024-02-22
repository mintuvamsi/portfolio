from dotenv import load_dotenv
import os
import sys
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import streamlit as st
load_dotenv()
import matplotlib
matplotlib.use('TkAgg')

API_KEY = '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'
llm = OpenAI(api_token=API_KEY)
pandass_ai = PandasAI(llm)

st.title('Analysis and Visualization Tool')

uploaded_file = st.file_uploader("Upload Your files", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head(3))
    prompt = st.text_area("Enter your prompt:")

    # Generate output
    if st.button("Generate"):
        if prompt:
            # call pandas_ai.run(), passing dataframe and prompt
            with st.spinner("Generating response..."):
                st.write(pandas_ai.run(df, prompt))
        else:
            st.warning("Please enter a prompt.")

        


