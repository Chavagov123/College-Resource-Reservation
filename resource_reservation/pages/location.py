import streamlit as st
from database import conn
from sqlalchemy import text

st.header("Location Information Form")

# Create form inputs for Location table
name = st.text_input("Location Name")
address = st.text_input("Address (Room and Building Floor)")

# Create a button to submit the data
if st.button("Submit Location"):
    if name and address:
        try:
            with conn.session as s:
                s.execute(
                    text("INSERT INTO Location (name, address) VALUES (:name, :address);"),
                    params={"name": name, "address": address},
                )
                s.commit()
            st.success("Location data has been inserted!")
        except Exception as e:
            st.error(f"Error inserting location data: {e}")
    else:
        st.error("Please fill in all required fields.")
