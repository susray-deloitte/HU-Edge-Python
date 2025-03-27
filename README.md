# Expense Tracker Application

This is an expense tracker application built with Django. It provides APIs for user authentication, managing occasions, and tracking expenditures.

## Features

- User authentication with JWT (login/signup)
- Create and manage occasions
- Add, clear, and view expenditures
- View expenditure summaries for occasions
- API documentation using Swagger

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd expense-tracker
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   Update the `DATABASES` setting in `expense_tracker/settings.py` with your database configuration.

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the API:**
   The API endpoints can be accessed at `http://127.0.0.1:8000/api/`.

## API Endpoints

- **User Authentication:**
  - POST `/api/users/signup/` - Register a new user
  - POST `/api/users/login/` - Login and receive a JWT token

- **Occasions:**
  - POST `/api/occasions/` - Create a new occasion
  - GET `/api/occasions/` - List all occasions
  - GET `/api/occasions/{id}/` - Retrieve an occasion
  - DELETE `/api/occasions/{id}/` - Clear an occasion

- **Expenditures:**
  - POST `/api/expenditures/` - Add a new expenditure
  - GET `/api/expenditures/` - List all expenditures
  - POST `/api/clear-expense/` - Clear an expenditure by paying the required amount
  - GET `/api/occasions/{id}/summary/` - View summary of expenditures for an occasion

## Testing

Run the tests using:
```bash
python manage.py test
```

## API Documentation

API documentation is available using Swagger. Access it at:
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## License

This project is licensed under the MIT License.