def ask_id(prompt):
    while True:
        value = input(f"{prompt} (press Enter to cancel): ").strip()
        if value == "":
            return None
        if not value.isdigit():
            print("ID must be a number.")
            continue
        return int(value)