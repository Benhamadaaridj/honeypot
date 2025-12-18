import time

def handle_command(cmd):
    time.sleep(0.3)
    cmd = " ".join(cmd.split())

    if cmd == "ls":
        return "bin  etc  home  var\r\n"
    elif cmd == "pwd":
        return "/root\r\n"
    elif cmd.startswith("cat"):
        if "/etc/passwd" in cmd:
            return open("fake_fs/etc_passwd.txt").read().replace("\n", "\r\n") + "\r\n"
        elif "notes" in cmd:
            return open("fake_fs/root_notes.txt").read().replace("\n", "\r\n") + "\r\n"
        elif "auth.log" in cmd:
            return open("fake_fs/var_log_auth.txt").read().replace("\n", "\r\n") + "\r\n"
        else:
            return "cat: file not found\r\n"
    elif cmd == "uname -a":
        return "Linux ubuntu 5.15.0-84-generic x86_64\r\n"
    elif cmd == "id":
        return "uid=0(root) gid=0(root) groups=0(root)\r\n"
    elif cmd == "sudo -l":
        return "User root may run the following commands on this host:\r\n    (ALL) ALL\r\n"
    elif cmd in ["exit", "logout"]:
        return "logout\r\n"
    else:
        return f"{cmd}: command not found\r\n"

