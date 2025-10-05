import streamlit as st
from database import conn
from sqlalchemy import text

st.title("Reservation Status Manager")

# Display existing reservation statuses
try:
    reservation_statuses_df = conn.query("SELECT * FROM ReservationStatus", ttl=0)
    st.subheader("Existing Reservation Statuses")
    if reservation_statuses_df.empty:
        st.write("No reservation statuses found.")
    else:
        st.table(reservation_statuses_df)
except Exception as e:
    st.error(f"Error fetching reservation statuses: {e}")

# Form to add a new reservation status
st.subheader("Add New Reservation Status")
new_status_name = st.text_input("New Status Name")

if st.button("Add Reservation Status"):
    if new_status_name:
        try:
            # Check if the status name already exists
            existing = conn.query(
                "SELECT 1 FROM ReservationStatus WHERE status_name = :name",
                params={"name": new_status_name},
            )
            if not existing.empty:
                st.error("Status name already exists. Please choose a different name.")
            else:
                with conn.session as s:
                    s.execute(
                        text("INSERT INTO ReservationStatus (status_name) VALUES (:name);"),
                        params={"name": new_status_name},
                    )
                    s.commit()
                st.success("New status added successfully!")
                st.rerun()
        except Exception as e:
            st.error(f"Error adding reservation status: {e}")
    else:
        st.error("Please enter a status name.")
