#!/bin/bash
set -euo pipefail

if [ $# -eq 0 ]; then
	echo "Usage: run.sh [template]"
	exit 1
fi

template="$1"

if [ -f "extract-$template.py" ]; then
	python3 "extract-$template.py"
fi

python3 build.py "$template" > work.tmp

cat work.tmp | parallel --bar --halt now,fail=1 'bash -c {}'

if [ -x "$(command -v svgo)" ]; then
	find ./assets -iname "*.svg" | parallel --bar --halt now,fail=1 'svgo {}'
fi

if [ -f "output.zip" ]; then
	rm output.zip
fi

zip -r output.zip statements assets
