import os 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly as px 
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from utils import get_data
from dotenv import load_dotenv

load_dotenv()

df_clients = get_data("clients_data")
df_traffic = get_data("traffic_data")

merge_keys = ['date', 'source_medium', 'campaign']
df = pd.merge(df_clients, df_traffic, on=merge_keys, how='inner')

print("Merged DataFrames")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-05-20",
    temperature=0,
    max_tokens=None,
    timeout=None,
)

agent = create_pandas_dataframe_agent(
    llm,
    df,
    allow_dangerous_code=True,
    verbose=True
)

# Maintain conversation history (as strings, to keep it simple)
print("\nStart chatting with your DataFrame agent. Type 'exit' or 'quit' to stop.\n")

while True:
    user_input = input("user: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    try:
        result = agent.invoke(user_input)
        print("assistant:", result)
    except Exception as e:
        print("⚠️ Note: There was an internal error, but the LLM likely succeeded (e.g., created a file or plot).")
