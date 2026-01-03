from datetime import datetime

class Session:
    def __init__(self, ip):
        self.ip = ip
        self.start = datetime.utcnow().isoformat()
        self.last_seen = self.start
        self.commands = []

    def add_command(self, cmd):
        self.commands.append({
            "cmd": cmd,
            "time": datetime.utcnow().isoformat()
        })
        self.last_seen = datetime.utcnow().isoformat()
