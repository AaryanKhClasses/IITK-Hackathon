import pandas as pd

# # Load the CSV file
file_path = input()
data = pd.read_csv(file_path)

patterns = ["'", "--", ";", "SELECT", "UNION", "INSERT", "UPDATE", "DELETE"]
pattern = '|'.join(patterns)
attempts = data[data["Info"].str.contains(pattern, case=False, na=False)]

if not attempts.empty:
    source_ip = attempts["Source"].iloc[0]
    print(f"1A: {source_ip}")
else:
    print("1A: NULL")

total_attempts = len(attempts)
print(f"2A: {total_attempts}")

if not attempts.empty:
    first_payload = attempts.sort_values(by="Time").iloc[0]["Info"]
    first_payload = first_payload.split(" ")[1]
    print(f"3A: {first_payload}")
else:
    print("3A: NULL")

if not attempts.empty:
    last_payload = attempts.sort_values(by="Time").iloc[-1]["Info"]
    last_payload = last_payload.split(" ")[1]
    print(f"4A: {last_payload}")
else:
    print("4A: NULL")

colons = attempts[attempts["Info"].str.contains(":", case=False, na=False)]
total_colons = len(colons)
print(f"5A: {total_colons}")
