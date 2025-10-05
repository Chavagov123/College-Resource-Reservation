import streamlit as st
from database import conn

st.set_page_config(
    page_title="Users",
    page_icon="👤",
)

st.title("User Management")

st.header("Add a New User")
with st.form("user_form"):
    user_name = st.text_input("User Name")
    phno = st.text_input("Phone Number")
    role_options = ["admin", "user"]
    role = st.selectbox("Role", role_options)

    submitted = st.form_submit_button("Submit User")
    if submitted:
        if not user_name or not phno:
            st.error("Please fill in all required fields.")
        else:
            try:
                with conn.session as s:
                    s.execute(
                        'INSERT INTO User (name, phno, role) VALUES (:name, :phno, :role);',
                        params=dict(name=user_name, phno=phno, role=role)
                    )
                    s.commit()
                st.success("User data has been inserted!")
            except Exception as e:
                st.error(f"Error inserting user data: {e}")

st.header("All Users")
try:
    users_df = conn.query('SELECT * FROM user;')
    if users_df.empty:
        st.write("No users found.")
    else:
        st.table(users_df)
except Exception as e:
    st.error(f"Error fetching users: {e}")