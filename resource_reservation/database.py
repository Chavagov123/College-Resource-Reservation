import streamlit as st
import mysql.connector

def get_db_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="resource_reservation_system"
    )
    cursor = db.cursor(buffered=True)
    return db, cursor

def get_reservation_count_per_resource(db, cursor):
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
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()

    return results

def get_user_reservation_count(db, cursor, user_id):
    query = """
        SELECT (
            SELECT COUNT(*)
            FROM Reservation r
            WHERE r.userid = u.userid
        ) AS reservation_count
        FROM User u
        WHERE u.userid = %s
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]

    return 0
