# Expense Tracker

A lightweight web-based Expense Tracker to record, categorize, and review personal expenses. Built using HTML for the frontend and Python for the backend, this repository provides a minimal, easy-to-extend foundation for personal finance tracking.

---

## Features
- Add, edit, and delete expense entries
- Categorize expenses (e.g., Food, Transport, Bills, Entertainment)
- View expense history and totals by date or category
- Export data to CSV/JSON (optional)
- Simple, easy-to-read codebase ready for extensions

---

## Tech stack
- Frontend: HTML (+ optional CSS/JavaScript)
- Backend: Python (Flask recommended; can be adapted to other frameworks)
- Storage: Local file (CSV/JSON) or SQLite or MongoDB (configurable)

---

## Project structure (example)
- static/ — frontend assets (CSS, JS, images)
- templates/ — HTML templates (if using Flask/Jinja2)
- app.py — application entrypoint (or main Python file)
- example_app.py — example showing .env + MongoDB usage
- requirements.txt — Python dependencies
- data/ or db.sqlite3 — local storage (if used)
- README.md — this file

Adjust the structure above to match the repository contents if different.

---

## Prerequisites
- Python 3.8+
- pip
- Optional: virtualenv or venv
- Optional: Git

---

## Environment & Secrets (local development)

This project uses a local `.env` file to store secrets (for example MONGODB_URI and SECRET_KEY). Do NOT commit your `.env` file. Commit a `.env.example` with placeholder values so contributors know which variables to set.

Required environment variables
- MONGODB_URI — MongoDB connection string (Atlas URI or mongodb://...).
- SECRET_KEY — App secret for session signing / cookies.
- FLASK_ENV — Optional (e.g., `development`).

If you accidentally committed `.env`
1. Remove it from the repo cache and commit:
   ```
   git rm --cached .env
   git commit -m "Remove .env"
   git push
   ```
2. Rotate any secrets you exposed (create a new DB user / change passwords, rotate keys).

For production, use your host’s secret manager or environment variable features rather than a `.env` file.

---

## Quick start

1. Clone the repository
   ```bash
   git clone https://github.com/Varun-kb/Expense_Tracker.git
   cd Expense_Tracker
   ```

2. Create and activate a virtual environment
   - macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
   or at minimum:
   ```bash
   pip install python-dotenv pymongo Flask
   ```

4. Create `.env` from the example and fill real values:
   - macOS / Linux:
     ```bash
     cp .env.example .env
     ```
   - Windows (PowerShell):
     ```powershell
     copy .env.example .env
     ```

5. Run the app
   - If using Flask:
     ```bash
     export FLASK_APP=example_app.py
     export FLASK_ENV=development
     flask run
     ```
     or
     ```bash
     python example_app.py
     ```

6. Open in your browser:
   - Flask default: http://127.0.0.1:5000/

---

## Usage
- Use the "Add Expense" form to record expenses with date, amount, category, and notes.
- View and filter expenses by date or category on the history page.
- Export or back up data via CSV/JSON if the feature is implemented.

---

## Docker (optional)
A simple Dockerfile and docker-compose.yml may be added to containerize the app:
```bash
docker build -t expense-tracker .
docker run -p 5000:5000 expense-tracker
```

---

## Tests
- If tests exist, run them with:
  ```bash
  pytest
  ```

---

## Contributing
Contributions are welcome. Suggested workflow:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feat/my-feature
   ```
3. Commit and push your changes:
   ```bash
   git push origin feat/my-feature
   ```
4. Open a pull request describing your changes and any setup steps.

Please include tests and update this README with any new setup or runtime instructions.

---

## Roadmap / Ideas
- Add user authentication and multi-user support
- Integrate charts (Chart.js) for spending visualization
- Add recurring expenses and budget alerts
- Mobile-first responsive UI
- Import from bank/export CSV integrations

---

## Troubleshooting
- ModuleNotFoundError: ensure virtualenv is activated and requirements installed.
- Port in use: specify a different port when running or stop the conflicting process.
- Database migrations: if using a framework with migrations, run the appropriate migration commands.

---

## License
This project is provided under the MIT License by default. Replace with your preferred license if different.

---

## Contact
Maintained by Varun-kb. For issues or contributions, open an issue or submit a pull request on GitHub.
