# Student Task Management App

A simple full-stack web application to manage daily student tasks.

##  Features
- Login UI
- Clean project structure
- Responsive design (basic)
- Built using HTML, CSS, and Python (Flask)

##  Tech Stack
- Frontend: HTML, CSS
- Backend: Python (Flask)
- Database: SQLite (to be added)

##  Project Structure
student-task-app/
│
├── app.py                  # Main Flask application
├── database.db             # SQLite database
├── requirements.txt        # Python dependencies (optional now)
│
├── templates/              # HTML (Jinja templates)
│   ├── base.html           # Common layout (navbar, styles)
│   ├── login.html          # Login page
│   └── dashboard.html      # Dashboard (tasks view)
│
├── static/                 # Static files
│   ├── style.css           # Main CSS file
│
├── README.md               # Project documentation
└── .gitignore              # Files to ignore in Git


##  Status
Day 1 completed – Login page UI and setup done.

Day 2 completed - Combined Day 2 & Day 3 work finished.
- Flask backend fully integrated with frontend
- HTML templates rendered using Flask
- CSS successfully linked using static folder
- Base template created
- Dashboard implemented

Day 3 completed - creation of db and flask corrections
- Flask sessions implemented (login persistence)
- SQLite database integration
- Tasks stored permanently
- Add task functionality
- View tasks per user
- Delete task feature
- Mark task as completed / pending

Day 4 completed -User sessions and database integration completed

- Implemented Flask session management for login persistence
- Protected routes to prevent unauthorized access
- Integrated SQLite database for permanent task storage
- Created tasks table with user-wise task mapping
- Implemented add task functionality with database storage
- Implemented delete task feature
- Implemented task status toggle (pending / completed)
- Added flash messages for user feedback
- Improved application stability and security checks

Day 5 completed -Focused on frontend polish and user experience improvements

- Improved overall UI to a modern, clean card-based design
- Enhanced user experience with smooth animations for task actions
- Improved visual feedback for task actions (add, delete, toggle)
- Performed UI and UX cleanup for better readability and layout consistency

Day 6 completed -focused on password login and hashing a password
- Password auth logic
- Users & tasks tables
- Session handling
- Real debugging
- Architecture testing

##  Author
Yash
