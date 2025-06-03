from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.github_events
collection = db.events

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def github_webhook():
    payload = request.json

    try:
        # PUSH EVENT
        if 'commits' in payload and payload.get("pusher"):
            data = {
                "request_id": payload["head_commit"]["id"],  # Git commit SHA
                "author": payload["pusher"]["name"],
                "action": "PUSH",
                "from_branch": None,
                "to_branch": payload["ref"].split("/")[-1],
                "timestamp": datetime.utcnow().isoformat()  # Store as string(datetime)
            }
            collection.insert_one(data)



        # PULL REQUEST & MERGE EVENT
        elif payload.get("pull_request"):
            pr = payload["pull_request"]
            from_branch = pr["head"]["ref"]
            to_branch = pr["base"]["ref"]
            author = pr["user"]["login"]
            pr_id = str(pr["id"])  # unique PR ID
            is_merged = pr.get("merged", False)

            action_type = "MERGE" if is_merged else "PULL_REQUEST"

            data = {
                "request_id": pr_id,
                "author": author,
                "action": action_type,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": datetime.utcnow().isoformat()
            }
            collection.insert_one(data)


        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/events', methods=['GET'])
def get_events():
    data = collection.find().sort("timestamp", -1).limit(10)
    result = []

    for d in data:
        ts_raw = d["timestamp"]
        if isinstance(ts_raw, str):
            ts = datetime.fromisoformat(ts_raw).replace(tzinfo=pytz.UTC)
        else:
            ts = ts_raw.astimezone(pytz.UTC)

        ts_str = ts.strftime('%d %B %Y - %I:%M %p UTC')

        action = d["action"].lower()
        if action == "push":
            msg = f"{d['author']} pushed to {d['to_branch']} on {ts_str}"
        elif action == "pull_request":
            msg = f"{d['author']} submitted a pull request from {d['from_branch']} to {d['to_branch']} on {ts_str}"
        elif action == "merge":
            msg = f"{d['author']} merged branch {d['from_branch']} to {d['to_branch']} on {ts_str}"

        result.append({"message": msg})

    return jsonify(result)

@app.route('/clear', methods=['POST'])
def clear_events():
    try:
        collection.delete_many({})
        return jsonify({"status": "success", "message": "Events cleared"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
