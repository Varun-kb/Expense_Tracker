# app.py
# This is the MAIN file that starts our Flask web server.
# Run this file to start the backend: python app.py

from flask import Flask
from flask_cors import CORS

# Import our route blueprints
from routes.auth     import auth_bp
from routes.tasks    import tasks_bp
from routes.expenses import expenses_bp

# ─────────────────────────────────────────────
# Create the Flask app
# ─────────────────────────────────────────────
app = Flask(__name__)

# Allow the frontend (running on a different port) to talk to our backend
# CORS = Cross-Origin Resource Sharing
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500",
                   "http://localhost:3000", "null"],
     supports_credentials=True)

# ─────────────────────────────────────────────
# Register all our routes
# ─────────────────────────────────────────────
app.register_blueprint(auth_bp,     url_prefix="/api/auth")
app.register_blueprint(tasks_bp,    url_prefix="/api/tasks")
app.register_blueprint(expenses_bp, url_prefix="/api/expenses")


# ─────────────────────────────────────────────
# Health check route — visit http://localhost:5000/
# to confirm the server is running
# ─────────────────────────────────────────────
@app.route("/")
def home():
    return {"message": "TaskFlow API is running! ✅", "version": "1.0"}


# ─────────────────────────────────────────────
# Start the server
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  TaskFlow Backend Server Starting...")
    print("  URL: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
