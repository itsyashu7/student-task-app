# Student Task Management App

A simple full-stack web application to manage daily student tasks.

##  Features
- Login UI
- Clean project structure
- Responsive design (basic)
- Built using HTML, CSS, and Python (Flask)

##  Tech Stack
- Frontend: HTML, CSS, JS
- Backend: Python (Flask)
- Database: SQLite
- itsdangerous
- Werkzeug Security
- HTML, CSS, JavaScript

##  Project Structure
student-task-app/
│   app.py
│   database.db
│   README.md
│   __init__.py
│
├───.vscode
│       launch.json
│
├───static
│       .gitignore 
│       background.jpg 
│       requirements.txt
│       style.css
│
└───templates
        base.html
        dashboard.html
        forgot_password.html
        login.html
        register.html
        reset_password.html


##  Status

###  Day 1 – Project Setup
- Login page UI created
- Basic Flask setup completed
- Project structure initialized

###  Day 2 – Frontend & Backend Integration
- Flask backend fully integrated with frontend
- HTML templates rendered using Jinja
- CSS linked via static folder
- Base template created
- Dashboard implemented

###  Day 3 – Database Integration
- SQLite database connected
- Tasks stored permanently
- Add task functionality
- View tasks per user
- Delete task feature
- Task status toggle (pending/completed)

###  Day 4 – Session Management & Stability
- Flask session management implemented
- Protected routes from unauthorized access
- Flash messages added for user feedback
- Improved application stability and error handling

###  Day 5 – UI & UX Improvements
- Modern card-based design applied
- Smooth animations added
- Improved visual feedback for task actions
- Layout consistency improvements

###  Day 6 – Authentication System
- Implemented password-based login system
- Users table created with secure password storage
- Password hashing using Werkzeug
- Session-based authentication flow
- Debugged database locking issues

###  Day 7 – Validation & Security Hardening
- Added email field during registration
- Implemented confirm password validation
- Added live password match feedback (JavaScript)
- Backend validation for all registration fields
- Improved security checks and form validation


##  Author
Yash
