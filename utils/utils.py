def yes_or_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'no']:
            return response
        else:
            print("    [!] Please enter 'yes' or 'no'.")
