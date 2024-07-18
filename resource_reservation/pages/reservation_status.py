import streamlit as st
from database import get_db_connection

def manage_reservation_status():
    db, cursor = get_db_connection()

    st.title("Reservation Status Manager")

    # Display existing reservation statuses
    cursor.execute("SELECT * FROM ReservationStatus")
    reservation_statuses = cursor.fetchall()

    st.subheader("Existing Reservation Statuses")
    st.table(reservation_statuses)

    # Form to add a new reservation status
    st.subheader("Add New Reservation Status")
    new_status_name = st.text_input("New Status Name")

    if st.button("Add Reservation Status"):
        if new_status_name:
            # Check if the status name already exists
            cursor.execute("SELECT 1 FROM ReservationStatus WHERE status_name = %s", (new_status_name,))
            if cursor.fetchone():
                st.error("Status name already exists. Please choose a different name.")
            else:
                # Insert the new status into the ReservationStatus table
                cursor.execute("INSERT INTO ReservationStatus (status_name) VALUES (%s)", (new_status_name,))
                db.commit()
                st.success("New status added successfully!")
        else:
            st.error("Please enter a status name.")

if __name__ == "__main__":
    manage_reservation_status()
