def mutate(data: str) -> str:
    """
    Aggressively mutates a JSON string to find crashes in a parser.
    """
    mutated_data = data
    
    # Basic mutations: character replacement, insertion, deletion, duplication
    for _ in range(random.randint(1, 5)):
        if not mutated_data:
            return "[]" # Handle empty string case
        
        mutation_type = random.choice([
            "replace", "insert", "delete", "duplicate", "swap", "truncate", "append_noise"
        ])
        
        pos = random.randint(0, len(mutated_data))
        
        if mutation_type == "replace":
            if mutated_data:
                char_to_replace = mutated_data[pos % len(mutated_data)]
                replacement_char = random.choice([
                    "{", "}", "[", "]", ":", ",", '"', "'", 
                    "\\", "/", "t", "f", "n", "r", "u", " ", "\n", "\t",
                    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                    ".", "-", "+", "e", "E",
                    random.choice(string.ascii_letters),
                    random.choice(string.punctuation),
                    chr(random.randint(0, 255)) # Include control characters and extended ASCII
                ])
                mutated_data = mutated_data[:pos] + replacement_char + mutated_data[pos+1:]
        elif mutation_type == "insert":
            insert_char = random.choice([
                "{", "}", "[", "]", ":", ",", '"', "'", 
                "\\", "/", "t", "f", "n", "r", "u", " ", "\n", "\t",
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                ".", "-", "+", "e", "E",
                random.choice(string.ascii_letters),
                random.choice(string.punctuation),
                chr(random.randint(0, 255))
            ])
            mutated_data = mutated_data[:pos] + insert_char + mutated_data[pos:]
        elif mutation_type == "delete":
            if mutated_data:
                mutated_data = mutated_data[:pos] + mutated_data[pos+1:]
        elif mutation_type == "duplicate":
            if mutated_data:
                mutated_data = mutated_data[:pos] + mutated_data[pos] + mutated_data[pos:]
        elif mutation_type == "swap":
            if len(mutated_data) > 1:
                pos2 = random.randint(0, len(mutated_data) - 1)
                if pos != pos2:
                    data_list = list(mutated_data)
                    data_list[pos], data_list[pos2] = data_list[pos2], data_list[pos]
                    mutated_data = "".join(data_list)
        elif mutation_type == "truncate":
            mutated_data = mutated_data[:pos]
        elif mutation_type == "append_noise":
            noise_len = random.randint(1, 20)
            noise = ''.join(random.choice(string.printable) for _ in range(noise_len))
            mutated_data += noise

    # More aggressive mutations: incorrect nesting, malformed numbers, invalid escapes
    if random.random() < 0.3: # Randomly apply these more complex mutations
        mutated_data = re.sub(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', r'\1.\2.\3', mutated_data) # Remove one part of IP-like numbers
        mutated_data = re.sub(r'([-+]?\d+)\.(\d+)', r'\1.\2.0', mutated_data) # Malform floats with multiple dots
        mutated_data = re.sub(r'"([^"\\]*(?:\\.[^"\\]*)*)"', lambda m: m.group(1).replace('\\', '\\\\'), mutated_data) # Escape backslashes in strings
        mutated_data = re.sub(r'"([^"\\]*(?:\\.[^"\\]*)*)"', lambda m: m.group(1).replace('"', '\\"'), mutated_data) # Escape quotes in strings
        mutated_data = re.sub(r'([{\[])', r'\1\1', mutated_data) # Duplicate opening brackets/braces
        mutated_data = re.sub(r'([}\]])', r'\1\1', mutated_data) # Duplicate closing brackets/braces
        mutated_data = re.sub(r'(\w+):', r'"\1":', mutated_data) # Unquote keys
        mutated_data = re.sub(r':(\w+)', r':"\1"', mutated_data) # Quote values
        mutated_data = re.sub(r':(true|false|null)', r': \1', mutated_data) # Add space after keywords
        mutated_data = re.sub(r'([\d.eE+-]+)', r'[\1]', mutated_data) # Wrap numbers in arrays
        mutated_data = re.sub(r'"([{}])"', r'\1', mutated_data) # Remove empty object/array strings
        mutated_data = re.sub(r'([{\[])\s*,', r'\1', mutated_data) # Remove trailing comma after opening bracket/brace
        mutated_data = re.sub(r',(\s*[}\]])', r'\1', mutated_data) # Remove leading comma before closing bracket/brace
        mutated_data = re.sub(r'\\\s*', '', mutated_data) # Remove escaped whitespace
        mutated_data = re.sub(r'([a-zA-Z0-9])([a-zA-Z0-9])', r'\1 \2', mutated_data) # Insert spaces between alphanumeric chars

    # Add some common malformed JSON patterns
    if random.random() < 0.2:
        mutated_data = "{" + mutated_data + "}" # Ensure it's wrapped in an object
        mutated_data = mutated_data.replace('{}', '{.}.')
        mutated_data = mutated_data.replace('[]', '[.].[].')
        
    # Ensure some control characters are present
    if random.random() < 0.1:
        for char_code in [0x00, 0x01, 0x07, 0x08, 0x0B, 0x0C, 0x0E, 0x1F]:
            if random.random() < 0.5:
                mutated_data += chr(char_code)

    # Truncate or repeat characters at the end for edge cases
    if len(mutated_data) > 1000:
        mutated_data = mutated_data[:random.randint(500, 1000)]
    elif len(mutated_data) < 10:
        mutated_data = mutated_data * random.randint(2, 10)

    # Final cleanup for potentially invalid JSON that might be generated
    # This is a heuristic to keep it somewhat parsable while introducing errors
    mutated_data = mutated_data.replace('\\"', '"') # Undo some escaping if it makes it invalid
    mutated_data = mutated_data.replace('"{', '{')
    mutated_data = mutated_data.replace('}"', '}')
    mutated_data = mutated_data.replace('"[', '[')
    mutated_data = mutated_data.replace(']"', ']')
    mutated_data = mutated_data.replace('":', ':')
    mutated_data = mutated_data.replace(':"', ':"')
    mutated_data = mutated_data.replace('":', '":')
    
    # Randomly corrupt characters that are unlikely to be valid JSON tokens
    chars_to_corrupt = [chr(i) for i in range(256) if chr(i) not in ' \t\n\r{}[]:, "' + string.ascii_letters + string.digits + '-.eE+']
    for _ in range(random.randint(0, 3)):
        if mutated_data:
            pos = random.randint(0, len(mutated_data) - 1)
            mutated_data = mutated_data[:pos] + random.choice(chars_to_corrupt) + mutated_data[pos+1:]

    return mutated_data