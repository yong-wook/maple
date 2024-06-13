import requests
import streamlit as st
url = "https://www.naver.com"
res = requests.get(url, verify=False)

st.markdown(res.text, unsafe_allow_html=True)
