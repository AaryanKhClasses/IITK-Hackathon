from datetime import datetime, timedelta
from collections import defaultdict, deque

def parse_log_entry(entry):
    timestamp, username, ip_address, access_result = entry.split()
    timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return timestamp, username, ip_address, access_result

def process_logs(log_entries):
    user_failures = defaultdict(deque)
    ip_failures = defaultdict(deque)
    user_lockout = {}
    ip_blacklist = {}
    user_suspended = set()
    violations = []

    for entry in log_entries:
        timestamp, username, ip_address, access_result = parse_log_entry(entry)

        if username in user_suspended:
            violations.append(f"SUSPENSION_VIOLATION {timestamp.isoformat()} {username} {ip_address}")
            continue
        
        if username in user_lockout and timestamp < user_lockout[username]:
            violations.append(f"LOCKOUT_VIOLATION {timestamp.isoformat()} {username} {ip_address}")
            continue

        if ip_address in ip_blacklist and timestamp < ip_blacklist[ip_address]:
            violations.append(f"BLACKLIST_VIOLATION {timestamp.isoformat()} {username} {ip_address}")
            continue

        if access_result == "FAILURE":
            user_failures[username].append(timestamp)
            ip_failures[ip_address].append(timestamp)

            if len(user_failures[username]) >= 3 and (timestamp - user_failures[username][-3]) <= timedelta(minutes=5):
                user_lockout[username] = timestamp + timedelta(minutes=5)

            while ip_failures[ip_address] and (timestamp - ip_failures[ip_address][0]) > timedelta(minutes=20):
                ip_failures[ip_address].popleft()
            if len(ip_failures[ip_address]) >= 5:
                ip_blacklist[ip_address] = timestamp + timedelta(minutes=30)

            while user_failures[username] and (timestamp - user_failures[username][0]) > timedelta(hours=24):
                user_failures[username].popleft()
            if len(user_failures[username]) >= 10:
                user_suspended.add(username)

        elif access_result == "SUCCESS":
            user_failures[username].clear()

    if not violations:
        print("NO_VIOLATION")
    else:
        for violation in violations:
            print(violation)

def main():
    print("Enter log entries (press Enter twice to finish):")
    log_entries = []
    
    first_line = input().strip()
    if not first_line.isdigit():
        print("Invalid input: The first line must be a number indicating the number of cases.")
        return
    
    num_cases = int(first_line)
    
    for _ in range(num_cases):
        line = input().strip()
        if line == "":
            print("Invalid input: Not enough log entries provided.")
            return
        log_entries.append(line)
    
    extra_line = input().strip()
    if extra_line != "":
        print("Invalid input: Extra log entries provided.")
        return
    
    process_logs(log_entries)
    
if __name__ == "__main__":
    main()
