import re
import pathlib

input_dir = pathlib.Path("input")
output_dir = pathlib.Path("tex")

problem_search_re = re.compile(r'\\begin{problem}.*?\\end{problem}', re.DOTALL)

single_re = re.compile(r'\\begin{problem}{(.*?)}(.*?)\\begin{solution}{\$(.*?)\$}(.*?)\\end{solution}', re.DOTALL)
single_re_alt = re.compile(r'\\begin{problem}{(.*?)}(.*?)\\begin{solution}{(.*?)}(.*?)\\end{solution}', re.DOTALL)


def cleanlines(x):
	return "\n".join([i.strip() for i in x.splitlines()])

for file in input_dir.glob("*.tex"):
	print("Processing", file)
	lang = file.with_suffix("").name.lower()

	with file.open() as f:
		data = f.read()

	problems = problem_search_re.findall(data)

	for i, problem in enumerate(problems):
		problem_dir = output_dir / lang / f"{i+1:02d}"
		problem_dir.mkdir(parents=True, exist_ok=True)

		m = single_re.match(problem)
		if m is None:
			m = single_re_alt.match(problem)
			ans = m.group(3)
		else:
			ans = f"${m.group(3)}$"

		with open(problem_dir / "statement.tex", "w") as f:
			f.write(f"\\textbf{{{m.group(1)}}}\\\\\n{cleanlines(m.group(2))}")

		with open(problem_dir / "answer.tex", "w") as f:
			f.write(ans)

		with open(problem_dir / "solution.tex", "w") as f:
			f.write(cleanlines(m.group(4)))
