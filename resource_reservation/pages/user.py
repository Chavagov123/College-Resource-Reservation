import streamlit as st
from database import get_db_connection

db,cursor= get_db_connection()

st.header("User Information")
user_name = st.text_input("User Name")
phno = st.text_input("Phone Number")
role_options = ["admin", "user"]  # Enum values for the role field
role = st.selectbox("Role", role_options)

if st.button("Submit User"):
    # Check if the role is valid
    if role not in role_options:
        st.error("Invalid role. Please select a valid role.")
        st.stop()

    cursor = db.cursor()
    cursor.execute("INSERT INTO User (name, phno, role) VALUES (%s, %s, %s)", (user_name, phno, role))
    db.commit()
    st.success("User data has been inserted!")
    
def print_user():
    # Use the db and cursor here as needed
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    return data