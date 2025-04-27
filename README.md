# Faculty Appraisal System

A comprehensive Streamlit-based Faculty Appraisal System that provides role-specific dashboards for Faculty, Dean, and Students to manage and evaluate academic performance.

## Features

- Role-based access control (Faculty, Dean, Student)
- Publication and experience tracking
- Feedback submission and management
- Authentication system with multi-role support
- PostgreSQL database integration
- Responsive Streamlit interface

## Installation

1. Clone this repository
2. Install the dependencies:
   ```
   pip install -r requirements_for_deployment.txt
   ```

## Database Setup

The application uses a PostgreSQL database. You need to set up the connection by configuring the following environment variables:

- `DATABASE_URL`: The complete connection URL for PostgreSQL
- `PGHOST`: PostgreSQL host
- `PGPORT`: PostgreSQL port
- `PGUSER`: PostgreSQL username
- `PGPASSWORD`: PostgreSQL password
- `PGDATABASE`: PostgreSQL database name

You can set these variables in a `.env` file or directly in your deployment environment.

## Running the Application

```
streamlit run app.py
```

## Default Users

The application comes with three default users:

- Faculty: username "john", password "faculty123"
- Dean: username "jane", password "dean123"
- Student: username "mike", password "student123"

## Deployment on Streamlit Cloud

1. Push this code to a GitHub repository
2. Connect your repository to Streamlit Cloud
3. Set the required environment variables in the Streamlit Cloud dashboard
4. Deploy

## Project Structure

- `app.py`: Main application file
- `auth.py`: Authentication related functions
- `data_manager.py`: Data management functions
- `db_setup.py`: Database models and setup
- `dashboards/`: Role-specific dashboard implementations
  - `faculty.py`: Faculty dashboard
  - `dean.py`: Dean dashboard
  - `student.py`: Student dashboard
- `.streamlit/config.toml`: Streamlit configuration