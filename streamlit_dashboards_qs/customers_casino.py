# customers_casino.py

import pandas as pd
from db_connection import get_db_connection
from datetime import datetime
import streamlit as st

def calculate_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def fetch_all_customers_data(page_no, page_size, filters=None):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        

        # Construct the WHERE clause for filtering
        where_clause = ""
        if filters:
            where_conditions = []
            for key, value in filters.items():
                if value:
                    if key == "membership_type":
                        # Handle multiple selected membership types
                        membership_types = "', '".join(value)
                        where_conditions.append(f"membership_type IN ('{membership_types.lower()}')")
                    elif key == "min_amount":
                        where_conditions.append(f"amount >= {value}")
                    elif key == "max_amount":
                        where_conditions.append(f"amount <= {value}")
                    elif key == "min_age":
                        min_birth_date = datetime.today().replace(year=datetime.today().year - value)
                        where_conditions.append(f"birth_date <= '{min_birth_date.strftime('%Y-%m-%d')}'")
                    elif key == "max_age":
                        max_birth_date = datetime.today().replace(year=datetime.today().year - value - 1)
                        where_conditions.append(f"birth_date > '{max_birth_date.strftime('%Y-%m-%d')}'")
                    elif key == "gender":
                        if value in ["Male", "Female", "Other"]:
                            where_conditions.append(f"{key} = '{value}'")
                    else:
                        if isinstance(value, str):
                            where_conditions.append(f"{key} LIKE '%{value}%'")
                        else:
                            where_conditions.append(f"{key} = '{value}'")
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        # SQL query to fetch customer data with pagination and filters
        offset = (page_no - 1) * page_size
        query = f"SELECT name, birth_date, amount, membership_type, timestamp, gender FROM customers {where_clause} ORDER BY customer_id ASC LIMIT {page_size} OFFSET {offset}"
        cursor.execute(query)
        
        data = cursor.fetchall()
        description = cursor.description
        cursor.close()
        connection.close()
        return data, description
    else:
        return None, None

def load_customers_data_as_dataframe(page_no, page_size, filters=None):
    data, description = fetch_all_customers_data(page_no, page_size, filters)
    if data:
        df = pd.DataFrame(data)
        if description:
            df.columns = [desc[0] for desc in description]
        return df
    else:
        return None

def customers_data():
    st.title(":sunglasses: :blue[Customer Data]")

    # Initialize page number if not already set
    if "page_number" not in st.session_state:
        st.session_state.page_number = 1
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Customer Data"

    # Define page size
    page_size = 100

    # Initialize filters
    filters = {}

    # Create a sidebar expander for filters
    with st.sidebar.expander("Filters"):
        # Get filter by membership type
        membership_type = st.multiselect(
            "Membership Type", ["", "Silver", "Gold", "Platinum", "Black", "Tribune"])
        if membership_type:
            filters["membership_type"] = membership_type

        # Get filter for minimum amount spent
        min_amount = st.number_input("Minimum Amount Spent", min_value=0)
        if min_amount:
            filters["min_amount"] = min_amount

        # Get filter for maximum amount spent
        max_amount = st.number_input("Maximum Amount Spent", min_value=0)
        if max_amount:
            filters["max_amount"] = max_amount

        # Get filter for minimum age
        min_age = st.slider("Minimum Age", min_value=18, max_value=50)
        if min_age:
            filters["min_age"] = min_age

        # Get filter for maximum age
        max_age = st.slider("Maximum Age", min_value=50, max_value=100)
        if max_age:
            filters["max_age"] = max_age

        # Get filter for gender
        gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
        if gender:
            filters["gender"] = gender

    # Call load_customers_data_as_dataframe() function from customers_data.py with filters
    df = load_customers_data_as_dataframe(
        st.session_state.page_number, page_size, filters)

    # Display customer data with pagination
    if df is not None:
        st.subheader("Customer Data")

        # Apply custom CSS to increase width and height
        st.write(
            f"""<style>
                .dataframe > div:first-child {{
                    width: 1000px !important;
                    max-height: 600px !important;
                    overflow-x: auto !important;
                    overflow-y: auto !important;
                }}
            </style>""",
            unsafe_allow_html=True
        )

        # Display the DataFrame
        st.dataframe(df)

        # Display pagination controls
        if st.session_state.page_number > 1:
            if st.button("Previous Page"):
                st.session_state.page_number -= 1
        if len(df) == page_size:
            if st.button("Next Page"):
                st.session_state.page_number += 1
    else:
        st.error(
            "Failed to load customer data. Please check your database connection.")



