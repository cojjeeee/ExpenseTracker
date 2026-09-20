import streamlit as st
import pandas as pd
import numpy as np

########################################## MAIN MENU ##########################################
########################################## MAIN MENU ##########################################
########################################## MAIN MENU ##########################################

st.image("xtrack_banner.jpg")
st.write("""
Expenses made for the given duration will be shown in the table below. You can also calculate the average expense for a given duration.
""")

data = pd.read_csv("personalexpense.csv", index_col=0)
data["Date"] = pd.to_datetime(data["Date"])

st.dataframe(data)

########################################## AVE PER DAY ##########################################
########################################## AVE PER DAY ##########################################
########################################## AVE PER DAY ##########################################

st.write("""
___
""")
daily_total = data.groupby("Date")["Price"].sum()
day_ave = daily_total.mean()
st.write(f"""
#### Average Expense per Day:
<h2 style="background-color: #384157"> ₱{day_ave:,.2f}</h2>
""", unsafe_allow_html=True)

########################################## AVE PER COLUMN ##########################################
########################################## AVE PER COLUMN ##########################################
########################################## AVE PER COLUMN ##########################################

########################################## CATEGORY ##########################################
st.write("""
___
#### Average Expense for:
""")
cgry = st.selectbox("Select Category", data["Category"].unique())
cgry_ave = (data[data["Category"] == cgry].groupby("Category")["Price"].sum()).mean()
st.write(f"""
<h2 style="background-color: #384157"> ₱{cgry_ave:,.2f}</h2>
""", unsafe_allow_html=True)

st.write("""
#### Average Expense for:
""")
srcs = st.selectbox("Select Source", data["Source"].unique())
srcs_ave = (data[data["Source"] == srcs].groupby("Source")["Price"].sum()).mean()
st.write(f"""
<h2 style="background-color: #384157"> ₱{srcs_ave:,.2f}</h2>
""", unsafe_allow_html=True)

########################################## AVE BETWEEN DATES ##########################################
########################################## AVE BETWEEN DATES ##########################################
########################################## AVE BETWEEN DATES ##########################################

st.write("""
___
#### Average Expense between:
""")
s_date = st.date_input("Start Date")
e_date = st.date_input("End Date")

if st.button("Calculate Average Expense"):
    ave_exp = data[(data["Date"] >= pd.to_datetime(s_date)) & (data["Date"] <= pd.to_datetime(e_date))]["Price"].mean()
    st.write(f"Average Expense: {round(ave_exp, 2)}")

