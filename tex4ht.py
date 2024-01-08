import pathlib
import sys
import tempfile
import re
import subprocess
import shutil
import css_inline

if len(sys.argv) < 3:
	print("Usage: tex4ht.py [in_file] [template_file] [out_file]")
	exit(1)

in_file = pathlib.Path(sys.argv[1])
template_file = pathlib.Path(sys.argv[2])
out_file = pathlib.Path(sys.argv[3])

with tempfile.TemporaryDirectory(prefix="tex4ht") as work_dir:
	work_dir = pathlib.Path(work_dir)

	with in_file.open() as f:
		input_tex = f.read()

	with template_file.open() as f:
		template_str = f.read()
		template_str = re.sub(r'\${{\s*\.Equation\s*}}\$', "[[REPLACE]]", template_str)
		template_str = template_str.replace("[[REPLACE]]", input_tex)
		template_str = template_str.replace(r"\strut{}", "")

	with (work_dir / "in.tex").open("w") as f:
		f.write(template_str)

	with (work_dir / "conf.cfg").open("w") as f:
		f.write(r"""\Preamble{xhtml}
\Configure{Gin-dim}{}
\Css{img {
    max-width: 100\%;
    height: auto;
}}
\begin{document}
\EndPreamble
""")

	subprocess.run(["/usr/bin/make4ht", "-x", "-c", "conf", "in.tex", "mathml"], check=True, cwd=work_dir)
	html_file = work_dir / "in.html"

	inliner = css_inline.CSSInliner(base_url="file://" + str(html_file.absolute()))
	with html_file.open() as f:
		inlined = inliner.inline(f.read())

	inlined = re.sub(r'class="[^"]*"', "", inlined)
	m = re.search(r'<body[^>]*>(.*)</body>', inlined, re.DOTALL)
	with out_file.open("w") as f:
		f.write(m.group(1).strip())
