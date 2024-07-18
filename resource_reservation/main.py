import streamlit as st
import pandas as pd
from pages.user import *
from pages import resource,reservation
from database import get_db_connection, get_reservation_count_per_resource,get_user_reservation_count

db,cursor= get_db_connection()

# Function to get user role based on user ID
def get_user_role(user_id):
    cursor.execute("SELECT GetUserRole(%s)", (user_id,))
    user_role = cursor.fetchone()[0]
    return user_role

# Create a Streamlit app
st.title("Resource Reservation System")

resource.show_resources()
reservation.show_reservations()

st.title("List of Users")

# Get all users from user.py
users = print_user()

# Display the list of users in the Streamlit app
if not users:
    st.write("No users found.")
else:
    # Convert the list of tuples to a DataFrame
    users_df = pd.DataFrame(users, columns=["UserID", "Name", "Phone Number", "Role"])

    # Display the DataFrame as a table
    st.table(users_df)
   
# Display reservation count per resource
reservation_count_results = get_reservation_count_per_resource(db, cursor)

st.header("Reservation Count per Resource")

# Convert the results to a DataFrame
reservation_count_df = pd.DataFrame(reservation_count_results, columns=["Resource ID", "Resource Name", "Reservation Count"])

# Display the DataFrame as a table
st.table(reservation_count_df)

# Streamlit app for Get User Role
st.title("Get User Role")

# Get user input for user ID
user_id = st.number_input("Enter User ID for Role:", min_value=1, key="user_role_input")

if st.button("Get User Role"):
    # Call the function to get user role
    user_role = get_user_role(user_id)

    # Display user role
    st.write(f"User ID: {user_id}")
    st.write(f"User Role: {user_role}")
    
# Streamlit app for Get User Reservation Count
st.title("Get User Reservation Count")

# Get user input for user ID
user_id_reservation_count = st.number_input("Enter User ID for Reservation Count:", min_value=1, key="reservation_count_input")

if st.button("User Reservation Count"):
    # Call the function to get user reservation count
    reservation_count = get_user_reservation_count(db, cursor, user_id_reservation_count)

    # Display user reservation count
    st.write(f"User ID: {user_id_reservation_count}")
    st.write(f"Reservation Count: {reservation_count}")