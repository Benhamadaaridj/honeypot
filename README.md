# Honeypot Project

## Overview
This project implements a multi-service honeypot that simulates vulnerable SSH, FTP, and HTTP services. Its primary goal is to attract and monitor malicious actors, safely record their activities, and analyze common attack techniques such as brute-force authentication, SQL injection, and path traversal, without exposing any real system.

The honeypot allows direct observation of attacker behavior through a simulated shell environment, enabling the study of post-exploitation actions after successful access attempts. Additionally, it emulates a vulnerable vsFTPd 2.4.5 FTP service, deliberately deceiving attackers and encouraging exploitation attempts while securely capturing all interaction data for research and educational analysis.

---

## Requirements
- Linux system  
- Python 3  

---

## Installation

Clone the repository:
```bash
git clone https://github.com/honeypot11012026/honeypot-project.git
cd honeypot-project
```

Install required dependencies:
```bash
pip install flask paramiko
```
---

## Running the Honeypot

Start the honeypot (requires root privileges):
```bash
sudo python3 main.py
```

If everything works correctly, you should see:
```bash
╔══════════════════════════════════════════════╗
║              H O N E Y P O T                 ║
╠══════════════════════════════════════════════╣
║  SSH        → port 2222                      ║
║  FTP        → port 21                        ║
║  HTTP       → port 80                        ║
║  Dashboard  → port 5000                     ║
╚══════════════════════════════════════════════╝
[2026-01-06 10:39:27,925] INFO: [+] Starting SSH service
[2026-01-06 10:39:27,926] INFO: [+] SSH Honeypot listening on port 2222
[2026-01-06 10:39:27,926] INFO: [+] Starting FTP service
[+] FTP service listening on port 21
[2026-01-06 10:39:27,928] INFO: [+] Starting HTTP service
[2026-01-06 10:39:27,928] INFO: HTTP service running on port 80
[2026-01-06 10:39:27,930] INFO: [+] Starting DASHBOARD service
[2026-01-06 10:39:27,931] INFO: Dashboard running on port 5000
[2026-01-06 10:39:27,930] INFO: [*] All services started successfully


```
---

visit :
```bash
http://127.0.0.1:5000
```

To view dashboaed on a browser

---

## Testing the Services
### 1) SSH Honeypot

Connect to the fake SSH service:
```bash
ssh root@127.0.0.1 -p 2222
```

Enter any password

Try common commands:
```bash
ls
pwd
id
sudo -l
```
#### All commands are simulated and logged.

---

### 2) HTTP Honeypot
### 2.1 Fake Admin Login

- Accepts any username and password

- Redirects to a fake admin dashboard

- Used to collect credentials and observe attacker behavior

Test in a browser:
```bash

http://127.0.0.1
http://127.0.0.1/admin
http://127.0.0.1/admin/dashboard
```
---
### 2.2 Brute Force Simulation

- Simulates a vulnerable login endpoint

- Always returns invalid credentials

- Logs every attempt
```bash

http://127.0.0.1/bruteforce
```
---
### 2.3 Path Traversal / LFI Simulation

- Simulates a Local File Inclusion vulnerability

- Returns a fake /etc/passwd file

- Used to detect directory traversal attempts
```bash

http://127.0.0.1/download?file=../../etc/passwd
```
---
### 2.4 SQL Injection Honeypot

- Detects common SQL injection patterns

- Returns realistic SQL error messages

- No real database is used
```bash
http://127.0.0.1/sql_login
```
Example test payloads (use in the username field):
```text
' OR 1=1 --
' OR '1'='1
admin' --
admin' #
```
---

### 3) FTP Honeypot

Launch Metasploit:
```bash
msfconsole -q
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOSTS 127.0.0.1
nc 127.0.0.1 6200
```

Try commands:
```bash
ls
pwd
```

#### All commands are simulated and logged.

---

> ⚠️ **DISCLAIMER**
>  
> This project is for **educational and research purposes only**.  
> It is designed to be used **strictly within a local or LAN environment** and is **not exposed to the public internet**.  
> Do **not** deploy this project on public networks or use it for illegal activities.



