import streamlit as st
import mysql.connector

from database import get_db_connection

# Function to fetch all resources
def fetch_resources(cursor):
    cursor.execute("SELECT * FROM Resource")
    resources = cursor.fetchall()
    return resources

# Function to display all resources
def show_resources():
    # Retrieve the database connection and cursor
    db, cursor = get_db_connection()

    st.title("All Resources")
    resources = fetch_resources(cursor)

    # Create a selectbox to choose a resource
    selected_resource = st.selectbox("Select a Resource", resources)

    if selected_resource:
        st.write(f"Selected Resource: {selected_resource[1]} (Resource ID: {selected_resource[0]})")
        # Store the selected resource in a session state
        st.session_state.selected_resource = selected_resource

        
db,cursor= get_db_connection()

st.title("Resource Information Form")

# Fetch all location names from the database
cursor.execute("SELECT name FROM Location")
locations = [location[0] for location in cursor.fetchall()]

# Create form inputs for Resource table
type = st.selectbox("Type", ["Lab", "Equipment", "Classroom"])
name = st.text_input("Name")
capacity = st.number_input("Capacity", min_value=1)
location = st.selectbox("Location", locations)

# Create a button to submit the data
if st.button("Submit Resource"):
    # Check if the name and capacity fields are not empty
    if name and capacity:
        # Get the location_id based on the selected location name
        cursor.execute("SELECT location_id FROM Location WHERE name = %s", (location,))
        location_id = cursor.fetchone()[0]

        # Insert data into the Resource table
        insert_query = "INSERT INTO Resource (type, name, location_id, capacity) VALUES (%s, %s, %s, %s)"
        data = (type, name, location_id, capacity)
        cursor.execute(insert_query, data)
        db.commit()
        st.success("Resource data has been inserted!")
    else:
        st.error("Please fill in all required fields.")