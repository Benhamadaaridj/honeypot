from flask import Flask, render_template
import json
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "ssh_commands.json"


@app.route("/")
def dashboard():
    rows = []

    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            data = json.load(f)

        for ip, info in data.items():
            sessions = info.get("sessions", [])

            total_commands = sum(len(s.get("commands", [])) for s in sessions)

            # آخر أوامر (آخر session)
            last_commands = []
            if sessions:
                last_session = sessions[-1]
                last_commands = [
                    c["cmd"] for c in last_session.get("commands", [])
                ][-5:]

            rows.append({
                "ip": ip,
                "country": info.get("country", "N/A"),
                "severity": info.get("severity", "LOW"),
                "sessions": len(sessions),
                "commands": total_commands,
                "last_seen": info.get("last_seen", "N/A"),
                "last_commands": last_commands
            })

    return render_template("dashboard.html", rows=rows)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
