from datetime import datetime

<<<<<<< HEAD
def time_diff(time1, time2):
  form = "%Y-%m-%dT%H:%M:%SZ"
  timeStart = datetime.strptime(time1, form)
  timeEnd = datetime.strptime(time2, form)
  return (timeEnd-timeStart).total_seconds()

class IpAddresses:
    def isBlacklisted(self, log):
        return False

class User:
    username = ""
    lockouts = 0
    suspensions = 0

    lockedout = False
    lastLockout = 0
    lastLockoutTime = ""
    lockoutStartTime = ""

    suspended = False
    lastSuspension = 0
    lastSuspensionTime = ""
    suspendStartTime = ""

    def __init__(self, user):
        self.username = user

    def isSuspended(self, log):
        time = log[0]
        if (not self.suspended and log[3]=="FAILURE"):
           self.suspensions += 1
           if (self.suspensions-self.lastSuspension>=5):
            if (not self.lastSuspensionTime=="" and time_diff(self.lastSuspensionTime, time)<=86400):
               self.suspended = True
               self.suspensionStartTime = time
            else:
               self.lastSuspension = self.suspensions
               self.lastSuspensionTime = time
        if (self.suspended and time_diff(self.suspendStartTime, time)>1800):
            self.suspended = False
        return self.suspended

    def isLockedout(self, log):
        time = log[0]
        if (not self.lockedout and log[3]=="FAILURE"):
            self.lockouts += 1
            if (self.lockouts-self.lastLockout>=5):
                if (not self.lastLockoutTime=="" and time_diff(self.lastLockoutTime, time)<=300):
                    self.lockedout = True
                    self.lockoutStartTime = time
                else:
                    self.lastLockout = self.lockouts
                    self.lastLockoutTime = time
        if (self.lockedout and time_diff(self.lockoutStartTime, time)>300):
            self.locked = False
        return self.lockedout

users = {}
ipads = IpAddresses()
logs = []
=======
def td(tsE, tsS, secs):
    template = "%Y-%m-%dT%H:%M:%SZ"
    timeStart = datetime.strptime(tsS, template)
    timeEnd = datetime.strptime(tsE, template)
    return (timeEnd-timeStart).total_seconds()>secs

users = {}
addresses = {}
logs = []
violation = 0
>>>>>>> eashan
if __name__ == "__main__":
    tc = int(input())
    for _ in range(0, tc):
        logs.append(input())
    for log in logs:
<<<<<<< HEAD
      user = log[1]
      if user not in users:
          users[user] = User(user)
      if users[user].isSuspended(log):
          print(f"SUSPENSION_VIOLATION {log[0]} {log[1]} {log[2]}")
      elif ipads.isBlacklisted(log):
          printf(f"BLACKLISTED_VIOLATION {log[0]} {log[1]} {log[2]}")
      elif users[user].isLockedout(log):
          print(f"LOCKOUT_VIOLATION {log[0]} {log[1]} {log[2]}")
=======
        ts, us, ip, va = log.split(" ")
        if us not in users:
            users[us] = [0, [0, ts], [0, ts]]
        if ip not in addresses:
            addresses[ip] = [0, [0, ts], ts]
        if va == "FAILURE":
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
>>>>>>> eashan
