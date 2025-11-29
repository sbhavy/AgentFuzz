def mutate(data: str) -> str:
    s = list(data)
    n = len(s)
    for _ in range(random.randint(1, 10)):
        mutator = random.choice([
            lambda: random.choice(string.printable),
            lambda: '',
            lambda: s[random.randint(0, n - 1)] if n > 0 else '',
            lambda: random.choice(['{', '}', '[', ']', ':', ',', '"', "'", ' ', '\n', '\t']),
            lambda: random.choice(['true', 'false', 'null']),
            lambda: str(random.randint(-1000, 1000))
        ])
        mutation_type = random.randint(0, 5)

        if mutation_type == 0 and n > 0:  # Character replacement
            idx = random.randint(0, n - 1)
            s[idx] = mutator()
        elif mutation_type == 1:  # Insertion
            idx = random.randint(0, n)
            s.insert(idx, mutator())
            n += 1
        elif mutation_type == 2 and n > 0:  # Deletion
            idx = random.randint(0, n - 1)
            s.pop(idx)
            n -= 1
        elif mutation_type == 3 and n > 0:  # Swap
            idx1 = random.randint(0, n - 1)
            idx2 = random.randint(0, n - 1)
            s[idx1], s[idx2] = s[idx2], s[idx1]
        elif mutation_type == 4 and n > 0: # Duplicate
            idx = random.randint(0, n - 1)
            s.insert(idx, s[idx])
            n += 1
        elif mutation_type == 5 and n > 0: # Block deletion
            start = random.randint(0, n - 1)
            end = random.randint(start, n - 1)
            del s[start:end+1]
            n = len(s)

    return "".join(s)