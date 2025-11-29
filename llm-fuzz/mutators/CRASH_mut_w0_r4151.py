def mutate(data: str) -> str:
    mutated_data = list(data)
    n = len(mutated_data)

    # Randomly decide mutation operations
    operations = [
        "delete", "insert", "replace", "swap", "duplicate"
    ]
    op = random.choice(operations)

    if op == "delete" and n > 0:
        idx = random.randrange(n)
        mutated_data.pop(idx)
    elif op == "insert":
        idx = random.randrange(n + 1)
        # Insert random printable ASCII characters
        insert_char = random.choice(string.printable)
        mutated_data.insert(idx, insert_char)
    elif op == "replace" and n > 0:
        idx = random.randrange(n)
        # Replace with random printable ASCII characters
        replace_char = random.choice(string.printable)
        mutated_data[idx] = replace_char
    elif op == "swap" and n > 1:
        idx1 = random.randrange(n)
        idx2 = random.randrange(n)
        mutated_data[idx1], mutated_data[idx2] = mutated_data[idx2], mutated_data[idx1]
    elif op == "duplicate" and n > 0:
        idx = random.randrange(n)
        mutated_data.insert(idx, mutated_data[idx])

    # Apply specific JSON-like mutations with a certain probability
    if random.random() < 0.3 and n > 0: # Malformed brackets/braces
        idx = random.randrange(n)
        if mutated_data[idx] == '{':
            mutated_data[idx] = '['
        elif mutated_data[idx] == '[':
            mutated_data[idx] = '{'
        elif mutated_data[idx] == '}':
            mutated_data[idx] = ']'
        elif mutated_data[idx] == ']':
            mutated_data[idx] = '}'

    if random.random() < 0.2 and n > 0: # Unescaped quotes
        idx = random.randrange(n)
        if mutated_data[idx] == '"':
            mutated_data[idx] = "'"

    if random.random() < 0.1: # Insert control characters
        idx = random.randrange(n + 1)
        control_char = random.choice(['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x09', '\x0a', '\x0b', '\x0c', '\x0d', '\x0e', '\x0f'])
        mutated_data.insert(idx, control_char)

    if random.random() < 0.1 and n > 0: # Corrupt numbers
        idx = random.randrange(n)
        if mutated_data[idx].isdigit():
            mutated_data[idx] = random.choice('abcdefg')
        elif mutated_data[idx] in ['.', 'e', '+', '-']:
            mutated_data[idx] = random.choice(string.digits)

    return "".join(mutated_data)