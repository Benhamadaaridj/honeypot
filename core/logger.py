import datetime

LOG_FILE = "logs/attacks.log"

def log_attack(service, ip, username, password):
    """تسجيل محاولة دخول مشبوهة"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Service: {service}, IP: {ip}, Username: {username}, Password: {password}\n"
    
    print(log_entry.strip())  
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

