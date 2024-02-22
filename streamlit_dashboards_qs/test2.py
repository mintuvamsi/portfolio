# test
import streamlit as st
from openai import OpenAI
import base64
import pandas as pd
import ydata_profiling as yp
from streamlit_pandas_profiling import st_profile_report

# Initialize OpenAI client
global client
client = OpenAI(api_key='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')
st.set_page_config('wide')

# Function to get base64 encoded string
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-size: cover;
    }}
    img {{
    opacity: 0.5
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit app
def main():
    st.title("EDA")

    # File upload
    df = st.file_uploader(label='Upload a CSV file', type=['csv'])

    if df is not None:
        df = pd.read_csv(df)
        st.dataframe(df, use_container_width=True)

        if st.button('EDA Analysis'):
            profile_report = yp.ProfileReport(df)
            st_profile_report(profile_report)

    # Background image
    set_background('data_files/background.jpg')
    with st.sidebar:
        st.markdown("@vamsidhar")
        messages = st.container(height=300)
        if prompt := st.chat_input("Say something"):
            messages.chat_message("user").write(prompt)
            if df is not None and ("dataframe" in prompt.lower() or "describe" in prompt.lower()):
                messages.chat_message("Assistant").write("Sure! Here are some insights about the DataFrame:")
                messages.write(get_dataframe_insights(df))
            else:
                chatbot_response = get_chat_response(prompt)
                messages.chat_message("Assistant").write(chatbot_response)

# Function to generate custom responses about the DataFrame
def get_dataframe_insights(df):
    insights = ""
    insights += f"Number of rows: {df.shape[0]}\n"
    insights += f"Number of columns: {df.shape[1]}\n"
    insights += f"Column names: {', '.join(df.columns)}\n"
    insights += f"Data types:\n{df.dtypes}\n"
    insights += f"Summary statistics:\n{df.describe()}\n"
    return insights

# Function to interact with chatbot API
def get_chat_response(input_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": input_text}]
    )
    message = response.choices[0].message.content
    return message

if __name__ == "__main__":
    main()