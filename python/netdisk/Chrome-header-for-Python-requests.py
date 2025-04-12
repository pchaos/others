def parse_header(raw_header: str):
    header = dict()

    for line in raw_header.split("\n"):

        if line.startswith(":"):
            a, b = line[1:].split(":", 1)
            a = f":{a}"
        else:
            a, b = line.split(":",1)

        header[a.strip()] = b.strip()

    return header