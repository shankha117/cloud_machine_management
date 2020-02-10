#!/usr/bin/env bash
python3 -m compileall -b .
find . -type f -name '*.py' -delete
