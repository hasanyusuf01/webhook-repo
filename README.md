
# 🚀 GitHub Webhook Receiver with Flask + MongoDB

This project implements a Flask-based webhook receiver that listens to GitHub events (`push`, `pull_request`, `merge`) and stores them in MongoDB. A minimal frontend UI displays these events in real-time, refreshing every 15 seconds.

---

## 🧱 Features

- Accepts GitHub Webhooks via `/webhook`
- Stores event data (author, action, branches, timestamp) in MongoDB
- Frontend UI polls every 15 seconds and displays activity feed
- Simple `clear` endpoint to delete all events

---





---

## ⚙️ Environment Setup

You can use either **Conda** or Python **virtual environment (`venv`)**.

---

##  Option 1: Using Conda (Recommended)

### Create a new Conda environment
```
conda create -n webhook-env python=3.11 -y
```
### Activate the environment
```
conda activate webhook-env

```

### Install project dependencies
```
pip install -r requirements.txt

```
---

## 🔹 Option 2: Using venv

### Create a virtual environment
```
python3 -m venv venv
```

### Activate the environment
```
source venv/bin/activate
```

### Windows: 
```
venv\Scripts\activate
```

### Install project dependencies
```
pip install -r requirements.txt

```
---

## 🔌 MongoDB Setup (Local)

### ✅ Step 1: Install MongoDB (if not already)

```
sudo apt update
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb

```
Check Mongo is running:

```
sudo systemctl status mongodb

```
If not then start MongoDB:

```
sudo systemctl start mongodb

```
### ✅ Step 2: 

Open Mongo Shell

```
mongosh

```
🛠 Step 4: Run This Inside Mongo Shell

```
use github_events

db.createCollection("events", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["author", "from_branch", "to_branch", "action", "timestamp"],
      properties: {
        author: { bsonType: "string" },
        from_branch: { bsonType: "string" },
        to_branch: { bsonType: "string" },
        action: {
          enum: ["push", "pull_request", "merge"]
        },
        timestamp: { bsonType: "date" }
      }
    }
  },
  validationLevel: "strict"
})

```
This creates a github_events.events collection that enforces your schema.

### ✅ Optional: View stored data

```
mongosh
> use github_events
> db.events.find().pretty()
```

### 🚀 Run the Flask App

Once dependencies are installed and MongoDB is running:

```
python3 app.py

```


The app will run at:  
[http://localhost:5000](http://localhost:5000)

---

## 🌐 Expose Locally Running App Using ngrok
### Using ngrok for public endpoint:
```
ngrok http 5000

```
To receive GitHub webhooks, expose your local server to the internet:








Copy the generated public URL and set it as your webhook endpoint in your GitHub repository settings (e.g., `https://<your-ngrok-id>.ngrok.io/webhook`).

---

## 🔑 GitHub Webhook Configuration

1. Go to your repository **Settings** > **Webhooks** > **Add webhook**.
2. Set the **Payload URL** to your public ngrok URL + `/webhook` (e.g., `https://<your-ngrok-id>.ngrok.io/webhook`).
3. Set **Content type** to `application/json`.
4. Select individual events or "Just the push event" as needed.
5. Click **Add webhook**.

---

## 📝 Additional Notes

- **Security:** For production, secure your endpoints and consider authentication.
- **Polling Interval:** The frontend UI refreshes every 15 seconds; you can adjust this in `index.html`.
- **MongoDB URI:** If using a remote MongoDB instance, update the connection URI in `app.py`.
- **Clear Events:** Use the `/clear` endpoint to remove all stored events.

---

## 💡 Troubleshooting

- **MongoDB Connection Issues:** Ensure MongoDB is running and accessible.
- **Webhook Delivery Issues:** Check your ngrok tunnel is active and the URL is correct in GitHub settings.
- **Dependencies:** If you see import errors, double-check your Python environment and `requirements.txt`.

---

## 📜 License

MIT License

---


