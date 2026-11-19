
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import csv
import json
import threading

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "analytics" / "data"
OUTPUT_DIR = ROOT / "analytics" / "output"

EVENT_FILE = DATA_DIR / "quiz_events.jsonl"
SUMMARY_FILE = OUTPUT_DIR / "quiz_summary.csv"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

lock = threading.Lock()


def save_event(event):
    with lock:
        with EVENT_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")


def load_events():
    events = []

    if not EVENT_FILE.exists():
        return events

    with EVENT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                events.append(json.loads(line))

    return events


def export_summary():
    events = load_events()
    sessions = {}

    for event in events:
        session_id = event["session_id"]

        if session_id not in sessions:
            sessions[session_id] = {
                "started": False,
                "completed": False,
                "score": None,
            }

        if event["event"] == "started":
            sessions[session_id]["started"] = True

        elif event["event"] == "completed":
            sessions[session_id]["started"] = True
            sessions[session_id]["completed"] = True
            sessions[session_id]["score"] = event["percentage"]

    started = sum(
        item["started"] for item in sessions.values()
    )

    completed_scores = [
        item["score"]
        for item in sessions.values()
        if item["completed"] and item["score"] is not None
    ]

    completed = len(completed_scores)

    average = (
        round(sum(completed_scores) / completed, 2)
        if completed
        else 0
    )

    with SUMMARY_FILE.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "participants_started",
            "completed_count",
            "average_score",
        ])

        writer.writerow([
            started,
            completed,
            average,
        ])


class QuizHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )
        self.end_headers()

    def do_GET(self):
        if urlparse(self.path).path != "/quiz-summary":
            self.send_json(404, {"error": "Not found"})
            return

        if not SUMMARY_FILE.exists():
            self.send_json(404, {"error": "CSV not found"})
            return

        content = SUMMARY_FILE.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header(
            "Content-Disposition",
            'attachment; filename="quiz_summary.csv"'
        )
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if urlparse(self.path).path != "/quiz-event":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))

            if length <= 0 or length > 4096:
                self.send_json(400, {"error": "Invalid request size"})
                return

            data = json.loads(self.rfile.read(length))

            if not isinstance(data, dict):
                self.send_json(400, {"error": "Invalid data"})
                return

            session_id = data.get("session_id")
            event_type = data.get("event")

            if (
                not isinstance(session_id, str)
                or not 16 <= len(session_id) <= 64
            ):
                self.send_json(400, {"error": "Invalid session"})
                return

            if event_type not in ("started", "completed"):
                self.send_json(400, {"error": "Invalid event"})
                return

            event = {
                "session_id": session_id,
                "event": event_type,
            }

            if event_type == "completed":
                percentage = data.get("percentage")

                if (
                    isinstance(percentage, bool)
                    or not isinstance(percentage, (int, float))
                    or not 0 <= percentage <= 100
                ):
                    self.send_json(400, {"error": "Invalid score"})
                    return

                event["percentage"] = percentage

            save_event(event)
            export_summary()

            self.send_json(200, {"success": True})

        except (ValueError, TypeError, json.JSONDecodeError):
            self.send_json(400, {"error": "Invalid data"})

        except Exception:
            self.send_json(500, {"error": "Server error"})


if __name__ == "__main__":
    server = ThreadingHTTPServer(
        ("127.0.0.1", 8000),
        QuizHandler
    )

    print("Quiz API running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nQuiz API stopped")
        server.server_close()
