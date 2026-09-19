import streamlit as st
import pandas as pd

st.write("""
# Headline
Hello po!!!!!!!
""")

data = pd.read_csv("personalexpense.csv")

st.dataframe(data)