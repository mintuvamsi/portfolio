# streamlit_dashboards_qs/qs_casino.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db_connection import get_db_connection

# Function to fetch data from the database with optional filtering
def fetch_data(page_number, page_size, bet_type=None):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        offset = (page_number - 1) * page_size

        # Construct SQL query with optional bet_type filter
        query = "SELECT * FROM quiz_answers WHERE 1=1"
        if bet_type:
            query += f" AND bet_type = '{bet_type}'"
        query += f" OFFSET {offset} LIMIT {page_size}"

        cursor.execute(query)
        data = cursor.fetchall()
        description = cursor.description
        cursor.close()
        connection.close()
        return data, description  # Return both data and cursor description
    else:
        return None, None

# Function to fetch data from the database
def fetch_count_by_bet_type():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        # SQL query to fetch required data
        cursor.execute("SELECT bet_type, COUNT(*) AS count FROM quiz_answers GROUP BY bet_type")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
    else:
        return None

# Main function to run the Streamlit app
def qs_casino_main():
    st.title("Data Visualization and Display from PostgreSQL Database")

    # Fetch data from the database
    data, _ = fetch_data(1, 100)  # Initial display without any filters

    # Display the data table if data is available
    if data:
        st.write("Data from the database:")

        # Convert data to DataFrame
        df = pd.DataFrame(data)

        # Set column names
        if _:
            df.columns = [desc[0] for desc in _]

        # Exclude 'id' and 'index' columns
        df.drop(columns=['id', 'index'], inplace=True, errors='ignore')

        # Display data in a table
        st.write(df)

        # Fetch count of each bet type for visualization
        count_data = fetch_count_by_bet_type()

        if count_data:
            count_df = pd.DataFrame(count_data, columns=['bet_type', 'count'])

            # Create bar plot using Matplotlib
            st.subheader("Bar Plot using Matplotlib")
            fig, ax = plt.subplots()
            ax.bar(count_df['bet_type'], count_df['count'])
            ax.set_xlabel("Bet Type")
            ax.set_ylabel("Count")
            ax.set_title("Count of Each Bet Type")
            st.pyplot(fig)

            # Create bar plot using Seaborn
            st.subheader("Bar Plot using Seaborn")
            fig, ax = plt.subplots()
            sns.barplot(data=count_df, x='bet_type', y='count', ax=ax)
            ax.set_xlabel("Bet Type")
            ax.set_ylabel("Count")
            ax.set_title("Count of Each Bet Type")
            st.pyplot(fig)
    else:
        st.error("Failed to fetch data from the database. Please check your database connection.")

if __name__ == "__main__":
    qs_casino_main()