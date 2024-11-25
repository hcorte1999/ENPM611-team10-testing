import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from dateutil import parser  # For date parsing
from features.severity_and_impact_analysis import SeverityAndImpactAnalysis, Issue
import pandas as pd

class TestSeverityAndImpactAnalysis(unittest.TestCase):
    
    # @patch('data_loader.DataLoader.get_issues')
    # def setUp(self, mock_get_issues):     
    #     # Mock get_issues to return the test data
    #     dummy_issue_empty_events = {
    #         'url': 'http://example.com/issue/1',
    #         'creator': 'John Doe',
    #         'state': 'open',
    #         'assignees': ['Alice'],
    #         'title': 'Sample Issue with Empty Events',
    #         'text': 'This is a sample issue description.',
    #         'number': 123,
    #         'created_date': '2024-11-23T10:00:00Z',
    #         'updated_date': '2024-11-23T12:00:00Z',
    #         'timeline_url': 'http://example.com/issue/1/timeline',
    #         'events': []  # Empty events list
    #     }
        
    #     # Return a list with a single issue object
    #     mock_get_issues.return_value = [Issue(dummy_issue_empty_events)]
        
    #     # Initialize the analysis object after mocking
    #     self.analysis = SeverityAndImpactAnalysis()
    
    # def test_fetch_plot(self):
    #     # Test normal flow
    #     try:
    #         self.analysisnormal = SeverityAndImpactAnalysis()
    #         self.analysisnormal.fetch_and_plot()    
    #     except AssertionError as e:
    #         # If we catch AssertionError, the test fails
    #         assert False, f"Expected no error, but got AssertionError: {str(e)}"
    
    # def test_fetch_plot_input_validation(self):
    #     dummy_issue_empty_events = {
    #         'url': 'http://example.com/issue/1',
    #         'creator': 'John Doe',
    #         'labels': ['bug', 'urgent'],
    #         'state': 'open',
    #         'assignees': ['Alice'],
    #         'title': 'Sample Issue with Empty Events',
    #         'text': 'This is a sample issue description.',
    #         'number': 123,
    #         'created_date': '2024-11-23T10:00:00Z',
    #         'updated_date': '2024-11-23T12:00:00Z',
    #         'timeline_url': 'http://example.com/issue/1/timeline',
    #         'events': []  # Empty events list
    #     }
        
    #     issue_empty_events = Issue(dummy_issue_empty_events)
    #     self.analysis.issues = [issue_empty_events]
        
    #     try:
    #         self.analysis.fetch_and_plot()    
    #     except AssertionError as e:
    #         assert False, f"Expected no error, but got AssertionError: {str(e)}"
    
    # def test_fetch_plot_with_empty_issues(self):
    #     # Test case where no issues are provided
    #     self.analysis.issues = []
    #     try:
    #         self.analysis.fetch_and_plot()    
    #     except AssertionError as e:
    #         assert False, f"Expected no error, but got AssertionError: {str(e)}"

    # ##########
    # ### The poetry data has labels in the form of kind/bug, status/triage, kind/feature, etc.
    # ### severity_impact_analysis is checking the labels contains of of their custom
    # ### labels:  {'Bug', 'Needs Triage', 'Feature'}, so the severity score is often times incorrect
    # ##########
    
    # def test_calculate_bug_severity(self):
    #     bug_issue = {'labels': ['kind/bug'], 'state': 'open', 'created_date': datetime.now(timezone.utc)}
    #     analysis = SeverityAndImpactAnalysis()

    #     # Expected results: 7.0, ("kind/bug" + "open" + "now - now") --> 5 + 2 + 0.0 = 7.0
    #     bug_score = analysis.calculate_severity(bug_issue)
    #     self.assertEqual(bug_score, 7.0)
        
    
    # def test_calculate_triage_severity(self):
    #     triage_issue = {'labels': ['status/triage'], 'state': 'open', 'created_date': datetime.now(timezone.utc)}
    #     analysis = SeverityAndImpactAnalysis()

    #     # Expected results: 5.0: ("status/triage" + "open" + "now - now") --> 3 + 2 + 0.0 = 5.0
    #     triage_score = analysis.calculate_severity(triage_issue)
    #     self.assertEqual(triage_score, 5.0)

    # def test_calculate_feature_severity(self):
    #     feature_issue = {'labels': ['kind/feature'], 'state': 'closed', 'created_date': datetime.now(timezone.utc)}
    #     analysis = SeverityAndImpactAnalysis()

    #     # Expected results: 1.0: ("kind/feature" + "closed" + "now - now") --> 1 + 0 + 0.0 = 1.0
    #     feature_score = analysis.calculate_severity(feature_issue)
    #     self.assertEqual(feature_score, 1.0)
        
# Calculate impact tests

    def test_calculate_impact(self):
        bug_issue = {'labels': ['Bug'], 'state': 'open', 'created_date': datetime.now(timezone.utc), 
            'title': "python version resolution is messed up",
            'text': "bug - I am trying to install PyTorch CUDA version",
            'events': [{"event_type": "labeled"},{"event_type": "labeled"}]
        }
        analysis = SeverityAndImpactAnalysis()

        # Expected results: 3.0, ("kind/bug" + 2 events) --> 1 + 2 = 3.0
        bug_score = analysis.calculate_impact(bug_issue)
        self.assertEqual(bug_score, 3.0)


    # This is a bug in the code. In the data file, bugs are labeled with 'kind/bug', but in the function we are checking
    # for 'Bug' in the label. This does not meet expected functionality, labels should be stripped of 'kind/' and ignore case 
    def test_calculate_impact_with_bug_label(self):
        bug_issue = {'labels': ['kind/bug'], 'state': 'open', 'created_date': datetime.now(timezone.utc), 
            'title': "python version resolution is messed up",
            'text': "I am trying to install PyTorch CUDA version",
            'events': []
        }
        analysis = SeverityAndImpactAnalysis()

        # Expected results: 1.0, ("kind/bug" ) --> 1 = 1.0
        bug_score = analysis.calculate_impact(bug_issue)
        self.assertEqual(bug_score, 1.0)


    def test_calculate_impact_with_feature(self):
        bug_issue = {'labels': ['kind/feature'], 'state': 'open', 'created_date': datetime.now(timezone.utc), 
            'title': "python version resolution is messed up",
            'text': "I am trying to install PyTorch CUDA version",
            'events': []
        }
        analysis = SeverityAndImpactAnalysis()

        # Expected results: 0.0, no mention of bugs or CI failure --> 0 = 0.0
        bug_score = analysis.calculate_impact(bug_issue)
        self.assertEqual(bug_score, 0.0)


    def test_calculate_impact_with_CI_failure(self):
        bug_issue = {'labels': ['CI Failure'], 'state': 'open', 'created_date': datetime.now(timezone.utc), 
            'title': "CI failure python version resolution is messed up",
            'text': "CI failure python version resolution is messed up",
            'events': [{"event_type": "labeled"},{"event_type": "labeled"}]
        }
        analysis = SeverityAndImpactAnalysis()

        # Expected results: 5.0: ("CI Failure" label + CI failure in title + title in text + 2 events) --> 1 + 1 + 1 + 2 = 5.0
        bug_score = analysis.calculate_impact(bug_issue)
        self.assertEqual(bug_score, 5.0)    

# plot_combined_visualizations tests
    @patch("matplotlib.pyplot.show")
    @patch('seaborn.histplot')
    def test_plot_combined_visualizations_should_plot_severity(self, mock_histplot, _):
        data = {
            'severity_score': [3, 5, 0, 0, 2],
            'impact_score': [1, 4, 9, 5, 1],
            'state': ['open', 'closed', 'open', 'closed', 'open']
        }
        analysis = SeverityAndImpactAnalysis()
        analysis.df = pd.DataFrame(data)
        
        analysis.plot_combined_visualizations()

        args, kwargs = mock_histplot.call_args_list[0]
        severity_scores = args
        self.assertEqual(severity_scores[0].tolist(), [3, 5, 0, 0, 2])
        

    @patch("matplotlib.pyplot.show")
    @patch('seaborn.histplot')
    def test_plot_combined_visualizations_should_plot_impact(self, mock_histplot, _):
        data = {
            'severity_score': [3, 5, 0, 0, 2],
            'impact_score': [1, 4, 9, 5, 1],
            'state': ['open', 'closed', 'open', 'closed', 'open']
        }
        analysis = SeverityAndImpactAnalysis()
        analysis.df = pd.DataFrame(data)
        
        analysis.plot_combined_visualizations()

        args, kwargs = mock_histplot.call_args_list[1]
        impact_scores = args
        self.assertEqual(impact_scores[0].tolist(), [1, 4, 9, 5, 1])


    @patch("matplotlib.pyplot.show")
    @patch('seaborn.scatterplot')
    def test_plot_combined_visualizations_should_call_scatter_plot(self, mock_scatplot, _):
        data = {
            'severity_score': [3, 5, 0, 0, 2],
            'impact_score': [1, 4, 9, 5, 1],
            'state': ['open', 'closed', 'open', 'closed', 'open']
        }
        analysis = SeverityAndImpactAnalysis()
        analysis.df = pd.DataFrame(data)
        
        analysis.plot_combined_visualizations()

        args = mock_scatplot.call_args

        severity_scores = args[1]['data']['severity_score'].tolist()
        impact_scores = args[1]['data']['impact_score'].tolist()
        states = args[1]['data']['state'].tolist()

        self.assertEqual(severity_scores, [3, 5, 0, 0, 2])
        self.assertEqual(impact_scores, [1, 4, 9, 5, 1])
        self.assertEqual(states, ['open', 'closed', 'open', 'closed', 'open'])
        

if __name__ == "__main__":
    unittest.main()
