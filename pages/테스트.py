import requests
import streamlit as st
url = "https://www.naver.com"
res = requests.get(url, verify=False)

st.markdown("<iframe>"+res.content+"</iframe>", unsafe_allow_html=True)
