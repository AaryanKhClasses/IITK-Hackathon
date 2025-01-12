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

        # Check for suspension violations
        if username in user_suspended:
            violations.append(f"SUSPENSION_VIOLATION {timestamp.isoformat().replace('+00:00', 'Z')} {username} {ip_address}")
            continue
        # Check for lockout violations
        if username in user_lockout and timestamp < user_lockout[username]:
            violations.append(f"LOCKOUT_VIOLATION {timestamp.isoformat().replace('+00:00', 'Z')} {username} {ip_address}")
            continue

        # Check for blacklist violations
        if ip_address in ip_blacklist and timestamp < ip_blacklist[ip_address]:
            violations.append(f"BLACKLIST_VIOLATION {timestamp.isoformat().replace('+00:00', 'Z')} {username} {ip_address}")
            continue

        if access_result == "FAILURE":
            # Update user failures
            user_failures[username].append(timestamp)
            if len(user_failures[username]) > 10:
                user_failures[username].popleft()
            # Check for user suspension
            if len(user_failures[username]) == 10 and (timestamp - user_failures[username][0]).total_seconds() <= 86400:
                user_suspended.add(username)
                violations.append(f"SUSPENSION_VIOLATION {timestamp.isoformat().replace('+00:00', 'Z')} {username} {ip_address}")
            # Check for user lockout
            if len(user_failures[username]) >= 3 and (timestamp - user_failures[username][-3]).total_seconds() <= 300:
                user_lockout[username] = timestamp + timedelta(seconds=300)
                violations.append(f"LOCKOUT_VIOLATION {timestamp.isoformat().replace('+00:00', 'Z')} {username} {ip_address}")
            # Update IP failures
            ip_failures[ip_address].append(timestamp)
            if len(ip_failures[ip_address]) > 5:
                ip_failures[ip_address].popleft()

            # Check for IP blacklist
            if len(ip_failures[ip_address]) == 5 and (timestamp - ip_failures[ip_address][0]).total_seconds() <= 1200:
                ip_blacklist[ip_address] = timestamp + timedelta(seconds=1800)
                violations.append(f"BLACKLIST_VIOLATION {timestamp.isoformat().replace('+00:00', 'Z')} {username} {ip_address}")

        elif access_result == "SUCCESS":
            if username in user_failures:
                user_failures[username].clear()

    # If no violations, return "NO_VIOLATION"
    if not violations:
        return ["NO_VIOLATION"]

    return violations

# Read number of log entries and the log entries from user
log_entries = []
num_entries = int(input(""))
for _ in range(num_entries):
    entry = input().strip()
    log_entries.append(entry)

violations = process_logs(log_entries)
for violation in violations:
    print(violation)
