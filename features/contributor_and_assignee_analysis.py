import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from data_loader import DataLoader

class ContributorAndAssigneeAnalysis:
    """
    Analyzes contributors and assignees from GitHub issues and visualizes the results.
    """

    def __init__(self):
        """
        Constructor
        """
        self.issues = DataLoader().get_issues()  # Load issues using DataLoader


    def plot_contributors_assignees_and_labels(self, contributor_df: pd.DataFrame, assignee_df: pd.DataFrame, label_df: pd.DataFrame, top_contributors_count: int, top_assignees_count: int, label: str = None):
        """
        Plots the top contributors, assignees, and labels on the same page (side by side).
        """
        # Create subplots with 1 row and 3 columns
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

        # Plot contributors (vertical bar chart)
        contributor_df = contributor_df.nlargest(top_contributors_count, 'Issue Count')
        axes[0].bar(contributor_df['Contributor'], contributor_df['Issue Count'], color='skyblue')
        
        # Set title for contributors based on the label
        if label:
            axes[0].set_title(f'Top Contributors for {label}')
        else:
            axes[0].set_title('Top Contributors')

        axes[0].set_xlabel('Contributors')
        axes[0].set_ylabel('Number of Issues')

        # Add count labels on the bars
        for index, value in enumerate(contributor_df['Issue Count']):
            axes[0].text(index, value, int(value), ha='center', va='bottom')  # ha: horizontal alignment

        # Rotate the x-axis labels for contributors
        plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha="right")

        # Plot assignees (vertical bar chart)
        assignee_df = assignee_df.nlargest(top_assignees_count, 'Issue Count')
        axes[1].bar(assignee_df['Assignee'], assignee_df['Issue Count'], color='salmon')

        # Set title for assignees based on the label
        if label:
            axes[1].set_title(f'Top Assignees for {label}')
        else:
            axes[1].set_title('Top Assignees')

        axes[1].set_xlabel('Assignees')
        axes[1].set_ylabel('Number of Issues')

        # Add count labels on the bars
        for index, value in enumerate(assignee_df['Issue Count']):
            axes[1].text(index, value, int(value), ha='center', va='bottom')

        # Rotate the x-axis labels for assignees
        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha="right")

        # Plot label frequencies (vertical bar chart)
        label_df = label_df.nlargest(10, 'Frequency')  # Top 10 labels
        axes[2].bar(label_df['Label'], label_df['Frequency'], color='lightgreen')

        # Set title for labels
        axes[2].set_title('Top Labels')

        axes[2].set_xlabel('Labels')
        axes[2].set_ylabel('Frequency')

        # Add count labels on the bars
        for index, value in enumerate(label_df['Frequency']):
            axes[2].text(index, value, int(value), ha='center', va='bottom')

        # Rotate the x-axis labels for labels
        plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=45, ha="right")

        # Adjust layout for better readability
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.2, hspace=0.2, left=0.04, right=0.99, top=0.938, bottom=0.26)
        plt.show()


    def plot_contributors_and_assignees(self, contributor_df: pd.DataFrame, assignee_df: pd.DataFrame, top_contributors_count: int, top_assignees_count: int, label: str = None):
        """
        Plots the top contributors and assignees on the same page (side by side), with dynamic titles for label.
        """
        # Create subplots with 1 row and 2 columns
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

        # Plot contributors (vertical bar chart)
        contributor_df = contributor_df.nlargest(top_contributors_count, 'Issue Count')
        axes[0].bar(contributor_df['Contributor'], contributor_df['Issue Count'], color='skyblue')
        
        # Set title for contributors based on the label
        if label:
            axes[0].set_title(f'Top Contributors for {label}')
        else:
            axes[0].set_title('Top Contributors')

        axes[0].set_xlabel('Contributors')
        axes[0].set_ylabel('Number of Issues')

        # Add count labels on the bars
        for index, value in enumerate(contributor_df['Issue Count']):
            axes[0].text(index, value, int(value), ha='center', va='bottom')  # ha: horizontal alignment

        # Rotate the x-axis labels for contributors
        plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha="right")

        # Plot assignees (vertical bar chart)
        assignee_df = assignee_df.nlargest(top_assignees_count, 'Issue Count')
        axes[1].bar(assignee_df['Assignee'], assignee_df['Issue Count'], color='salmon')

        # Set title for assignees based on the label
        if label:
            axes[1].set_title(f'Top Assignees for {label}')
        else:
            axes[1].set_title('Top Assignees')

        axes[1].set_xlabel('Assignees')
        axes[1].set_ylabel('Number of Issues')

        # Add count labels on the bars
        for index, value in enumerate(assignee_df['Issue Count']):
            axes[1].text(index, value, int(value), ha='center', va='bottom')  # ha: horizontal alignment

        # Rotate the x-axis labels for assignees
        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha="right")

        # Adjust layout for better readability
        plt.tight_layout()
        plt.show()


    def fetch_and_plot(self):
        """
        Fetches the top contributors and assignees and plots them without any label filter.
        """
        # Ask user for the number of contributors and assignees to display
        top_contributors_count = int(input("Enter the number of contributors to display: "))
        top_assignees_count = int(input("Enter the number of assignees to display: "))
        
        contributor_counts = {}
        assignee_counts = {}
        label_counts = Counter()

        for issue in self.issues:
            # Count contributors
            contributor = issue.creator
            contributor_counts[contributor] = contributor_counts.get(contributor, 0) + 1

            # Count assignees (if any)
            if issue.assignees:
                for assignee in issue.assignees:
                    assignee_username = assignee['login']
                    assignee_counts[assignee_username] = assignee_counts.get(assignee_username, 0) + 1

            # Count labels (directly from the list of label strings)
            for label in issue.labels:
                label_counts[label] += 1

        # Create DataFrames from counts
        contributor_df = pd.DataFrame(list(contributor_counts.items()), columns=['Contributor', 'Issue Count'])
        assignee_df = pd.DataFrame(list(assignee_counts.items()), columns=['Assignee', 'Issue Count'])
        label_df = pd.DataFrame(list(label_counts.items()), columns=['Label', 'Frequency'])

        # Plot the analysis for contributors, assignees, and labels
        self.plot_contributors_assignees_and_labels(contributor_df, assignee_df, label_df, top_contributors_count, top_assignees_count)


    def fetch_and_plot_with_label(self, label: str):
        """
        Fetches the top contributors and assignees for a particular label and plots them.
        """
        contributor_counts = {}
        assignee_counts = {}

        # Iterate over all issues and filter them by the provided label
        for issue in self.issues:
            if label not in [lbl for lbl in issue.labels]:  # Check if the label is in the issue labels
                continue

            # Count contributors
            contributor = issue.creator
            contributor_counts[contributor] = contributor_counts.get(contributor, 0) + 1

            # Count assignees
            for assignee in issue.assignees:
                assignee_username = assignee['login']  # Ensure to extract correctly
                assignee_counts[assignee_username] = assignee_counts.get(assignee_username, 0) + 1

        # Create DataFrames from counts
        contributor_df = pd.DataFrame(list(contributor_counts.items()), columns=['Contributor', 'Issue Count'])
        assignee_df = pd.DataFrame(list(assignee_counts.items()), columns=['Assignee', 'Issue Count'])

        # Check if the DataFrames are empty
        if contributor_df.empty and assignee_df.empty:
            print(f"Error: No such label '{label}' found.")
            return

        # Ask user for the number of contributors and assignees to display only if data is available
        top_contributors_count = int(input("Enter the number of contributors to display: "))
        top_assignees_count = int(input("Enter the number of assignees to display: "))

        # Plot the analysis for contributors and assignees with the specified label
        self.plot_contributors_and_assignees(contributor_df, assignee_df, top_contributors_count, top_assignees_count, label)
