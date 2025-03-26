# Aidminton

Aidminton is a web application designed to help badminton players track and manage their injuries. This application allows users to create accounts, log injuries, track pain levels, and access resources for injury prevention and recovery.

## Features

- **User Authentication**: Secure signup and login functionality
- **Profile Management**: Users can update their personal information
- **Injury Logging**: Record injury details including title, description, date, and pain level
- **Injury History**: View a log of past injuries
- **Medical Expert Resources**: Access information about medical professionals

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Werkzeug security for password hashing

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/aidminton.git
   cd aidminton
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following content:
   ```
   FLASK_SECRET_KEY=your_secret_key_here
   ```

5. Initialize the database:
   ```
   python init_db.py
   ```

6. Run the application:
   ```
   python app.py
   ```

7. Open your browser and navigate to `http://127.0.0.1:5000`

## Project Structure

- `app.py`: Main application file containing routes and logic
- `init_db.py`: Database initialization script
- `schema.sql`: SQL schema for database tables
- `requirements.txt`: Project dependencies
- `static/`: Static files (CSS, JavaScript, images)
- `templates/`: HTML templates for the application

## Assignment Context

This project was created as part of an academic assignment to demonstrate web application development skills using Flask and SQLite.

## License

This project is submitted for academic purposes and is not licensed for commercial use.
