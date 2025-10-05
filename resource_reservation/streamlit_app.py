import streamlit as st
from database import get_reservation_count_per_resource, get_user_reservation_count, get_user_role

st.set_page_config(
    page_title="Resource Reservation System",
    page_icon="📅",
)

st.title("Resource Reservation System Dashboard")
st.sidebar.success("Select a page above.")

st.header("Reservation Count per Resource")
reservation_count_df = get_reservation_count_per_resource()
st.table(reservation_count_df)

st.title("Get User Information")

user_id_input = st.number_input("Enter User ID:", min_value=1, key="user_id_input")

if st.button("Get User Details"):
    reservation_count = get_user_reservation_count(user_id_input)
    user_role = get_user_role(user_id_input)
    st.write(f"User ID: {user_id_input}")
    st.write(f"Reservation Count: {reservation_count}")
    st.write(f"Role: {user_role}")