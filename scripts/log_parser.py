import json
import os
from datetime import datetime

LOG_FILE = "reports/logs/cowrie.json"

def parse_logs():
    if not os.path.exists(LOG_FILE):
        print(f"No log file found at {LOG_FILE}")
        print("Make sure Cowrie is running and has received connections.")
        return []

    events = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    print(f"Total events found: {len(events)}")
    print("-" * 50)

    for e in events:
        timestamp = e.get("timestamp", "unknown time")
        event_id  = e.get("eventid", "unknown event")
        src_ip    = e.get("src_ip", "unknown IP")
        msg       = e.get("message", "")
        print(f"[{timestamp}] {event_id} | IP: {src_ip} | {msg}")

    return events

if __name__ == "__main__":
    parse_logs()
