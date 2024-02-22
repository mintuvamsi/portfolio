# import os
# import streamlit as st
# import pandas as pd
# import ydata_profiling as yp
# from streamlit_pandas_profiling import st_profile_report


# st.title("Data Analyst Bot")

# data_uploaded = False
# df = None

# st.header("Please upload your dataset")
# file = st.file_uploader("Upload CSV File", type=["csv"])
# if file:
#     df = pd.read_csv(file)
#     st.dataframe(df)
#     data_uploaded = True

# if data_uploaded:
#     st.header("Exploratory Data Analysis (EDA)")

#     # Perform EDA using ydataprocessing
#     profile_df = yp.ProfileReport(df)
#     st_profile_report(profile_df)

# file_formats = {
#     "csv": pd.read_csv,
#     "xls": pd.read_excel,
#     "xlsx": pd.read_excel,
#     "xlsm": pd.read_excel,
#     "xlsb": pd.read_excel,
# }

# def clear_submit():
#     """
#     Clear the Submit Button State
#     Returns:

#     """
#     st.session_state["submit"] = False

# @st.cache(ttl=7200)
# def load_data(uploaded_file):
#     try:
#         ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
#     except:
#         ext = uploaded_file.split(".")[-1]
#     try:
#         if ext in file_formats:
#             return file_formats[ext](uploaded_file)
#         else:
#             st.error(f"Unsupported file format: {ext}")
#             return None
#     except:
#         pass

# uploaded_file = file

# if uploaded_file:
#     df = load_data(uploaded_file)

# openai_api_key = st.sidebar.text_input("OpenAI API Key",
#                                        type="password",
#                                        placeholder="Paste your OpenAI API key here (sk-...)")

# with st.sidebar:
#     st.markdown("@vamsidhar")

# if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
#     st.session_state["messages"] = [
#         {"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input(placeholder="What is this data about?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     # Initialize OpenAI's language model
#     llm = OpenAI(api_token=openai_api_key)

#     with st.chat_message("assistant"):
#         response = llm.generate_response(prompt)  # Generate response using OpenAI
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.write(response)


import streamlit as st
from openai import OpenAI
import base64
import pandas as pd
import ydata_profiling as yp
from streamlit_pandas_profiling import st_profile_report

# Initialize OpenAI client
global additional_stop_words
additional_stop_words = [
    "analysis",
    "explore",
    "visualization",
    "insights",
    "chart",
    "plot",
    "graph",
    "statistics",
    "dataframe",
    "describe",
    "data",
    "rows",
    "columns",
    "column names",
    "data types",
    "summary",
    "missing values",
    "count",
    "unique",
    "values",
    "distribution",
    "frequency",
    "correlation",
    "scatter",
    "histogram",
    "boxplot",
    "heatmap",
    "pairplot",
    "outliers",
    "trend",
    "pattern",
    "cluster",
    "cluster analysis",
    "regression",
    "classification",
    "machine learning",
    "model",
    "accuracy",
    "precision",
    "recall",
    "f1-score",
    "confusion matrix",
    "feature importance",
    "hyperparameter",
    "overfitting",
    "underfitting",
    "cross-validation",
    "bias",
    "variance",
    "ensemble",
    "bagging",
    "boosting",
    "gradient boosting",
    "random forest",
    "xgboost",
    "lightgbm",
    "catboost",
    "hyperparameter tuning",
    "grid search",
    "random search",
    "hyperopt",
    "model evaluation",
    "model selection",
    "model comparison",
    "hyperparameter optimization",
    "data cleaning",
    "data preprocessing",
    "feature engineering",
    "imputation",
    "scaling",
    "normalization",
    "transformation",
    "encoding",
    "one-hot encoding",
    "label encoding",
    "target encoding",
    "feature selection",
    "dimensionality reduction",
    "PCA",
    "t-SNE",
    "UMAP",
    "autoencoder",
    "model deployment",
    "API",
    "web application",
    "deployment",
    "production",
    "pipeline",
    "ETL",
    "extract",
    "transform",
    "load",
    "big data",
    "cloud",
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",
    "serverless",
    "lambda",
    "sagemaker",
    "spark",
    "hadoop",
    "hive",
    "pig",
    "sql",
    "nosql",
    "database",
    "data warehouse",
    "business intelligence",
    "dashboard",
    "reporting",
    "visualization tool",
    "power bi",
    "tableau",
    "qlik",
    "google data studio",
    "matplotlib",
    "seaborn",
    "plotly",
    "bokeh",
    "ggplot",
    "altair",
    "dash",
    "shiny",
    "streamlit",
    "flask",
    "django",
    "fastapi",
    "backend",
    "frontend",
    "full stack",
    "development",
    "software engineering",
    "coding",
    "programming",
    "python",
    "r",
    "java",
    "javascript",
    "html",
    "css",
    "sql",
    "no code",
    "low code",
    "scripting",
    "automation",
    "integration",
    "data science",
    "machine learning",
    "artificial intelligence",
    "deep learning",
    "natural language processing",
    "computer vision",
    "reinforcement learning",
    "supervised learning",
    "unsupervised learning",
    "semi-supervised learning",
    "ensemble learning",
    "transfer learning",
    "generative adversarial network",
    "neural network",
    "convolutional neural network",
    "recurrent neural network",
    "transformer",
    "BERT",
    "GPT",
    "BERT",
    "Word2Vec",
    "GloVe",
    "Doc2Vec",
    "fastText",
    "topic modeling",
    "word embedding",
    "vectorization",
    "tokenization",
    "preprocessing",
    "text mining",
    "text analysis",
    "sentiment analysis",
    "text classification",
    "named entity recognition",
    "part of speech tagging",
    "topic modeling",
    "information retrieval",
    "search engine",
    "keyword extraction",
    "text summarization",
    "chatbot",
    "natural language understanding",
    "natural language generation",
    "knowledge graph",
    "recommendation system",
    "collaborative filtering",
    "content-based filtering",
    "hybrid filtering",
    "A/B testing",
    "experimentation",
    "hypothesis testing",
    "statistical testing",
    "p-value",
    "confidence interval",
    "ANOVA",
    "chi-square",
    "t-test",
    "linear regression",
    "logistic regression",
    "decision tree",
    "random forest",
    "gradient boosting",
    "XGBoost",
    "LightGBM",
    "CatBoost",
    "neural network",
    "deep learning",
    "CNN",
    "RNN",
    "LSTM",
    "GRU",
    "transformer",
    "BERT",
    "GPT",
    "autoencoder",
    "GAN",
    "VAE",
    "recommender system",
    "collaborative filtering",
    "content-based filtering",
    "matrix factorization",
    "SVD",
    "NMF",
    "deep learning",
    "neural network",
    "CNN",
    "RNN",
    "LSTM",
    "GRU",
    "transformer",
    "BERT",
    "GPT",
    "autoencoder",
    "GAN",
    "VAE",
    "recommender system",
    "collaborative filtering",
    "content-based filtering",
    "matrix factorization",
    "SVD",
    "NMF"
]


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
            # if df is not None and ("dataframe" in prompt.lower() or "describe" in prompt.lower() or "data" in prompt.lower()):
            if df is not None and any(word in prompt.lower() for word in additional_stop_words):
                messages.chat_message("Assistant").write(
                    "Sure! Here are some insights about the DataFrame:")
                messages.write(get_dataframe_insights(df))
            else:
                chatbot_response = get_chat_response(prompt)
                messages.chat_message("Assistant").write(chatbot_response)

# Function to generate custom responses about the DataFrame


def get_dataframe_insights(df):
    # print(df.nunique())
    insights = ""
    insights += f"Number of rows: {df.shape[0]}\n"
    insights += f"Number of columns: {df.shape[1]}\n"
    insights += f"Column names: {', '.join(df.columns)}\n"
    insights += f"Data types:\n{df.dtypes}\n"
    insights += f"Summary statistics:\n{df.describe()}\n"
    # Count missing values in each column
    insights += f"Missing values:\n{df.isnull().sum()}\n"
    # Count unique values in each column
    insights += f"Unique values:\n{df.nunique()}\n"
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
