import streamlit as st
import mysql.connector

conn = st.connection('mysql', type='sql')

def get_reservation_count_per_resource():
    # Execute the query
    query = """
        SELECT
            Resource.resource_id,
            Resource.name AS resource_name,
            COUNT(Reservation.Reservation_ID) AS reservation_count
        FROM
            Resource
        LEFT JOIN
            Reservation ON Resource.resource_id = Reservation.resource_id
        GROUP BY
            Resource.resource_id, resource_name
        ORDER BY
            reservation_count DESC;
    """
    df = conn.query(query)

    return df

def get_user_reservation_count(user_id):
    query = """
        SELECT (
            SELECT COUNT(*)
            FROM Reservation r
            WHERE r.userid = u.userid
        ) AS reservation_count
        FROM User u
        WHERE u.userid = :user_id
    """
    df = conn.query(query, params={'user_id': user_id})
    if not df.empty:
        return df.iloc[0]['reservation_count']

    return 0

def get_user_role(user_id):
    df = conn.query("SELECT role FROM User WHERE userid = :user_id", params={'user_id': user_id})
    if not df.empty:
        return df.iloc[0]['role']
    return "Unknown"