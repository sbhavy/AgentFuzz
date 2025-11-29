def mutate(data: str) -> str:
    mutated_data = data
    mutations = [
        lambda d: d + "}",
        lambda d: d[:-1] if d.endswith("}") else d,
        lambda d: d.replace(" ", ""),
        lambda d: d.replace('":', '": ' if random.random() > 0.5 else '":'),
        lambda d: d.replace(",", ", ") if random.random() > 0.5 else d.replace(",", ","),
        lambda d: d.replace("[", "[ ") if random.random() > 0.5 else d.replace("[", "["),
        lambda d: d.replace("]", " ]") if random.random() > 0.5 else d.replace("]", "]"),
        lambda d: d.replace("{", "{ ") if random.random() > 0.5 else d.replace("{", "{"),
        lambda d: d.replace("}", " }") if random.random() > 0.5 else d.replace("}", "}"),
        lambda d: d.replace("null", "null ") if random.random() > 0.5 else d,
        lambda d: d.replace("true", "true ") if random.random() > 0.5 else d,
        lambda d: d.replace("false", "false ") if random.random() > 0.5 else d,
        lambda d: d.replace('"a"', '"a" ') if random.random() > 0.5 else d,
        lambda d: d.replace('1', '1 ') if random.random() > 0.5 else d,
        lambda d: d.replace('2', '2 ') if random.random() > 0.5 else d,
        lambda d: d.replace('3', '3 ') if random.random() > 0.5 else d,
        lambda d: d.replace('4', '4 ') if random.random() > 0.5 else d,
        lambda d: d.replace('"', '\\"') if random.random() > 0.5 else d,
        lambda d: d.replace("'", '"') if "'" in d else d,
        lambda d: d.replace('true', 'True') if random.random() > 0.5 else d,
        lambda d: d.replace('false', 'False') if random.random() > 0.5 else d,
        lambda d: d.replace('null', 'None') if random.random() > 0.5 else d,
        lambda d: d + random.choice([" ", "\n", "\t", "\r", "z"]),
        lambda d: d[:-1] if len(d) > 1 and random.random() > 0.5 else d,
        lambda d: d[1:] if len(d) > 1 and random.random() > 0.5 else d,
        lambda d: d.replace(", ,", ","),
        lambda d: d.replace("[,", "["),
        lambda d: d.replace(",]", "]"),
        lambda d: d.replace("{,", "{"),
        lambda d: d.replace(",}", "}"),
        lambda d: d.replace(":{", ": {"),
        lambda d: d.replace(":[", ": ["),
        lambda d: d.replace(":1", ": 1"),
        lambda d: d.replace(":'", ": '"),
        lambda d: d.replace(':"', ': "'),
        lambda d: d.replace("true,", "true, "),
        lambda d: d.replace("false,", "false, "),
        lambda d: d.replace("null,", "null, "),
        lambda d: "".join(random.sample(d, len(d))),
    ]

    num_mutations = random.randint(1, min(5, len(mutations)))
    selected_mutations = random.sample(mutations, num_mutations)

    for mutation in selected_mutations:
        mutated_data = mutation(mutated_data)

    # Add some random characters at the end
    if random.random() < 0.3:
        mutated_data += ''.join(random.choice(string.printable) for _ in range(random.randint(1, 5)))

    # Corrupt specific patterns if they exist
    if ", ," in mutated_data:
        mutated_data = mutated_data.replace(", ,", ",")
    if "[," in mutated_data:
        mutated_data = mutated_data.replace("[,", "[")
    if ",]" in mutated_data:
        mutated_data = mutated_data.replace(",]", "]")
    if "{," in mutated_data:
        mutated_data = mutated_data.replace("{,", "{")
    if ",}" in mutated_data:
        mutated_data = mutated_data.replace(",}", "}")

    return mutated_data