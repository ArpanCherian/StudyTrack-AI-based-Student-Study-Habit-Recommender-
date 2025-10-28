# StudyTrack - AI-Powered Student Study Habit Recommender

## Project Overview
StudyTrack is a Django-based web application designed to help students improve their study habits with AI-powered personalized course recommendations, progress tracking, and notifications. Admins can manage students, courses, and send automated reminders.

---

## Features

- User registration and authentication
- Course enrollment and management
- Progress tracking with video and quiz completion
- AI-based course recommendations
- Personalized insights on strengths, weaknesses, and best study times
- Automated email notifications and course reminders
- Admin dashboard for student and course management

---

## Installation

### Prerequisites
- Python 3.8+
- Django 4.2+
- SQLite (default) or other supported database

### Setup Steps
1. Clone the repository: git clone https://github.com/ArpanCherian/StudyTrack-AI-based-Student-Study-Habit-Recommender
- cd StudyTrack

2. Create and activate virtual environment:
- Linux/Mac:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```
- Windows:
  ```
  python -m venv venv
  venv\Scripts\activate
  ```

3. Install dependencies:
pip install -r requirements.txt

4. Configure email settings in `settings.py` for SMTP (e.g., Gmail SMTP with app password).

5. Apply migrations:
python manage.py migrate

6. Run the development server:
python manage.py runserver

8. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Usage

- Students can register, enroll in courses, watch videos, take quizzes, and view personalized AI insights on their dashboard.
- Admins can view all student progress, send email reminders, and manage courses from the admin panel.

---

## AI Features

- **Course Recommendation:** Suggests next best courses based on progress and quiz scores.
- **Study Time Insight:** Analyzes quiz attempt times to suggest users' optimal study hours.
- **Strengths & Weaknesses:** Highlights student's performance on courses.
- **Automated Email Reminders:** Admin-triggered course completion reminders sent via email.

---





## Contact

- Name - Arpan Cherian 
- Mail - arpanjcherian@gmail.com
