
# 🚀 GitHub Webhook Receiver with Flask + MongoDB

This project implements a Flask-based webhook receiver that listens to GitHub events (`push`, `pull_request`, `merge`) and stores them in MongoDB. A minimal frontend UI displays these events in real-time, refreshing every 15 seconds.

---

## 🧱 Features

- Accepts GitHub Webhooks via `/webhook`
- Stores event data (author, action, branches, timestamp) in MongoDB
- Frontend UI polls every 15 seconds and displays activity feed
- Simple `clear` endpoint to delete all events

---

## 📁 Project Structure

webhook-repo/
├── app.py # Flask backend + webhook handler
├── templates/
│ └── index.html # UI for event feed
├── requirements.txt # Python dependencies
└── README.md # This file



---

## ⚙️ Environment Setup

You can use either **Conda** or Python **virtual environment (`venv`)**.

---

###  Option 1: Using Conda (Recommended)

# Create a new Conda environment
conda create -n webhook-env python=3.11 -y

# Activate the environment
conda activate webhook-env

# Install project dependencies
pip install -r requirements.txt


### 🔹 Option 2: Using venv

# Create a virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install project dependencies
pip install -r requirements.txt

### 🔌 MongoDB Setup (Local)

Make sure MongoDB is installed and running.

✅ Start MongoDB:

sudo systemctl start mongodb


✅ Optional: View stored data

mongosh
> use github_events
> db.events.find().pretty()

### 🚀 Run the Flask App

Once dependencies are installed and MongoDB is running:

python3 app.py

The app will run on:

http://localhost:5000

### Using ngrok for public endpoint:

ngrok http 5000
