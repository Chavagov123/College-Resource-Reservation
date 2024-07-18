import streamlit as st
import mysql.connector

from database import get_db_connection

db,cursor= get_db_connection()

st.header("Location Information Form")

# Create form inputs for Location table
name = st.text_input("Location Name")
address = st.text_input("Address (Room and Building Floor)")

# Create a button to submit the data
if st.button("Submit Location"):
    # Check if the name and address fields are not empty
    if name and address:
        # Insert the data into the Location table
        cursor = db.cursor()
        insert_query = "INSERT INTO Location (name, address) VALUES (%s, %s)"
        data = (name, address)
        cursor.execute(insert_query, data)
        db.commit()
        st.success("Location data has been inserted!")
    else:
        st.error("Please fill in all required fields.")
