import config
import pandas as pd
import matplotlib.pyplot as plt
from typing import List

from data_loader import DataLoader
from model import Issue, Event

class BugPatternsAnalysis:
    """
    Analyzes bug patterns and frequency from GitHub issues.
    """

    def __init__(self):
        """
        Constructor
        """
        self.LABEL: str = config.get_parameter('label')

    def run(self):
        """
        Starting point for the bug pattern analysis.
        """
        issues: List[Issue] = DataLoader().get_issues()

        ### BUG PATTERNS AND FREQUENCY
        # Define a list of keywords that commonly appear in bug-related issues
        bug_keywords = ['bug', 'error', 'fail', 'exception', 'crash', 'not working', 'unexpected']
        bug_patterns_count = {}

        # Loop through issues to detect keywords in titles or labels and count occurrences
        for issue in issues:
            issue_text = (issue.title + ' ' + ' '.join(issue.labels)).lower()
            for keyword in bug_keywords:
                if keyword in issue_text:
                    bug_patterns_count[keyword] = bug_patterns_count.get(keyword, 0) + 1

        bug_patterns_count = sorted(bug_patterns_count.items(), key=lambda x: x[1], reverse=True)

        # Output results
        print("\n\nBug Patterns and Frequency Analysis:\n")
        for keyword, count in bug_patterns_count:
            print(f"{keyword.capitalize()}: {count} occurrences")

        ### BAR CHART FOR BUG PATTERNS
        # Visualize the frequency of each bug pattern in a bar chart
        if bug_patterns_count:
            bug_patterns_df = pd.DataFrame(list(bug_patterns_count), columns=['Pattern', 'Frequency'])
            bug_patterns_chart = bug_patterns_df.set_index('Pattern').plot(
                kind='bar', 
                figsize=(12, 6), 
                title="Bug Patterns and Their Frequency"
            )
            plt.xlabel("Bug Patterns")
            plt.ylabel("Frequency")

            for bar in bug_patterns_chart.patches:
                bug_patterns_chart.annotate(
                    f'{int(bar.get_height())}', 
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                    ha='center', 
                    va='bottom', 
                    fontsize=10, 
                    color='black'
                )
            
            plt.show()

        else:
            print("No bug patterns found.\n")

if __name__ == "__main__":
    BugPatternsAnalysis().run()
