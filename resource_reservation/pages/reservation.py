import streamlit as st
import pandas as pd
from database import get_db_connection

# Function to fetch all reservations for a selected resource
def fetch_reservations(resource_id):
    # Establish a database connection
    db, cursor = get_db_connection()
    cursor.execute("SELECT * FROM Reservation WHERE resource_id = %s", (resource_id,))
    reservations = cursor.fetchall()
    db.close()  # Close the database connection
    return reservations

def show_reservations():
    if "selected_resource" not in st.session_state:
        st.warning("Please select a resource from the 'All Resources' page.")
        return
    
    selected_resource = st.session_state.selected_resource

    st.title("All Reservations")
    st.write(f"Reservations for {selected_resource[1]} (Resource ID: {selected_resource[0]})")

    # Fetch reservations
    reservations = fetch_reservations(selected_resource[0])

    # Convert the list of tuples to a DataFrame
    reservations_df = pd.DataFrame(reservations, columns=["Reservation ID", "Start Time", "End Time", "Resource ID", "User ID", "Status ID", "Attendees"])

    # Display the DataFrame as a table
    st.table(reservations_df)
    
# Function to fetch all user IDs from the User table
def fetch_all_user_ids():
    db, cursor = get_db_connection()
    cursor.execute("SELECT userid FROM User")
    user_ids = [row[0] for row in cursor.fetchall()]
    db.close()
    return user_ids

# Function to fetch all resource IDs from the Resource table
def fetch_all_resource_ids():
    db, cursor = get_db_connection()
    cursor.execute("SELECT resource_id FROM Resource")
    resource_ids = [row[0] for row in cursor.fetchall()]
    db.close()
    return resource_ids

# Function to fetch all reservation IDs from the Reservation table
def fetch_all_reservation_ids():
    db, cursor = get_db_connection()
    cursor.execute("SELECT reservation_id FROM Reservation")
    reservation_ids = [row[0] for row in cursor.fetchall()]
    db.close()
    return reservation_ids

# Function to fetch all status IDs from the ReservationStatus table
def fetch_all_status_ids():
    db, cursor = get_db_connection()
    cursor.execute("SELECT status_id FROM ReservationStatus")
    status_ids = [row[0] for row in cursor.fetchall()]
    db.close()
    return status_ids

db, cursor = get_db_connection()
st.title("Reservation Information Form")

# Create form inputs for Reservation table
start_date = st.date_input("Start Date", key="start_date_input")
start_time = st.time_input("Start Time", key="start_time_input")
end_date = st.date_input("End Date", key="end_date_input")
end_time = st.time_input("End Time", key="end_time_input")

# Dropdowns for User ID, Resource ID, and Status ID
user_id = st.selectbox("User ID", fetch_all_user_ids(), key="user_id_input")
resource_id = st.selectbox("Resource ID", fetch_all_resource_ids(), key="resource_id_input")
status_id = st.selectbox("Status ID", fetch_all_status_ids(), key="status_id_input")

attendees = st.number_input("Number of Attendees", min_value=1, key="attendees_input")

# Combine date and time into datetime objects
start_datetime = pd.to_datetime(f"{start_date} {start_time}")
end_datetime = pd.to_datetime(f"{end_date} {end_time}")

# Create a button to submit the data
if st.button("Submit Reservation"):
    # Check if the required fields are not empty
    if start_datetime and end_datetime and user_id and resource_id and status_id and attendees:
        # Check if the resource_id exists
        cursor.execute("SELECT 1 FROM Resource WHERE resource_id = %s", (resource_id,))
        if not cursor.fetchone():
            st.error("Invalid Resource ID. Please enter a valid Resource ID.")
            st.stop()

        # Check if the userid exists
        cursor.execute("SELECT 1 FROM User WHERE userid = %s", (user_id,))
        if not cursor.fetchone():
            st.error("Invalid User ID. Please enter a valid User ID.")
            st.stop()

        # Check if the status_id exists
        cursor.execute("SELECT 1 FROM ReservationStatus WHERE status_id = %s", (status_id,))
        if not cursor.fetchone():
            st.error("Invalid Status ID. Please enter a valid Status ID.")
            st.stop()

        # Insert the data into the Reservation table
        insert_query = "INSERT INTO Reservation (start_time, end_time, resource_id, userid, status_id, attendees) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (start_datetime, end_datetime, resource_id, user_id, status_id, attendees)
        cursor.execute(insert_query, data)

        # Commit the transaction
        db.commit()
        st.success("Reservation data has been inserted!")
    else:
        st.error("Please fill in all required fields.")

# Streamlit form for updating reservation status
st.subheader("Update Reservation Status")
reservation_id = st.number_input("Reservation ID", min_value=1, key="update_reservation_id_input")
new_status_id = st.selectbox("New Status ID", fetch_all_status_ids(), key="new_status_id_input")

if st.button("Update Reservation Status"):
    try:
        # Call the stored procedure to update reservation status
        update_status_query = "CALL UpdateReservationStatus(%s, %s)"
        data = (reservation_id, new_status_id)
        cursor.execute(update_status_query, data)
        db.commit()
        st.success("Reservation status updated successfully.")
    except Exception as e:
        st.error(f"Error updating reservation status: {str(e)}")


# Streamlit form for updating reservation details
st.subheader("Update Reservation Details")
update_reservation_id = st.selectbox("Reservation ID to Update", fetch_all_reservation_ids(), key="update_reservation_details_id_input")

# Create form inputs for updated Reservation details
update_start_date = st.date_input("New Start Date", key="update_start_date_input")
update_start_time = st.time_input("New Start Time", key="update_start_time_input")
update_end_date = st.date_input("New End Date", key="update_end_date_input")
update_end_time = st.time_input("New End Time", key="update_end_time_input")

# Dropdowns for User ID, Resource ID, and Status ID
update_user_id = st.selectbox("New User ID", fetch_all_user_ids(), key="update_user_id_input")
update_resource_id = st.selectbox("New Resource ID", fetch_all_resource_ids(), key="update_resource_id_input")
update_status_id = st.selectbox("New Status ID", fetch_all_status_ids(), key="update_status_id_input")

update_attendees = st.number_input("New Number of Attendees", min_value=1, key="update_attendees_input")

# Combine date and time into datetime objects
update_start_datetime = pd.to_datetime(f"{update_start_date} {update_start_time}")
update_end_datetime = pd.to_datetime(f"{update_end_date} {update_end_time}")

if st.button("Update Reservation"):
    # Check if the required fields are not empty
    if update_reservation_id and (update_start_datetime or update_end_datetime or update_user_id or update_resource_id or update_status_id or update_attendees):
        # Check if the resource_id exists
        cursor.execute("SELECT 1 FROM Resource WHERE resource_id = %s", (update_resource_id,))
        if not cursor.fetchone():
            st.error("Invalid Resource ID. Please enter a valid Resource ID.")
            st.stop()

        # Check if the userid exists
        cursor.execute("SELECT 1 FROM User WHERE userid = %s", (update_user_id,))
        if not cursor.fetchone():
            st.error("Invalid User ID. Please enter a valid User ID.")
            st.stop()

        # Check if the status_id exists
        cursor.execute("SELECT 1 FROM ReservationStatus WHERE status_id = %s", (update_status_id,))
        if not cursor.fetchone():
            st.error("Invalid Status ID. Please enter a valid Status ID.")
            st.stop()

        # Update the data in the Reservation table
        update_reservation_query = """
            UPDATE Reservation
            SET start_time = COALESCE(%s, start_time),
                end_time = COALESCE(%s, end_time),
                resource_id = COALESCE(%s, resource_id),
                userid = COALESCE(%s, userid),
                status_id = COALESCE(%s, status_id),
                attendees = COALESCE(%s, attendees)
            WHERE Reservation_ID = %s
        """
        data = (update_start_datetime, update_end_datetime, update_resource_id, update_user_id, update_status_id, update_attendees, update_reservation_id)
        cursor.execute(update_reservation_query, data)
        db.commit()
        st.success("Reservation details updated successfully.")
    else:
        st.error("Please provide at least one field to update.")

# Streamlit form for deleting reservations
st.subheader("Delete Reservation")

# Fetch all existing reservation IDs
all_reservation_ids_query = "SELECT Reservation_ID FROM Reservation"
cursor.execute(all_reservation_ids_query)
all_reservation_ids = [row[0] for row in cursor.fetchall()]

# Create a dropdown to choose a reservation ID for deletion
delete_reservation_id = st.selectbox("Choose Reservation ID to Delete", all_reservation_ids, key="delete_reservation_id_input")

if st.button("Delete Reservation"):
    # Delete the reservation using the selected ID
    delete_reservation_query = "DELETE FROM Reservation WHERE Reservation_ID = %s"
    cursor.execute(delete_reservation_query, (delete_reservation_id,))
    db.commit()
    st.success("Reservation deleted successfully.")
