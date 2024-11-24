#!/usr/bin/bash
python3 -m coverage run -m unittest discover
python3 -m coverage report --omit="*test_*,*/lib/python*/*"
python3 -m coverage xml