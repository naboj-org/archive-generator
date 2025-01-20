import pathlib
import sys
import json

input_dir = pathlib.Path("tex")
output_dir = pathlib.Path("statements")

if len(sys.argv) < 2:
    print("Usage: build.py [template]")
    exit(1)

template = pathlib.Path("templates") / sys.argv[1]

for directory in input_dir.glob("*"):
    if not directory.is_dir():
        continue

    lang = directory.name
    print("Processing", directory, file=sys.stderr)

    template_file = (template / lang).with_suffix(".tex")
    if not template_file.exists():
        print(f"Could not find template {template_file}.", file=sys.stderr)
        exit(1)

    template_real = template_file.readlink().with_suffix("").name

    for problem in directory.glob("*"):
        if not problem.is_dir():
            continue

        for part in ("answer", "solution", "statement"):
            input_file = problem / f"{part}.tex"
            output_file = output_dir / problem.relative_to(input_dir) / f"{part}.html"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            print(f"python tex4ht.py {input_file} {template_file} {output_file}")
