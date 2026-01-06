# Honeypot Project

## Overview
This project implements a **multi-service honeypot** that simulates vulnerable **HTTP, SSH, and FTP** services.  
The goal is to attract attackers, log malicious behavior, and study common attack techniques such as **brute force**, **SQL injection**, and **path traversal**, without exposing a real system.

---

## Requirements
- Linux system  
- Python 3  

---

## Installation



Clone the repository:

git clone https://github.com/ayazrrouni/honey.git
cd honeypot

Install required dependencies:
```bash
git clone https://github.com/ayazrrouni/honey.git
cd honey
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
[+] HTTP Honeypot listening on port 80
[+] SSH Honeypot listening on port 2222
```
---
## Open Dahsboard to view logs:
```bash

python3 -m dashboard.app
```
visit :
```bash
http://127.0.0.1:5000
```

To view dashboaed on a search engin

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

All commands are simulated and logged.
---

### 2) HTTP Honeypot
- Fake Admin Login

- Accepts any username and password

- Redirects to a fake admin dashboard

- Used to collect credentials and observe attacker behavior

Test in a browser:
```bash

http://127.0.0.1
http://127.0.0.1/admin
http://127.0.0.1/admin/dashboard
```

### 3)Brute Force Simulation

- Simulates a vulnerable login endpoint

- Always returns invalid credentials

- Logs every attempt
```bash

http://127.0.0.1/bruteforce
```

### 4)Path Traversal / LFI Simulation

- Simulates a Local File Inclusion vulnerability

- Returns a fake /etc/passwd file

- Used to detect directory traversal attempts
```bash

http://127.0.0.1/download?file=../../etc/passwd
```

### 5)SQL Injection Honeypot

- Detects common SQL injection patterns

- Returns realistic SQL error messages

- No real database is used
```bash

http://127.0.0.1/sql_login
```


### 4) FTP Honeypot

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
## Disclaimer

> This project is for educational and research purposes only.
> Do not deploy it on public networks or use it for illegal activities.



