import pandas as pd
from db_connection import get_db_connection
from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
                    # elif key == "start_date":
                    #     where_conditions.append(f"timestamp >= '{value}'")
                    # elif key == "end_date":
                    #     where_conditions.append(f"timestamp <= '{value}'")
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
    if "filters" not in st.session_state:
        st.session_state.filters = {}

    # Create a sidebar expander for filters
    with st.sidebar.expander("Filters"):
        # Get filter by membership type
        membership_type = st.multiselect(
            "Membership Type", ["", "Silver", "Gold", "Platinum", "Black", "Tribune"], )
        if membership_type:
            st.session_state.filters["membership_type"] = membership_type
        else:
            st.session_state.filters.pop("membership_type", None)

        # Get filter for minimum amount spent
        min_amount = st.number_input("Minimum Amount Spent", min_value=0)
        if min_amount:
            st.session_state.filters["min_amount"] = min_amount
        else:
            st.session_state.filters.pop("min_amount", None)

        # Get filter for maximum amount spent
        max_amount = st.number_input("Maximum Amount Spent", min_value=0)
        if max_amount:
            st.session_state.filters["max_amount"] = max_amount
        else:
            st.session_state.filters.pop("max_amount", None)

        # Get filter for minimum age
        min_age = st.slider("Minimum Age", min_value=18, max_value=100)
        if min_age:
            st.session_state.filters["min_age"] = min_age
        else:
            st.session_state.filters.pop("min_age", None)

        # Get filter for maximum age
        max_age = st.slider("Maximum Age", min_value=18, max_value=100)
        if max_age:
            st.session_state.filters["max_age"] = max_age
        else:
            st.session_state.filters.pop("max_age", None)

        # Get filter for gender
        gender = st.radio("Gender", ["", "Male", "Female", "Other"])
        if gender:
            st.session_state.filters["gender"] = gender
        else:
            st.session_state.filters.pop("gender", None)

    # Call load_customers_data_as_dataframe() function from customers_data.py with filters
    df = load_customers_data_as_dataframe(
        st.session_state.page_number, page_size, st.session_state.filters)

    # Display customer data with pagination
    if df is not None:
        # Calculate the sum of the filtered amounts
        sum_amount = df['amount'].sum()

        # Calculate the count of each membership type
        membership_type_counts = df['membership_type'].value_counts()

        # Calculate the average amount spent
        average_amount = df['amount'].mean()
        
        # Display metrics for membership type counts
        st.subheader("Membership Type Counts")

        # Get the count of each membership type in the current dataframe
        membership_type_counts = df['membership_type'].value_counts()

        # Initialize columns for side-by-side display
        cols = st.columns(len(membership_type_counts))

        # Display metrics for each membership type count
        for idx, (membership_type, count) in enumerate(membership_type_counts.items()):
            with cols[idx]:
                st.metric(membership_type, value=count)

        # Display metrics for minimum and maximum amounts and sum of the current table amount
        cols = st.columns(3)
        with cols[0]: 
            st.metric("Minimum Amount", value=float(df.min(axis=0).amount))
        with cols[1]: 
            st.metric("Maximum Amount", value=float(df.max(axis=0).amount))
        with cols[2]:
            st.metric("Sum of Current table Amount", value=float(sum_amount))

        # Display the metric for the average amount spent
        st.metric("Average Amount Spent", value=average_amount)
        
        # Apply custom CSS to rotate the delta arrow for metrics
        st.markdown(
            '''
            <style>
            [data-testid="stMetricDelta"] svg {
                transform: rotate(180deg);
            }
            </style>
            ''',
            unsafe_allow_html=True
        )

        # Display customer data
        st.subheader("Customer Data")
        # Apply custom CSS to increase width and height of DataFrame
        st.write(
            f"""<style>
                .dataframe > div:first-child {{
                    width: 1000px !important;
                    max-height: 1000px !important;
                    overflow-x: auto !important;
                    overflow-y: auto !important;
                }}
            </style>""",
            unsafe_allow_html=True
        )
        st.dataframe(df)

        try:
            # Gender Distribution bar chart
            st.subheader("Gender Distribution")

            # Calculate counts of each gender
            gender_counts = df['gender'].value_counts()

            # Create bar chart
            plt.bar(gender_counts.index, gender_counts.values, color=['blue', 'pink', 'green'])

            # Customize the chart
            plt.xlabel('Gender')
            plt.ylabel('Count')
            plt.title('Gender Distribution')

            # Show the chart
            st.pyplot(plt)

            # Calculate age of each customer
            df['age'] = df['birth_date'].apply(calculate_age)

            # Create histogram
            plt.hist(df['age'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)

            # Customize the chart
            plt.xlabel('Age')
            plt.ylabel('Count')
            plt.title('Age Distribution')

            # Show the chart
            st.pyplot(plt)
        except Exception as e:
            print(e)


        # Display pagination controls
        if st.session_state.page_number > 1:
            if st.button("Previous Page"):
                st.session_state.page_number -= 1
        if len(df) == page_size:
            if st.button("Next Page"):
                st.session_state.page_number += 1
    else:
        st.error("Failed to load customer data. Please check your database connection.")
    
