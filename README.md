# ChronoCare-AI: AI-Driven Health Monitoring Platform

## Overview

Welcome to **ChronoCare-AI**, a cutting-edge web application designed to empower users to monitor their daily health habits, predict future health outcomes, and access seamless doctor appointments—all in one place. Founded on May 9th, 2025, by Prashanth and Sushanth Reddy, this project aims to revolutionize personal wellness by leveraging data-driven insights and an intuitive user interface. Whether you're tracking your sleep, booking a consultation, or exploring your health predictions, ChronoCare-AI is your partner for a healthier, longer life.

This project is built with a focus on user empowerment, security, and accessibility, making it an ideal showcase for developers interested in health-tech, web development, and data analytics.

## Features

- **Daily Health Monitoring**: Users can input daily lifestyle data (sleep hours, diet quality, exercise minutes, stress levels) and view detailed dashboards with trends and suggestions.
- **Health Predictions**: Provides personalized health scores, estimated life expectancy, and tailored recommendations based on lifestyle data using rule-based algorithms.
- **7-Day Lifestyle Forecast**: Utilizes linear regression to predict future sleep and exercise trends, helping users plan their wellness routine.
- **Insights Analysis**: Offers a deep dive into the last 7 days of data with feedback on sleep quality, exercise habits, and stress management.
- **Doctor Appointments**: Enables users to book and cancel appointments with doctors, complete with dynamic slot availability and secure authentication.
- **Interactive Chatbot**: A health assistant that provides tips on diet, exercise, stress, and more, with a fun twist for specific users.
- **Report Generation**: Generates downloadable PDF reports summarizing health data, forecasts, and predictions.
- **Secure User Authentication**: Implements sign-up, login, and logout with password hashing for data security.
- **Contact Us**: Allows users to send messages to the admin via email.

## 📸 Screenshots

### Home Page
![Home Page](screenshots/Home-Page.jpg)
*The welcoming homepage of ChronoCare-AI featuring an intuitive interface and easy navigation to all key features.*

### Lifestyle Input Form
![Lifestyle Input Form](screenshots/Lifestyle-Input-Form.jpg)
*Users can easily input their daily health data including sleep hours, diet quality, exercise minutes, and stress levels.*

### Dashboard
![Dashboard](screenshots/Dashboard-Page.jpg)
*Comprehensive dashboard displaying health trends, analytics, and personalized insights based on user data.*

### Health Predictions
![Health Prediction Page](screenshots/Health-Prediction-Page.jpg)
*AI-powered health predictions showing personalized health scores, life expectancy estimates, and tailored recommendations.*

### Doctor Appointments
![Doctor Appointment Page](screenshots/Doctor-Appointment-Page.jpg)
*Seamless appointment booking system with dynamic slot availability and doctor selection.*

### Interactive Chatbot
![Chatbot](screenshots/Chatbot.jpg)
*AI-powered health assistant providing personalized tips and answering health-related questions.*

## Project Structure

The project is organized into a modular Flask application structure. Below is the detailed folder and file layout:

```
ChronoCare-AI/
├── app/
│   ├── __init__.py         # Initializes the Flask app with create_app() function
│   ├── models.py           # Defines database models (User, LifestyleData, Doctor, Appointment)
│   ├── predictor.py        # Contains the predict_health function for health predictions
│   └── routes.py           # Contains all route definitions (e.g., /lifestyle_form, /appointments)
├── instance/               # Contains database or configuration files (e.g., SQLite database)
├── migrations/             # Directory for database migration scripts (if using Flask-Migrate)
├── static/                 # Contains static files (CSS, JS, images)
├── templates/              # Contains HTML templates (e.g., farewell.html, intro.html, chatbot.html)
├── config.py               # Configuration settings (e.g., database URI, secret key)
├── main.py                 # Alternative entry point or script
├── run.py                  # Main script to run the Flask app, imports create_app()
└── README.md               # This file (project documentation)
```

- **Root Files**: run.py serves as the entry point, importing create_app() from app/__init__.py to start the server.
- **App Folder**: Houses the core application logic, separated into models, routes, and prediction logic.
- **Templates and Static**: Manage the frontend presentation and assets.
- **Instance and Migrations**: Handle database persistence and schema updates.

## Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Flask-Mail, Flask-JWT-Extended, xhtml2pdf, NumPy, PyMySQL, certifi, charset-normalizer
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: MySQL (via PyMySQL), SQLite (for development)
- **Deployment**: Gunicorn (production server)
- **Development Tools**: PyCharm, Git, GitHub

## How to Run

Follow these step-by-step instructions to set up and run ChronoCare-AI locally:

### 1. Clone the Repository
Open a terminal and run:
```bash
git clone https://github.com/sushanthreddy009/chronocare.git
```

Move the project to a specific folder (e.g., Desktop or Downloads):
- **On Windows**: Move the chronocare folder to `C:\Users\YourUsername\Desktop` or `C:\Users\YourUsername\Downloads`.
- **On macOS/Linux**: Move to `~/Desktop` or `~/Downloads`.

### 2. Open in PyCharm
- Launch PyCharm.
- Go to **File > Open** and navigate to the chronocare folder you moved.
- Select the folder and click **OK** to open the project.

### 3. Set Up a Virtual Environment
In the PyCharm terminal, run:
```bash
python -m venv venv
```

Activate the virtual environment:
- **On Windows**: `venv\Scripts\activate`
- **On macOS/Linux**: `source venv/bin/activate`

You should see `(venv)` in your terminal prompt.

### 4. Install Dependencies
Run one of the following commands:
```bash
pip install flask flask_sqlalchemy flask_migrate flask_bcrypt flask_jwt_extended flask_mail xhtml2pdf pyhanko numpy pymysql certifi charset_normalizer
```

OR

```bash
pip install -r requirements.txt
```

**Note**: If requirements.txt is not present, use the first command to install all dependencies. Afterward, generate requirements.txt with:
```bash
pip freeze > requirements.txt
```

### 5. Configure config.py
Open `config.py` and modify the following details with your credentials:

**Database URI**: Update the `SQLALCHEMY_DATABASE_URI` to connect to your MySQL database. Example:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'
```

- **Username and Password**: Replace `username` and `password` with your MySQL credentials.
- **Database Creation**: Use MySQL Workbench to create a database named `db_name` (or your preferred name) and ensure the user has privileges.

Other settings (e.g., `SECRET_KEY`) can be generated randomly:
```python
import os
SECRET_KEY = os.urandom(24)
```

### 6. Initialize and Apply Database Migrations
In the PyCharm terminal (with the virtual environment activated), run:

```bash
flask db init
```
This initializes the migration repository.

Then run:
```bash
flask db migrate -m "Initial migration"
```
This generates migration scripts based on your models.

Finally, apply the migrations:
```bash
flask db upgrade
```
This creates the database tables (e.g., users, lifestyle_data, doctors, appointments).

### 7. Run the Application
In the PyCharm terminal, run:
```bash
python run.py
```

The app should start on `http://0.0.0.0:5007` (or check the terminal output for the URL).
Open a browser and visit `http://localhost:5007` to access the app.

## Deployment (Optional)

To deploy ChronoCare-AI to a platform like Render:

1. Push your code to GitHub (already done).
2. Create a `requirements.txt` if not present (see Step 4 above).
3. Follow Render's deployment guide (available at https://render.com/docs/deploy-flask) with the start command:
   ```
   gunicorn --bind 0.0.0.0:5000 "app:create_app()"
   ```
4. Add environment variables (e.g., `FLASK_ENV=production`, `SECRET_KEY`) in the Render dashboard.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details (if not present, consider adding one).

## Contact

For questions or support, reach out to:

- **Email**: sushanthreddy717@gmail.com
- **GitHub**: https://github.com/sushanthreddy009

## Acknowledgments

- Inspired by the vision of Prashanth and Sushanth Reddy to create a health-tech solution.
- Built with love using open-source tools and libraries from the Python community.

Happy coding, and enjoy exploring ChronoCare-AI!
