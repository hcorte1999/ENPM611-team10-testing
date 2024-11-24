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

if __name__ == "__main__":
    unittest.main()
