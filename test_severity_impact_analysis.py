import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from dateutil import parser  # For date parsing
from features.severity_and_impact_analysis import SeverityAndImpactAnalysis, Issue  # Replace 'your_module' with actual module
import pandas as pd

class TestSeverityAndImpactAnalysis(unittest.TestCase):
    
    @patch('data_loader.DataLoader.get_issues')
    def setUp(self, mock_get_issues):     
        # Mock get_issues to return the test data
        dummy_issue_empty_events = {
            'url': 'http://example.com/issue/1',
            'creator': 'John Doe',
            'state': 'open',
            'assignees': ['Alice'],
            'title': 'Sample Issue with Empty Events',
            'text': 'This is a sample issue description.',
            'number': 123,
            'created_date': '2024-11-23T10:00:00Z',
            'updated_date': '2024-11-23T12:00:00Z',
            'timeline_url': 'http://example.com/issue/1/timeline',
            'events': []  # Empty events list
        }
        
        # Return a list with a single issue object
        mock_get_issues.return_value = [Issue(dummy_issue_empty_events)]
        
        # Initialize the analysis object after mocking
        self.analysis = SeverityAndImpactAnalysis()
    
    def test_fetch_plot(self):
        # Test normal flow
        try:
            self.analysisnormal = SeverityAndImpactAnalysis()
            self.analysisnormal.fetch_and_plot()    
        except AssertionError as e:
            # If we catch AssertionError, the test fails
            assert False, f"Expected no error, but got AssertionError: {str(e)}"
    
    def test_fetch_plot_input_validation(self):
        dummy_issue_empty_events = {
            'url': 'http://example.com/issue/1',
            'creator': 'John Doe',
            'labels': ['bug', 'urgent'],
            'state': 'open',
            'assignees': ['Alice'],
            'title': 'Sample Issue with Empty Events',
            'text': 'This is a sample issue description.',
            'number': 123,
            'created_date': '2024-11-23T10:00:00Z',
            'updated_date': '2024-11-23T12:00:00Z',
            'timeline_url': 'http://example.com/issue/1/timeline',
            'events': []  # Empty events list
        }
        
        issue_empty_events = Issue(dummy_issue_empty_events)
        self.analysis.issues = [issue_empty_events]
        
        try:
            self.analysis.fetch_and_plot()    
        except AssertionError as e:
            assert False, f"Expected no error, but got AssertionError: {str(e)}"
    
    def test_fetch_plot_with_empty_issues(self):
        # Test case where no issues are provided
        self.analysis.issues = []
        try:
            self.analysis.fetch_and_plot()    
        except AssertionError as e:
            assert False, f"Expected no error, but got AssertionError: {str(e)}"

    ##########
    ### The poetry data has labels in the form of kind/bug, status/triage, kind/feature, etc.
    ### severity_impact_analysis is checking the labels contains of of their custom
    ### labels:  {'Bug', 'Needs Triage', 'Feature'}, so the severity score is often times incorrect
    ##########
    
    def test_calculate_bug_severity(self):
        bug_issue = {'labels': ['kind/bug'], 'state': 'open', 'created_date': datetime.now(timezone.utc)}
        analysis = SeverityAndImpactAnalysis()

        # Expected results: 7.0, ("kind/bug" + "open" + "now - now") --> 5 + 2 + 0.0 = 7.0
        bug_score = analysis.calculate_severity(bug_issue)
        self.assertEqual(bug_score, 7.0)
        
    
    def test_calculate_triage_severity(self):
        triage_issue = {'labels': ['status/triage'], 'state': 'open', 'created_date': datetime.now(timezone.utc)}
        analysis = SeverityAndImpactAnalysis()

        # Expected results: 5.0: ("status/triage" + "open" + "now - now") --> 3 + 2 + 0.0 = 5.0
        triage_score = analysis.calculate_severity(triage_issue)
        self.assertEqual(triage_score, 5.0)

    def test_calculate_feature_severity(self):
        feature_issue = {'labels': ['kind/feature'], 'state': 'closed', 'created_date': datetime.now(timezone.utc)}
        analysis = SeverityAndImpactAnalysis()

        # Expected results: 1.0: ("kind/feature" + "closed" + "now - now") --> 1 + 0 + 0.0 = 1.0
        feature_score = analysis.calculate_severity(feature_issue)
        self.assertEqual(feature_score, 1.0)
        

if __name__ == "__main__":
    unittest.main()
