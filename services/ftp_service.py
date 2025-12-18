import socket
import threading
import time
import os

HOST = "0.0.0.0"
PORT = 21
LOG_FILE = "logs/attacks.log"


def log_attack(action, detail):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()} | FTP | {action} | {detail}\n")


def handle_client(conn, addr):
    ip = addr[0]
    conn.send(b"220 FTP Server Ready\r\n")

    username = ""
    password = ""

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode(errors="ignore").strip()
            log_attack("COMMAND", f"IP={ip} CMD={command}")

            if command.upper().startswith("USER"):
                username = command.split(" ", 1)[1] if " " in command else ""
                log_attack("USERNAME", f"IP={ip} USER={username}")
                conn.send(b"331 Username OK, need password\r\n")

            elif command.upper().startswith("PASS"):
                password = command.split(" ", 1)[1] if " " in command else ""
                log_attack(
                    "LOGIN_ATTEMPT",
                    f"IP={ip} USER={username} PASS={password}"
                )
                conn.send(b"530 Login incorrect\r\n")

            elif command.upper().startswith(("LIST", "RETR", "STOR")):
                conn.send(b"550 Permission denied\r\n")

            elif command.upper().startswith("QUIT"):
                conn.send(b"221 Goodbye\r\n")
                break

            else:
                conn.send(b"502 Command not implemented\r\n")

    except Exception as e:
        log_attack("ERROR", f"IP={ip} ERR={e}")

    conn.close()


def start_ftp():
    print("[+] FTP Honeypot listening on port 21")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )
        thread.start()

