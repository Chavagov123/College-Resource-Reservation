import streamlit as st
from database import conn
from sqlalchemy import text

st.set_page_config(
    page_title="Resources",
    page_icon="📦",
)

st.title("Resource Management")

st.header("Add a New Resource")
locations = conn.query("SELECT name FROM Location", ttl=0)
location_names = [row['name'] for index, row in locations.iterrows()]

with st.form("resource_form"):
    type = st.selectbox("Type", ["Lab", "Equipment", "Classroom"])
    name = st.text_input("Name")
    capacity = st.number_input("Capacity", min_value=1)
    location = st.selectbox("Location", location_names)

    submitted = st.form_submit_button("Submit Resource")
    if submitted:
        if name and capacity:
            location_id_df = conn.query(f"SELECT location_id FROM Location WHERE name = '{location}'")
            if not location_id_df.empty:
                location_id = location_id_df.iloc[0]['location_id']
                try:
                    with conn.session as s:
                        s.execute(
                            text('INSERT INTO Resource (type, name, location_id, capacity) VALUES (:type, :name, :location_id, :capacity);'),
                            params=dict(type=type, name=name, location_id=location_id, capacity=capacity)
                        )
                        s.commit()
                    st.success("Resource data has been inserted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error inserting resource data: {e}")
            else:
                st.error("Invalid location selected.")
        else:
            st.error("Please fill in all required fields.")

st.header("All Resources")
try:
    resources_df = conn.query("SELECT * FROM Resource", ttl=0)
    if resources_df.empty:
        st.write("No resources found.")
    else:
        st.table(resources_df)
except Exception as e:
    st.error(f"Error fetching resources: {e}")