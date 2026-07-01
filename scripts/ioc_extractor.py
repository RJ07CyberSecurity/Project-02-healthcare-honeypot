import json
import os

LOG_FILE = "reports/logs/cowrie.json"
OUTPUT_FILE = "reports/iocs.json"

def extract_iocs():
    if not os.path.exists(LOG_FILE):
        print(f"Log file not found: {LOG_FILE}")
        return

    ips      = set()
    commands = []
    hashes   = []
    sessions = {}

    with open(LOG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Collect attacker IPs
            if e.get("src_ip"):
                ips.add(e["src_ip"])

            # Collect commands typed by attacker
            if e.get("eventid") == "cowrie.command.input":
                commands.append({
                    "ip":      e.get("src_ip"),
                    "command": e.get("input"),
                    "time":    e.get("timestamp")
                })

            # Collect uploaded malware file hashes
            if e.get("eventid") == "cowrie.session.file_download":
                hashes.append({
                    "ip":       e.get("src_ip"),
                    "filename": e.get("filename"),
                    "shasum":   e.get("shasum"),
                    "url":      e.get("url")
                })

            # Track session duration
            session = e.get("session")
            if session:
                if session not in sessions:
                    sessions[session] = {"ip": e.get("src_ip"), "events": 0}
                sessions[session]["events"] += 1

    iocs = {
        "unique_attacker_ips": list(ips),
        "commands_executed":   commands,
        "malware_hashes":      hashes,
        "sessions":            sessions,
        "summary": {
            "total_ips":      len(ips),
            "total_commands": len(commands),
            "total_files":    len(hashes),
            "total_sessions": len(sessions)
        }
    }

    os.makedirs("reports", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(iocs, f, indent=2)

    print(f"IoCs saved to {OUTPUT_FILE}")
    print(f"Unique IPs:       {len(ips)}")
    print(f"Commands logged:  {len(commands)}")
    print(f"Files uploaded:   {len(hashes)}")
    print(f"Sessions tracked: {len(sessions)}")

if __name__ == "__main__":
    extract_iocs()
