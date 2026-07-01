import json
import os
import folium
from collections import Counter

GEO_FILE    = "reports/geo_data.json"
IOC_FILE    = "reports/iocs.json"
OUTPUT_FILE = "reports/attack_map.html"

def build_map():
    if not os.path.exists(GEO_FILE):
        print("Run geolocation.py first.")
        return

    with open(GEO_FILE, "r") as f:
        geo_data = json.load(f)

    # Load commands for popup detail
    commands_by_ip = {}
    if os.path.exists(IOC_FILE):
        with open(IOC_FILE, "r") as f:
            iocs = json.load(f)
        for cmd in iocs.get("commands_executed", []):
            ip = cmd.get("ip")
            if ip not in commands_by_ip:
                commands_by_ip[ip] = []
            commands_by_ip[ip].append(cmd.get("command"))

    # Build the map centred on the world
    attack_map = folium.Map(location=[20, 0], zoom_start=2,
                            tiles="CartoDB positron")

    plotted = 0
    for entry in geo_data:
        lat = entry.get("lat")
        lon = entry.get("lon")
        if not lat or not lon:
            continue

        ip       = entry.get("ip", "unknown")
        city     = entry.get("city", "unknown")
        country  = entry.get("country", "unknown")
        isp      = entry.get("isp", "unknown")
        cmds     = commands_by_ip.get(ip, [])
        cmd_html = "<br>".join(cmds[:5]) or "none recorded"

        popup_html = f"""
        <b>Attacker IP:</b> {ip}<br>
        <b>Location:</b> {city}, {country}<br>
        <b>ISP:</b> {isp}<br>
        <b>Commands run:</b><br>{cmd_html}
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=f"{ip} — {country}",
            icon=folium.Icon(color="red", icon="exclamation-sign")
        ).add_to(attack_map)
        plotted += 1

    os.makedirs("reports", exist_ok=True)
    attack_map.save(OUTPUT_FILE)
    print(f"Map saved to {OUTPUT_FILE} ({plotted} attackers plotted)")
    print("Open it in your browser: xdg-open reports/attack_map.html")

if __name__ == "__main__":
    build_map()
