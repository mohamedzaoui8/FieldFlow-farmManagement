# FieldFlow

**FieldFlow** is a farm workforce management system designed to manage workers, attendance, payroll, and farm operations through a role-based web application.

The project consists of a **FastAPI backend**, a **web frontend**, and a **Postman API test collection**.

## Features

* JWT-based authentication
* Role-based access control
* Owner and Chef roles
* Worker management
* Chef management
* Worker assignment to chefs
* Attendance management
* Attendance submission workflow
* Payroll management
* User activation/deactivation
* Database migrations with Alembic
* RESTful API
* Postman API collection for testing

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* MySQL
* Alembic
* JWT Authentication

### Frontend

* HTML
* CSS
* JavaScript

### API Testing

* Postman

## User Roles

### Owner

The Owner has administrative access to the system and can:

* Manage users
* Create and deactivate Chefs
* Manage workers
* Manage chef assignments
* Access payroll information

### Chef

The Chef is responsible for managing assigned workers and their attendance.

A Chef can:

* View assigned workers
* Manage attendance
* Submit attendance records
* Access relevant worker information

### Worker

Workers do not have individual accounts.

They are managed by the Owner and assigned to Chefs.

## Project Structure

```text
FieldFlow/
│
├── back-end/
│   ├── alembic/
│   └── app/
│       ├── core/
│       ├── database/
│       ├── models/
│       ├── routers/
│       ├── schemas/
│       └── services/
│
├── front-end/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── postman/
│   ├── collections/
│   ├── environments/
│   └── globals/
│
├── .gitignore
└── README.md
```

## API

The backend exposes RESTful API endpoints for:

* Authentication
* Users
* Chefs
* Workers
* Attendance
* Jobs
* Payroll

API documentation is available through FastAPI's automatically generated documentation:

```text
/docs
```

and:

```text
/redoc
```

when the backend is running.

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:mohamedzaoui8/FieldFlow-farmManagement.git
cd FieldFlow-farmManagement
```

### 2. Create a virtual environment

```bash
cd back-end
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file inside `back-end/`.

Example:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

Do not commit `.env` to GitHub.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the backend

```bash
uvicorn app.main:app --reload
```

The API will then be available locally.

## Database

The project uses **MySQL** with **SQLAlchemy** as the ORM.

Database schema changes are managed using **Alembic migrations**.

## Testing

API endpoints can be tested using the Postman collection included in:

```text
postman/collections/
```

## Project Status

FieldFlow is an ongoing project. The core backend functionality, authentication, role-based access control, worker management, attendance, and payroll features have been implemented.

## Future Improvements

* Automated testing with pytest
* Dockerization
* Production deployment
* PostgreSQL support
* Refresh token implementation
* Rate limiting
* Improved frontend UI/UX
* CI/CD pipeline

## Author

**Mohamed Zaoui**

Python Backend Developer — FastAPI / REST APIs
