import streamlit as st
import pandas as pd
from database import conn
from sqlalchemy import text

st.set_page_config(
    page_title="Reservations",
    page_icon="📅",
)

st.title("Reservation Management")

def fetch_all_ids(table, id_column):
    df = conn.query(f"SELECT {id_column} FROM {table}", ttl=0)
    return [row[id_column] for index, row in df.iterrows()]

st.header("Add a New Reservation")
with st.form("reservation_form"):
    start_date = st.date_input("Start Date")
    start_time = st.time_input("Start Time")
    end_date = st.date_input("End Date")
    end_time = st.time_input("End Time")

    user_ids = fetch_all_ids("User", "userid")
    resource_ids = fetch_all_ids("Resource", "resource_id")
    status_ids = fetch_all_ids("ReservationStatus", "status_id")

    user_id = st.selectbox("User ID", user_ids)
    resource_id = st.selectbox("Resource ID", resource_ids)
    status_id = st.selectbox("Status ID", status_ids)
    attendees = st.number_input("Number of Attendees", min_value=1)

    submitted = st.form_submit_button("Submit Reservation")
    if submitted:
        start_datetime = pd.to_datetime(f"{start_date} {start_time}")
        end_datetime = pd.to_datetime(f"{end_date} {end_time}")

        if start_datetime and end_datetime and user_id and resource_id and status_id and attendees:
            try:
                with conn.session as s:
                    s.execute(
                        text('INSERT INTO Reservation (start_time, end_time, resource_id, userid, status_id, attendees) VALUES (:start, :end, :res_id, :user_id, :stat_id, :attendees);'),
                        params=dict(start=start_datetime, end=end_datetime, res_id=resource_id, user_id=user_id, stat_id=status_id, attendees=attendees)
                    )
                    s.commit()
                st.success("Reservation data has been inserted!")
                st.rerun()
            except Exception as e:
                st.error(f"Error inserting reservation data: {e}")
        else:
            st.error("Please fill in all required fields.")

st.header("All Reservations")
try:
    reservations_df = conn.query("SELECT * FROM Reservation", ttl=0)
    if reservations_df.empty:
        st.write("No reservations found.")
    else:
        st.table(reservations_df)
except Exception as e:
    st.error(f"Error fetching reservations: {e}")

st.subheader("Update Reservation Status")
with st.form("update_status_form"):
    reservation_ids = fetch_all_ids("Reservation", "Reservation_ID")
    reservation_id = st.selectbox("Reservation ID", reservation_ids)
    new_status_id = st.selectbox("New Status ID", status_ids)

    update_status_submitted = st.form_submit_button("Update Reservation Status")
    if update_status_submitted:
        try:
            with conn.session as s:
                s.execute(text('CALL UpdateReservationStatus(:res_id, :new_stat_id);'), params=dict(res_id=reservation_id, new_stat_id=new_status_id))
                s.commit()
            st.success("Reservation status updated successfully.")
        except Exception as e:
            st.error(f"Error updating reservation status: {e}")

st.subheader("Delete Reservation")
with st.form("delete_reservation_form"):
    delete_reservation_id = st.selectbox("Choose Reservation ID to Delete", reservation_ids)

    delete_submitted = st.form_submit_button("Delete Reservation")
    if delete_submitted:
        try:
            with conn.session as s:
                s.execute(text('DELETE FROM Reservation WHERE Reservation_ID = :res_id;'), params=dict(res_id=delete_reservation_id))
                s.commit()
            st.success("Reservation deleted successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Error deleting reservation: {e}")