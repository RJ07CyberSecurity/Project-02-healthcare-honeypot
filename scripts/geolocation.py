import json
import os
import time
import requests

IOC_FILE = "reports/iocs.json"
OUTPUT_FILE = "reports/geo_data.json"

def geolocate_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        if data.get("status") == "success":
            return {
                "ip":      ip,
                "country": data.get("country"),
                "city":    data.get("city"),
                "region":  data.get("regionName"),
                "lat":     data.get("lat"),
                "lon":     data.get("lon"),
                "isp":     data.get("isp")
            }
    except requests.RequestException as e:
        print(f"Failed to geolocate {ip}: {e}")
    return {"ip": ip, "country": None, "city": None,
            "lat": None, "lon": None}

def run_geolocation():
    if not os.path.exists(IOC_FILE):
        print(f"IoC file not found: {IOC_FILE}")
        print("Run ioc_extractor.py first.")
        return

    with open(IOC_FILE, "r") as f:
        iocs = json.load(f)

    ips = iocs.get("unique_attacker_ips", [])
    if not ips:
        print("No IPs found in IoC file.")
        return

    print(f"Geolocating {len(ips)} IP addresses...")
    geo_results = []

    for ip in ips:
        print(f"  Looking up {ip}...")
        result = geolocate_ip(ip)
        geo_results.append(result)
        time.sleep(0.5)  # Respect ip-api.com rate limit

    os.makedirs("reports", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(geo_results, f, indent=2)

    print(f"\nGeo data saved to {OUTPUT_FILE}")
    for r in geo_results:
        print(f"  {r['ip']} -> {r.get('city')}, {r.get('country')}")

if __name__ == "__main__":
    run_geolocation()
