def mutate(data: str) -> str:
    s = list(data)
    n = len(s)
    
    # Aggressive mutations
    for _ in range(random.randint(1, n // 5 + 1)):
        op = random.randint(0, 5)
        
        if op == 0 and n > 0: # Delete a character
            i = random.randint(0, n - 1)
            s.pop(i)
            n -= 1
        elif op == 1: # Insert a random character
            i = random.randint(0, n)
            char = random.choice(string.printable)
            s.insert(i, char)
            n += 1
        elif op == 2: # Replace a character
            if n > 0:
                i = random.randint(0, n - 1)
                char = random.choice(string.printable)
                s[i] = char
        elif op == 3: # Swap characters
            if n > 1:
                i, j = random.sample(range(n), 2)
                s[i], s[j] = s[j], s[i]
        elif op == 4 and n > 0: # Duplicate a character
            i = random.randint(0, n - 1)
            s.insert(i, s[i])
            n += 1
        elif op == 5 and n > 1: # Swap adjacent characters
            i = random.randint(0, n - 2)
            s[i], s[i+1] = s[i+1], s[i]

    # Specific JSON-related mutations
    if random.random() < 0.3: # Modify numbers
        match = re.search(r'(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', data)
        if match:
            num_str = match.group(0)
            mutated_num = num_str
            if random.random() < 0.5: # Add decimal point
                if '.' not in mutated_num:
                    insert_pos = random.randint(0, len(mutated_num))
                    mutated_num = mutated_num[:insert_pos] + '.' + mutated_num[insert_pos:]
            else: # Modify existing decimal
                if '.' in mutated_num:
                    dot_pos = mutated_num.find('.')
                    if random.random() < 0.5: # Remove decimal
                        mutated_num = mutated_num.replace('.', '')
                    else: # Shift decimal
                        parts = mutated_num.split('.')
                        if len(parts) == 2:
                            if parts[0] and parts[1]:
                                mutated_num = parts[1] + '.' + parts[0]
                            elif parts[0]:
                                mutated_num = parts[0] + '.'
                            elif parts[1]:
                                mutated_num = '.' + parts[1]
            
            if mutated_num != num_str:
                start, end = match.span()
                s = list(data[:start] + mutated_num + data[end:])

    if random.random() < 0.3: # Corrupt strings
        match = re.search(r'"([^"\\]*(\\.[^"\\]*)*)"', data)
        if match:
            start, end = match.span()
            original_str = match.group(1)
            mutated_str = list(original_str)
            
            for _ in range(random.randint(1, len(mutated_str) // 10 + 1)):
                idx = random.randint(0, len(mutated_str) - 1)
                if random.random() < 0.5:
                    mutated_str[idx] = random.choice(r'\"/') # Common escapes
                else:
                    mutated_str.pop(idx)
            
            if len(mutated_str) > 0:
                s = list(data[:start+1] + "".join(mutated_str) + data[end-1:])
            else:
                s = list(data[:start+1] + data[end-1:])


    if random.random() < 0.2: # Mismatched brackets/braces
        bracket_type = random.choice(['{}', '[]'])
        if bracket_type[0] in s:
            open_idx = s.index(bracket_type[0])
            s[open_idx] = bracket_type[1]
        elif bracket_type[1] in s:
            close_idx = s.index(bracket_type[1])
            s[close_idx] = bracket_type[0]

    if random.random() < 0.1: # Insert invalid characters
        i = random.randint(0, len(s))
        s.insert(i, random.choice('\x00\xff\xfe\xfd'))

    return "".join(s)