# Project-02-healthcare-honeypot
Project Overview
Healthcare environments are increasingly reliant on smart, connected cyber-physical systems,
ranging from patient vitals monitors to smart HVAC infrastructure. Unfortunately, many of these
Internet of Things (IoT) devices lack robust built-in security, making them prime targets for
botnets and ransomware gangs seeking to pivot into the broader hospital network.
The objective of this project is to develop an IoT Deception Honeypot Network. The intern will
architect a virtual environment consisting of simulated, low-interaction vulnerable IoT devices to
proactively deceive attackers, trap them, and analyze their behavioral patterns and exploit
techniques before they can reach actual medical equipment.

Structure of file system.

healthcare-honeypot/
│
├── docker/
│   ├── docker-compose.yml        # Container orchestration
│   ├── cowrie/
│   │   ├── cowrie.cfg            # Honeypot config (ports, banners)
│   │   └── userdb.txt            # Fake credentials for bait
│   └── Dockerfile
│
├── scripts/
│   ├── log_parser.py             # Parses Cowrie JSON logs
│   ├── ioc_extractor.py          # Extracts IPs, hashes, commands
│   └── geolocation.py            # Enriches IPs with geo data
│
├── dashboards/
│   ├── splunk_dashboard.xml      # OR Python Dash/Matplotlib configs
│   └── world_map_viz.py
│
├── reports/
│   └── analytical_report.pdf     # Final week 4 deliverable
│
├── diagrams/
│   └── architecture.png          # Safe architectural diagram
│
└── README.md                     # Setup guide + how to triage logs
