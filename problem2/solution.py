root = ("/", {}, [])
users = []

def create(alp):
    u, p = alp.split(":")
    pem = ""
    if ('R' in p):
        pem.append("1")
    if ('W' in p)
def executable(cmd):
    global root, users
    cd, us, tr, pm = cmd.split(" ")
    usp = map(create, pm.split(";"))
if __name__ == "__main__":
  for _ in range(0, int(input())):
      user = input()
      users.append(user)
      root[1][user] = "111"
  for _ in range(0, int(input())):
      if (executable(input())):
          print("SUCCESS")
      else:
          print("DENY")
