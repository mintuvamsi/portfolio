# streamlit_server.py
import base64
import streamlit as st
from customers_casino import customers_data
from streamlit_pandas_profiling import st_profile_report
import ydata_profiling as yp
import pandas as pd
from openai import OpenAI
import streamlit.components.v1 as compo

# Initialize OpenAI client
global client
client = OpenAI(api_key='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')

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

# set_background('data_files/background.jpg')

def home():
    
    # Define the HTML code for the Lottie animations
    html_code = '''
    <div style="display: flex; align-items: center; justify-content: space-around;">
        <div style="margin-right: 20px;">
            <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
            <lottie-player src="https://lottie.host/cedc1377-595d-4379-9e75-40b40f0ab79d/wNcoPaIEt8.json" background="#fff" speed="1" style="width: 300px; height: 300px" loop controls autoplay direction="1" mode="normal"></lottie-player>
        </div>
        <div>
            <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
            <lottie-player src="https://lottie.host/21e28a91-010d-405c-b107-5ce52330ed5f/Fs8nmhURkV.json" background="#fff" speed="1" style="width: 300px; height: 300px" loop controls autoplay direction="1" mode="normal"></lottie-player>
        </div>
    </div>
    '''

    # Render the HTML code for the Lottie animations
    compo.html(html_code, width=800, height=400)

    # Display the title and introductory text
    st.title(":sunglasses: :blue[Customer Information]")
    st.write(" :blue[Welcome to the Customer Information App!]")

    # Render the HTML code
    # compo.html(html_code)

    # Display the essay
    st.markdown('''
                <div style="text-align: justify;  color: white;">
                <br>
                In today's dynamic business landscape, understanding customer behavior is paramount for success. 
                Web-based analytical applications provide a powerful platform for businesses to gain insights into customer preferences, behaviors, and trends. 
                By leveraging advanced analytics and interactive visualizations, these applications enable businesses to analyze vast amounts of customer data efficiently. 
                One key advantage of web-based analytical applications is their accessibility. Users can access these applications from any device with an internet connection, allowing for seamless collaboration and decision-making across teams. 
                <br>
                <br>
                Additionally, these applications often feature user-friendly interfaces and customizable dashboards, empowering users to tailor their analyses to specific business objectives. 
                Furthermore, web-based analytical applications offer real-time data processing capabilities, enabling businesses to monitor customer interactions and trends as they happen. 
                This real-time visibility allows for timely interventions and adjustments to marketing strategies, product offerings, and customer service initiatives. 
                <br>
                <br>
                Moreover, web-based analytical applications support data integration from multiple sources, including customer relationship management (CRM) systems, social media platforms, and e-commerce websites. 
                This holistic view of customer data enables businesses to create comprehensive customer profiles and segmentations, facilitating targeted marketing campaigns and personalized customer experiences. 
                Another benefit of web-based analytical applications is their scalability. As businesses grow and evolve, these applications can easily accommodate increasing data volumes and user requirements without significant infrastructure investments. 
                This scalability ensures that businesses can continue to derive value from their analytical initiatives as they expand. 
                In conclusion, web-based analytical applications play a vital role in enhancing customer understanding and driving business growth. 
                By providing accessible, real-time insights into customer behavior, preferences, and trends, these applications empower businesses to make data-driven decisions that ultimately lead to improved customer satisfaction, loyalty, and profitability.        
                This app allows you to search for a customer by their name or ID and view their information. 
                This app allows you to explore the customer information of a casino. 
                </div>
                ''', unsafe_allow_html=True)

def customers_data_page():
    st.title(":bar_chart: :blue[EDA Analysis]")
    st.write("Perform Exploratory Data Analysis (EDA) here.")

    # File upload
    uploaded_file = st.file_uploader(label='Upload a CSV file', type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

        if st.button('Perform EDA Analysis'):
            profile_report = yp.ProfileReport(df)
            st_profile_report(profile_report)

        # Chat functionality
        st.sidebar.title("Chat")
        chat_input = st.sidebar.text_input("Say something:")
        if chat_input:
            chatbot_response = get_chat_response(chat_input)
            st.sidebar.write("Assistant: " + chatbot_response)

def main():
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Home"

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.selectbox(
        "Go to", ("Home", "Customer Data", "EDA Analysis"), index=["Home", "Customer Data", "EDA Analysis"].index(st.session_state.selected_page))
    st.session_state.selected_page = selected_page

    if selected_page == "Home":
        home()
    elif selected_page == "Customer Data":
        customers_data()
    elif selected_page == "EDA Analysis":
        customers_data_page()

def get_chat_response(input_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": input_text}]
    )
    message = response.choices[0].message.content
    return message

if __name__ == "__main__":
    main()
