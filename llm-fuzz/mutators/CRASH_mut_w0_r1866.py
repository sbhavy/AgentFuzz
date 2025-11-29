def mutate(data: str) -> str:
    """
    Aggressively mutates a JSON string to potentially crash a parser.
    """
    mutated_data = list(data)
    n = len(mutated_data)

    # Randomly choose a mutation strategy
    mutation_type = random.randint(0, 9)

    if mutation_type == 0 and n > 0: # Character deletion
        idx = random.randint(0, n - 1)
        mutated_data.pop(idx)
    elif mutation_type == 1 and n > 0: # Character replacement
        idx = random.randint(0, n - 1)
        mutated_data[idx] = random.choice(string.printable)
    elif mutation_type == 2: # Character insertion
        idx = random.randint(0, n)
        mutated_data.insert(idx, random.choice(string.printable))
    elif mutation_type == 3: # String duplication
        if n > 0:
            idx = random.randint(0, n - 1)
            char_to_dup = mutated_data[idx]
            mutated_data.insert(idx, char_to_dup)
    elif mutation_type == 4: # String reversal (small chunks)
        if n > 10:
            start = random.randint(0, n - 10)
            end = min(start + random.randint(5, 10), n)
            chunk = mutated_data[start:end]
            chunk.reverse()
            mutated_data[start:end] = chunk
    elif mutation_type == 5: # Whitespace manipulation
        whitespace_chars = [' ', '\t', '\n', '\r']
        if n > 0:
            idx = random.randint(0, n - 1)
            if mutated_data[idx] in whitespace_chars:
                mutated_data.insert(idx, random.choice(whitespace_chars))
            else:
                mutated_data.insert(idx, random.choice(whitespace_chars))
    elif mutation_type == 6: # Bracket/brace manipulation
        bracket_chars = ['[', ']', '{', '}']
        if n > 0:
            idx = random.randint(0, n - 1)
            if mutated_data[idx] in bracket_chars:
                mutated_data[idx] = random.choice(bracket_chars)
    elif mutation_type == 7: # Number modification
        numeric_indices = [i for i, char in enumerate(mutated_data) if char.isdigit()]
        if numeric_indices:
            idx = random.choice(numeric_indices)
            mutated_data[idx] = random.choice(string.digits + 'eE.+-')
    elif mutation_type == 8: # String termination/escape issues
        if n > 0:
            idx = random.randint(0, n - 1)
            if mutated_data[idx] == '"':
                mutated_data.insert(idx + 1, random.choice(['\\', '\'', '\0', '\n', '\r', '"']))
            elif mutated_data[idx] == '\\':
                 mutated_data.insert(idx + 1, random.choice(['\\', '"', "'", '/', 'b', 'f', 'n', 'r', 't', 'u']))
    elif mutation_type == 9: # Overlapping or missing delimiters
        if n > 5:
            idx = random.randint(0, n - 1)
            if mutated_data[idx] in [':', ',', '[', '{', ']', '}']:
                 mutated_data.insert(idx, mutated_data[idx])


    # Ensure result is not empty and try to maintain some semblance of structure
    result = "".join(mutated_data)
    if not result:
        return "{}"
    return result