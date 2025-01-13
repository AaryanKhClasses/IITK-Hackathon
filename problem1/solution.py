from datetime import datetime

def td(tsE, tsS, secs):
    template = "%Y-%m-%dT%H:%M:%SZ"
    timeStart = datetime.strptime(tsS, template)
    timeEnd = datetime.strptime(tsE, template)
    return (timeEnd-timeStart).total_seconds()>secs

users = {}
addresses = {}
logs = []
violation = 0
if __name__ == "__main__":
    tc = int(input())
    for _ in range(0, tc):
        logs.append(input())
    for log in logs:
        ts, us, ip, va = log.split(" ")
        if us not in users:
            users[us] = [0, [0, ts], [0, ts]]
        if ip not in addresses:
            addresses[ip] = [0, [0, ts], ts]
        
        if (users[us][1][0]) < 10 and (td(ts, users[us][1][1], 86400)):
            users[us][1][1] = ts
            users[us][1][0] = 0
        if (td(ts, addresses[ip][1][1], 1200) or (addresses[ip][1][0]==5 and td(ts, addresses[ip][2], 1800))):
            addresses[ip][1][0] = 0
        if (users[us][2][0]==3 and td(ts, users[us][2][1], 300)):
            users[us][2][0] = 0

        if users[us][1][0]>=10:
            print(f"SUSPENSION_VIOLATION {ts} {us} {ip}")
            violation += 1
            continue
        if addresses[ip][1][0]>=5:
            print(f"BLACKLIST_VIOLATION {ts} {us} {ip}")
            violation += 1
            continue
        if users[us][2][0]>=3:
            print(f"LOCKOUT_VIOLATION {ts} {us} {ip}")
            violation += 1
            continue
        if va == "FAILURE":
            users[us][0]        += 1
            users[us][1][0]     += 1
            users[us][2][0]     += 1
            addresses[ip][0]    += 1
            addresses[ip][1][0] += 1
            if (users[us][2][0]==3):
                users[us][2][1] = ts
            if (addresses[ip][1][0]==5):
                addresses[ip][2] = ts
        else:
            users[us][2][0] = 0
    if violation==0:
        print("NO_VIOLATION")
