# ⏱️ Productivity Tracker

A web app to set weekly hour-based goals, track how much time you actually spend on them, and build a daily streak — with a built-in timer so you don't even need a stopwatch.

## 📖 About the Project

Productivity Tracker helps you stay accountable to your own goals. After logging in, you set a weekly target in hours, then log your work either manually or by starting the built-in timer while you work. The dashboard shows how you're doing against your target for the week, month, and overall — plus how many days in a row you've kept up the habit.

## ✨ Features

- User registration and login
- Set a **weekly goal in hours**, editable anytime
- Dashboard showing **target vs. completed hours** for the week, month, and all-time
- **Daily streak** tracking to build consistency
- Manual hour logging, or use the **built-in timer** — start, pause, stop, and reset
- One-click **"Log Hours"** button that saves the time tracked by the timer straight to your daily record
- Fully **mobile-responsive** design

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (timer logic)
- **Database:** SQLite (default)

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Heisenberg-m/productivity-app.git
cd productivity-app
```

### 2. Set up a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file (or update `settings.py` directly) with:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
```

### 4. Run migrations and start the server

```bash
python manage.py migrate
python manage.py createsuperuser   # optional, for admin access
python manage.py runserver
```

The app will be running at `http://127.0.0.1:8000/`.

## 🧑‍💻 Usage

1. Register an account and log in.
2. Set your weekly goal in hours.
3. Log your work either manually, or start the timer at the beginning of a session and click **Log Hours** when you're done.
4. Check your dashboard to see target vs. completed hours and your current streak.

## 🔮 Future Improvements

- Charts/graphs for visualizing progress over time
- Reminders/notifications for unlogged days
- Multiple goal categories (e.g. study, work, exercise)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋 Author

**Mridul Anand**
📧 mridul.katyayan@gmail.com
🔗 [github.com/Heisenberg-m](https://github.com/Heisenberg-m)
