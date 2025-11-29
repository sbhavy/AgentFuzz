def mutate(data: str) -> str:
    """
    Aggressively mutates a JSON string to find vulnerabilities.
    """
    if not data:
        return '[]'

    mutated_data = list(data)
    length = len(mutated_data)

    # Extreme length changes
    if random.random() < 0.1:
        # Truncate
        if length > 10:
            mutated_data = mutated_data[:random.randint(1, length // 2)]
        # Extend with random characters or specific JSON patterns
        else:
            extend_len = random.randint(10, 100)
            extension = ''.join(random.choice('{}[]:,0123456789"\'\\') for _ in range(extend_len))
            mutated_data.extend(list(extension))
            length = len(mutated_data)

    # Character replacements and insertions
    num_mutations = int(length * random.uniform(0.1, 0.5))
    for _ in range(num_mutations):
        if not mutated_data:
            break
        mutation_type = random.random()
        idx = random.randint(0, len(mutated_data) - 1)

        if mutation_type < 0.3:  # Replace character
            mutated_data[idx] = random.choice('{}[]:,"\'\\0123456789 \t\n\r\b\f\v')
        elif mutation_type < 0.6:  # Insert character
            mutated_data.insert(idx, random.choice('{}[]:,"\'\\0123456789 \t\n\r\b\f\v'))
            length += 1
        elif mutation_type < 0.8:  # Delete character
            del mutated_data[idx]
            length -= 1
        else:  # Duplicate character
            mutated_data.insert(idx, mutated_data[idx])
            length += 1

    # Specific JSON-related mutations
    json_chars = ['{', '}', '[', ']', ':', ',', '"', "'"]
    special_chars = ['\\', '\'', '"', '\b', '\f', '\n', '\r', '\t', '\v', '\x00', '\xff']
    valid_escapes = ['\\', '/', '"', 'b', 'f', 'n', 'r', 't', 'u']

    mutated_str = "".join(mutated_data)
    length = len(mutated_str)

    # Corrupting string escapes
    if length > 0:
        for _ in range(random.randint(0, length // 10)):
            idx = random.randint(0, length - 1)
            if mutated_str[idx] == '\\':
                if random.random() < 0.7:
                    # Replace with invalid escape
                    mutated_str = mutated_str[:idx] + random.choice('abcdefgXYZ01') + mutated_str[idx+1:]
                else:
                    # Insert after escape
                    mutated_str = mutated_str[:idx+1] + random.choice(special_chars) + mutated_str[idx+1:]
            elif mutated_str[idx] in '"\'':
                if random.random() < 0.1:
                    mutated_str = mutated_str[:idx] + '\\' + mutated_str[idx] + mutated_str[idx+1:]
                elif random.random() < 0.2:
                    mutated_str = mutated_str[:idx] + random.choice(special_chars) + mutated_str[idx+1:]


    mutated_data = list(mutated_str)
    length = len(mutated_data)

    # Injecting control characters or invalid unicode
    if length > 0:
        for _ in range(random.randint(0, length // 20)):
            idx = random.randint(0, length - 1)
            if mutated_data[idx] == '\\' and idx + 1 < length and mutated_data[idx+1] == 'u':
                # Corrupt unicode escape
                if random.random() < 0.5:
                    mutated_data.insert(idx + 2, random.choice('XYZ'))
                else:
                    mutated_data.pop(idx + 1)
                    mutated_data.pop(idx)
                    mutated_data.insert(idx, random.choice(special_chars))

            if mutated_data[idx] == '"':
                 if random.random() < 0.05:
                     mutated_data.insert(idx + 1, '\\')
                     mutated_data.insert(idx + 2, random.choice(string.printable.replace('"', '').replace('\\', '')))
                 elif random.random() < 0.02:
                     mutated_data.insert(idx + 1, random.choice([chr(i) for i in range(32)]))


    mutated_str = "".join(mutated_data)
    length = len(mutated_str)

    # Number fuzzing
    if length > 0:
        for _ in range(random.randint(0, length // 15)):
            idx = random.randint(0, length - 1)
            if mutated_str[idx].isdigit():
                if random.random() < 0.1:
                    mutated_str = mutated_str[:idx] + random.choice('eE.+-') + mutated_str[idx:]
                elif random.random() < 0.2:
                    mutated_str = mutated_str[:idx] + random.choice(string.ascii_letters) + mutated_str[idx+1:]
                elif random.random() < 0.3:
                    mutated_str = mutated_str[:idx] + ' ' + mutated_str[idx:]

    mutated_str = "".join(mutated_data)
    length = len(mutated_str)


    # Add more extreme cases
    if random.random() < 0.05:
        mutated_str = mutated_str * random.randint(2, 5)

    if random.random() < 0.05 and length > 1:
        # Swap parts
        idx1 = random.randint(0, length // 2)
        idx2 = random.randint(length // 2, length - 1)
        part1 = mutated_str[idx1:idx1+5]
        part2 = mutated_str[idx2:idx2+5]
        mutated_str = mutated_str[:idx1] + part2 + mutated_str[idx1+5:]
        mutated_str = mutated_str[:idx2] + part1 + mutated_str[idx2+5:]


    # Ensure it's somewhat JSON-like if it became too broken
    if not mutated_str or not (mutated_str.startswith('{') or mutated_str.startswith('[')):
        if random.random() < 0.5:
            return '{}'
        else:
            return '[]'

    return mutated_str