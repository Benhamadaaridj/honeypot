import socket
import threading
import paramiko
import time
from core.fake_shell import handle_command

HOST = "0.0.0.0"
PORT = 2222

# Generate SSH host key (honeypot)
host_key = paramiko.RSAKey.generate(2048)


class SSHServer(paramiko.ServerInterface):

    def check_auth_password(self, username, password):
        log_attack("LOGIN", f"{username}:{password}")
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True

    def check_channel_shell_request(self, channel):
        return True


def log_attack(action, detail):
    with open("logs/attacks.log", "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] SSH | {action} | {detail}\n")


def handle_client(client):
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(host_key)
        transport.local_version = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3"

        server = SSHServer()
        transport.start_server(server=server)

        chan = transport.accept(20)
        if chan is None:
            return

        chan.send("Welcome to Ubuntu 22.04 LTS\r\n")
        chan.send("root@ubuntu:~# ")

        buffer = ""

        while True:
            data = chan.recv(1)
            if not data:
                break

            char = data.decode("utf-8", errors="ignore")

            # Enter key
            if char in ("\r", "\n"):
                chan.send("\r\n")
                cmd = buffer.strip()
                buffer = ""

                if cmd:
                    log_attack("CMD", cmd)
                    output = handle_command(cmd)
                    chan.send(output)

                    if cmd in ["exit", "logout"]:
                        break

                chan.send("root@ubuntu:~# ")

            # Backspace
            elif char == "\x7f":
                if buffer:
                    buffer = buffer[:-1]
                    chan.send("\b \b")

            # Normal character (echo)
            else:
                buffer += char
                chan.send(char)

        chan.close()
        transport.close()

    except Exception as e:
        print(f"[!] SSH client error: {e}")


def start_ssh():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(100)

    print("[+] SSH Honeypot listening on port 2222")

    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

