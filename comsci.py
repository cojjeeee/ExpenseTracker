import streamlit as st
import pandas as pd
from datetime import date

########################################## MAIN MENU ##########################################
########################################## MAIN MENU ##########################################
########################################## MAIN MENU ##########################################

st.image("xtrack_banner.jpg")
st.write("""
Dataframe can be edited.
""")

data = pd.read_csv("personalexpense.csv")
data["Date"] = pd.to_datetime(data["Date"], format="mixed")

data["Delete"] = False  # add the column, default unchecked

t_data = st.data_editor(data, num_rows="fixed", hide_index=True)

if st.button("Remove Selected"):
    data = t_data[t_data["Delete"] == False].drop(columns=["Delete"])
    data = data.reset_index(drop=True)
    data.to_csv("personalexpense.csv", index=False)
    st.success("Selected records removed!")
    st.rerun()

########################################## ADD RECORD ##########################################
########################################## ADD RECORD ##########################################
########################################## ADD RECORD ##########################################

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    d1 = st.text_input("Expense")

with c2:
    d2 = st.text_input("Category")

with c3:
    d3 = st.text_input("Source")

with c4:
    d4 = st.number_input("Price")

with c5:
    d5 = st.date_input("Date")

if st.button("Record Expense"):
    new_row = pd.DataFrame([{"Expense": d1, "Category": d2, "Source": d3, "Price": d4, "Date": pd.to_datetime(d5)}])
    data = pd.concat([data, new_row], ignore_index=True)
    data.to_csv("personalexpense.csv", index=False)
    st.success("Expense added!")
    st.dataframe(data)

########################################## AVE PER DAY ##########################################
########################################## AVE PER DAY ##########################################
########################################## AVE PER DAY ##########################################

st.write("""
___
""")

cb1, cb2 = st.columns(2)

with cb1:
    day_tots = data.groupby("Date")["Price"].sum()
    day_ave = day_tots.mean()
    st.write(f"""
    #### Average Expense per Day:
    <h2 style="background-color: #212F19"> ₱{day_ave:,.2f}</h2>
    """, unsafe_allow_html=True)

with cb2:
    monthly_total = data.groupby(data["Date"].dt.to_period("M"))["Price"].sum()
    month_ave = monthly_total.mean()
    st.write(f"""
    #### Average Expense per Month:
    <h2 style="background-color: #212F19"> ₱{month_ave:,.2f}</h2>
    """, unsafe_allow_html=True)

########################################## AVE PER COLUMN ##########################################
########################################## AVE PER COLUMN ##########################################
########################################## AVE PER COLUMN ##########################################

st.write("""
___
#### Average Expense for:
""")
ca1, ca2 = st.columns(2)

########################################## CATEGORY ##########################################


with ca1:
    cgry = st.selectbox("Select Category", data["Category"].unique())
    cgry_ave = (data[data["Category"] == cgry].groupby("Category")["Price"].sum()).mean()
    st.write(f"""
    <h2 style="background-color: #212F19"> ₱{cgry_ave:,.2f}</h2>
    """, unsafe_allow_html=True)

########################################## SOURCE ##########################################
with ca2:
    srcs = st.selectbox("Select Source", data["Source"].unique())
    srcs_ave = (data[data["Source"] == srcs].groupby("Source")["Price"].sum()).mean()
    st.write(f"""
    <h2 style="background-color: #212F19"> ₱{srcs_ave:,.2f}</h2>
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
    st.write(f"""
             <h2 style="background-color: #384157"> ₱{ave_exp:,.2f}</h2>
        """, unsafe_allow_html=True)

