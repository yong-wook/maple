import requests
import streamlit as st
#url = "https://www.naver.com"
#res = requests.get(url, verify=False)

st.markdown('''<iframe
            scr = "https://www.naver.com/?embed=true"
></iframe>''', unsafe_allow_html=True)
