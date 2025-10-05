# Resource Reservation System

This is a Streamlit-based web application for managing and reserving resources such as labs, equipment, and classrooms. It provides a user-friendly interface for administrators and users to manage resources, users, and reservations.

## Project Structure

The project is organized as follows:

- `streamlit_app.py`: The main application file that serves as the dashboard.
- `pages/`: This directory contains the different pages of the Streamlit application.
  - `1_Users.py`: User management page.
  - `2_Resources.py`: Resource management page.
  - `3_Reservations.py`: Reservation management page.
- `database.py`: Handles the database connection and queries.
- `requirements.txt`: A list of Python dependencies for the project.
- `resource_reservation_system.sql`: The SQL script to set up the database schema and stored procedures.

## Setup Instructions

### Prerequisites

- Python 3.7+
- MySQL Server

### 1. Database Setup

1.  **Create the database:**
    ```sql
    CREATE DATABASE resource_reservation_system;
    ```

2.  **Use the database:**
    ```sql
    USE resource_reservation_system;
    ```

3.  **Run the `resource_reservation_system.sql` script** to create the necessary tables, stored procedures, and sample data. You can do this via the MySQL command line or a GUI tool like MySQL Workbench.

    ```bash
    mysql -u your_username -p resource_reservation_system < resource_reservation_system.sql
    ```

### 2. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection

The application uses Streamlit's `st.connection` to manage the database connection. You need to configure the connection details in Streamlit's secrets management.

Create a file at `~/.streamlit/secrets.toml` and add the following content, replacing the placeholders with your MySQL credentials:

```toml
[connections.mysql]
dialect = "mysql"
host = "localhost"
port = 3306
database = "resource_reservation_system"
username = "your_username"
password = "your_password"
```

## How to Run the Application

To run the Streamlit application, navigate to the `resource_reservation` directory and run the following command:

```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501` in your web browser.

## Features

- **Dashboard**: View key statistics like reservation counts per resource.
- **User Management**: Add and view users.
- **Resource Management**: Add and view resources.
- **Reservation Management**: Create, view, update, and delete reservations.
- **Role-Based Access**: (Future enhancement) Implement different views and permissions for admins and users.
- **Search and Filtering**: (Future enhancement) Easily find specific resources or reservations.