python3 -m unittest test_bug_pattern_analysis.py
#python3 -m unittest test_contributor_and_assignee_analysis.py
#python3 -m unittest test_severity_and_impact_analysis.py

python3 -m coverage run -m unittest discover
python3 -m coverage report --omit="*test_*,*/lib/python*/*"
