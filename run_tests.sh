#!/usr/bin/bash
python3 -m coverage run -m unittest discover coverage

# Omits the test files and system python libraries that appear
python3 -m coverage report --omit="*test_*,*/lib/python*/*"
python3 -m coverage xml