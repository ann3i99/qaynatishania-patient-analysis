import streamlit as st

st.set_page_config(page_title="test", 
                   page_icon=":shark:", 
                   layout="wide")

st.markdown("# Hello World!")
st.sidebar.write("this is main page")