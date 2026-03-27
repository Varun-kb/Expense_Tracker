# config.py
# This file connects our Flask app to MongoDB Atlas

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load values from the .env file
load_dotenv()

# Read the MongoDB connection string from .env
MONGO_URI = os.getenv("MONGO_URI")

# Read the secret key used for creating login tokens
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-please-change")

# Create the MongoDB connection
client = MongoClient(MONGO_URI)

# Select our database named "taskflow"
db = client["taskflow"]

# These are our collections (like tables in a regular database)
users_col     = db["users"]       # stores user accounts
tasks_col     = db["tasks"]       # stores tasks
expenses_col  = db["expenses"]    # stores expenses
