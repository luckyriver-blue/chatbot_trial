from langchain_openai import ChatOpenAI
import streamlit as st

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.8, #1がランダム性高い
    max_tokens=3000, #200文字以内の生成にしたい
    #tomlファイルからapi_keyを取り出す
    openai_api_key = st.secrets["openai_key"],
)