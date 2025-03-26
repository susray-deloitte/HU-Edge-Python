# Expense Tracker Application

This is an expense tracker application built with Django. It provides APIs for user authentication, managing occasions, and tracking expenditures.

## Features

- User authentication with JWT (login/signup)
- Create and manage occasions
- Add and clear expenditures
- View expenditure summaries for occasions
- API documentation using Swagger

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd expense-tracker
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   Update the `DATABASES` setting in `expense_tracker/settings.py` with your database configuration.

5. **Run migrations:**
   ```
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```
   python manage.py createsuperuser
   ```

7. **Run the server:**
   ```
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
  - GET `/api/expenditures/summary/{occasion_id}/` - View summary of expenditures for an occasion

## Testing

Run the tests using:
```
python manage.py test
```

## API Documentation

API documentation is available using Swagger. Access it at `http://127.0.0.1:8000/swagger/`.

## License

This project is licensed under the MIT License.