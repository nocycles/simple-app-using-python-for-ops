import streamlit as st
from pymongo import MongoClient

# Import functions from mongodb_query.py
from web_class_cs_helper import status_pengajuan, dana_instant, pengajuan_motor, member_check, cek_pending

def main():
    st.title("Your MongoDB Query App")
    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Select an option", ("Status Pengajuan", "Dana Instant", "Pengajuan Motor", "Member Check", "Cek Pending"))
    
    if menu == "Status Pengajuan":
        status_pengajuan_ui()
    elif menu == "Dana Instant":
        dana_instant_ui()
    elif menu == "Pengajuan Motor":
        pengajuan_motor_ui()
    elif menu == "Member Check":
        member_check_ui()
    elif menu == "Cek Pending":
        cek_pending_ui()

def status_pengajuan_ui():
    st.write("### Status Pengajuan")
    user_input = st.text_input("Input Mobile Phone / NIK:")
    if st.button("Submit"):
        status_pengajuan(user_input)
    pass

def dana_instant_ui():
    st.write("### Dana Instant")
    user_input = st.text_input("Input Mobile Phone:")
    if st.button("Submit"):
        dana_instant(user_input)

def pengajuan_motor_ui():
    st.write("### Pengajuan Motor")
    user_input = st.text_input("Input Mobile Phone:")
    if st.button("Submit"):
        pengajuan_motor(user_input)

def member_check_ui():
    st.write("### Member Check")
    st.write("Soon to be updated on the next version!")

def cek_pending_ui():
    st.write("### Cek Pending")
    start_date = st.text_input("Enter the start date (example: 2023-06-01):")
    end_date = st.text_input("Enter the end date (example: 2023-06-02):")
    if st.button("Submit"):
        cek_pending(start_date, end_date)

if __name__ == "__main__":
    main()
