import streamlit as st

# This file is kept for compatibility.
# The app now runs from Home.py
# Run with: streamlit run Home.py

st.set_page_config(page_title="Kids Learning Hub", page_icon="🌈")
st.info("👉 Please run the app using: `streamlit run Home.py`")
st.page_link("Home.py", label="Go to Home Page 🏠", icon="🌈")
