import json, os

LOG = "reports/logs/cowrie.json"
counts = {}
bf = {}

with open(LOG) as f:
    for line in f:
        try:
            e = json.loads(line.strip())
            eid = e.get("eventid","unknown")
            counts[eid] = counts.get(eid,0) + 1
            if "login" in eid:
                ip = e.get("src_ip","?")
                bf[ip] = bf.get(ip,0) + 1
        except: pass

print("=== Event summary ===")
for k,v in sorted(counts.items()):
    print(f"  {k}: {v}")
print(f"\n=== Brute-force IPs ===")
for ip,n in sorted(bf.items(),key=lambda x:-x[1]):
    print(f"  {ip}: {n} attempts")
