def deactivate_account(file, name, acc_id):
    acc_id = f"{int(acc_id):05}"
    name = name.ljust(20)[:20]

    with open(file, "r") as f:
        lines = f.readlines()

    while lines and lines[-1].strip() == "":
        lines.pop()

    delimiter = lines.pop()

    updated_lines = []
    for line in lines:
        if len(line) < 30:
            updated_lines.append(line)
            continue

        line_id = line[0:5]
        line_name = line[6:26]

        if line_id == acc_id and line_name == name:
            line = line[:27] + "D" + line[28:]

        updated_lines.append(line)

    with open(file, "w", newline="\n") as f:
        for line in updated_lines:
            f.write(line)
        f.write(delimiter)

    return True


def delete_account(file, name, acc_id):
    acc_id = f"{int(acc_id):05}"
    name = name.ljust(20)[:20]

    with open(file, "r") as f:
        lines = f.readlines()

    while lines and lines[-1].strip() == "":
        lines.pop()

    delimiter = lines.pop()

    new_lines = []
    for line in lines:
        if len(line) < 30:
            continue

        line_id = line[0:5]
        line_name = line[6:26]

        if line_id == acc_id and line_name == name:
            continue

        new_lines.append(line)

    with open(file, "w", newline="\n") as f:
        for line in new_lines:
            f.write(line)
        f.write(delimiter)

    return True