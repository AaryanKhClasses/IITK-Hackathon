from datetime import datetime

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
if __name__ == "__main__":
    tc = int(input())
    for _ in range(0, tc):
        logs.append(input())
    for log in logs:
      user = log[1]
      if user not in users:
          users[user] = User(user)
      if users[user].isSuspended(log):
          print(f"SUSPENSION_VIOLATION {log[0]} {log[1]} {log[2]}")
      elif ipads.isBlacklisted(log):
          printf(f"BLACKLISTED_VIOLATION {log[0]} {log[1]} {log[2]}")
      elif users[user].isLockedout(log):
          print(f"LOCKOUT_VIOLATION {log[0]} {log[1]} {log[2]}")
