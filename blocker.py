import re
from flask import request
from datetime import datetime, timedelta

blocked_ips = {}
block_duration = timedelta(minutes=10)

def is_sql_injection(payload):
    pattern = r"(union|select|insert|drop|--|;|'|\"|xp_)"
    return bool(re.search(pattern, payload, re.IGNORECASE))

def log_intrusion(ip, payload):
    with open("logs/intrusions.log", "a") as log_file:
        log_file.write(f"{datetime.now()} - {ip} - Suspicious: {payload}\n")

def is_blocked(ip):
    if ip in blocked_ips:
        if datetime.now() < blocked_ips[ip]:
            return True
        else:
            del blocked_ips[ip]
    return False

def check_request():
    ip = request.remote_addr
    if is_blocked(ip):
        return "Your IP is temporarily blocked.", 403

    for key, value in request.args.items():
        if is_sql_injection(value):
            log_intrusion(ip, value)
            blocked_ips[ip] = datetime.now() + block_duration
            return "Potential intrusion detected. IP blocked.", 403

    return None
