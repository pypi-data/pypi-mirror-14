#!/usr/bin/env bash

echo "line1
line2
line3" | python -c "import stdin;print(stdin.STDIN)"

