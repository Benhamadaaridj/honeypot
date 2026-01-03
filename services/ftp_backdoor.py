import socket
import threading
import uuid
from core.fake_shell import handle_command, FakeShell
from core.logger import start_session, log_command, end_session


def handle_shell(conn, addr):
    ip = addr[0]
    session_id = str(uuid.uuid4())

    start_session(ip, session_id, service="ftp")

    shell = FakeShell("root")
    conn.send(b"uid=0(root)\n")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            cmd = data.decode(errors="ignore").strip()
            log_command(ip, session_id, cmd)

            output, _ = handle_command(cmd, {"shell": shell})
            if output:
                conn.send(output.encode())

    finally:
        end_session(ip, session_id)
        conn.close()


def start_backdoor_listener():
    sock = socket.socket()
    sock.bind(("0.0.0.0", 6200))
    sock.listen(5)

    print("[+] FTP backdoor listening on 6200")

    while True:
        c, a = sock.accept()
        threading.Thread(target=handle_shell, args=(c, a), daemon=True).start()
