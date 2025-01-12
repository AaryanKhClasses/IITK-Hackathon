def main():
    U = int(input())
    users = []
    permissions_db = {}
    KEYWORDS = ['CREATE_DIR', 'CREATE_FILE', 'READ_FILE', 'WRITE_FILE', 'DELETE', 'LIST_DIR']

    for _ in range(U):
        users.append(input())

    def parse_command(command):
        parts = command.split(" ", 3)
        command_type = parts[0]
        issuer = parts[1]
        target = parts[2]
        permissions_dict = {}

        if command_type in {"CREATE_DIR", "CREATE_FILE"} and len(parts) > 3:
            user_permissions = parts[3]
            for user_permission in user_permissions.split(";"):
                user, perms = user_permission.split(":")
                permissions_dict[user] = perms.split(",")
        return command_type, issuer, target, permissions_dict

    def execute_command(command):
        command_type, issuer, target, permissions = parse_command(command)
        if command_type in {"CREATE_DIR", "CREATE_FILE"}:
            permissions_db[target] = permissions
            return "SUCCESS"
        elif command_type in {"READ_FILE", "WRITE_FILE", "DELETE", "LIST_DIR"}:
            if target not in permissions_db:
                return "DENY"
            required_permission = {
                "READ_FILE": "R",
                "WRITE_FILE": "W",
                "DELETE": "W",
                "LIST_DIR": "X"
            }[command_type]

            if issuer in permissions_db[target] and required_permission in permissions_db[target][issuer]:
                return "SUCCESS"
            else:
                return "DENY"

    num_commands = int(input())
    commands = [input() for _ in range(num_commands)]

    for command in commands:
        result = execute_command(command)
        print(result)

if __name__ == "__main__":
    main()
