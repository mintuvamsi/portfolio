import streamlit as st
from customers_casino import customers_data


def home():
    st.title(":sunglasses: :blue[Customer Information]")
    st.write("Welcome to the Customer Information App!")
    # Show the essay
    st.markdown('''
                <div style="text-align: justify;">
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


def main():
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Home"
    elif "page_number" not in st.session_state:
        st.session_state.page_number = 1

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.selectbox(
        "Go to", ("Home", "Customer Data"), index=["Home", "Customer Data"].index(st.session_state.selected_page))
    st.session_state.selected_page = selected_page
    if selected_page == "Home":
        home()
    elif selected_page == "Customer Data":
        with st.container():
            customers_data()


if __name__ == "__main__":
    main()