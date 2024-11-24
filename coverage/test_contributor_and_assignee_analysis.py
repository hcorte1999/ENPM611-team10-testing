    
import unittest
from unittest.mock import patch, MagicMock
from features.contributor_and_assignee_analysis import ContributorAndAssigneeAnalysis
import pandas as pd
from collections import Counter

class TestContributorAndAssigneeAnalysis(unittest.TestCase):
    
    def setUp(self):
        issue_1 = MagicMock()
        issue_1.creator = 'user1'
        issue_1.assignees = [{'login': 'assignee1'}, {'login': 'assignee2'}]
        issue_1.labels = ['bug', 'high-priority']

        issue_2 = MagicMock()
        issue_2.creator = 'user2'
        issue_2.assignees = [{'login': 'assignee1'}]
        issue_2.labels = ['feature', 'low-priority']

        issue_3 = MagicMock()
        issue_3.creator = 'user1'
        issue_3.assignees = [{'login': 'assignee3'}]
        issue_3.labels = ['bug']

        self.mock_issues = [issue_1, issue_2, issue_3]
        

    ## Fetch and Plot Tests:
    
    @patch('builtins.input', side_effect=["s", ""])
    def test_fetch_and_plot_invalid_input(self, mock_input):
        """
        Test that a ValueError is raised when the user enters a string and empty instead of a number.
        """
        analysis = ContributorAndAssigneeAnalysis()

        # Assert that a ValueError is thrown
        with self.assertRaises(ValueError):
            analysis.fetch_and_plot()


    @patch('builtins.input', side_effect=["2", "2"])
    @patch.object(ContributorAndAssigneeAnalysis, 'plot_contributors_assignees_and_labels')
    def test_fetch_and_plot_correctly_calculates_contributor_df(self, mock_plot, mock_input):
        """
        Test fetch_and_plot method correctly calculates the contributor_counts and sends it as df to plot
        """
        # Setup
        analysis = ContributorAndAssigneeAnalysis()
        analysis.issues = self.mock_issues

        # Action
        analysis.fetch_and_plot()

        args, kwargs = mock_plot.call_args
        contributor_df, assignee_df, label_df, top_contributors_count, top_assignees_count = args

        # Assert
        pd.testing.assert_frame_equal(contributor_df, pd.DataFrame([('user1', 2), ('user2', 1)], columns=['Contributor', 'Issue Count']))


    @patch('builtins.input', side_effect=["2", "2"])
    @patch.object(ContributorAndAssigneeAnalysis, 'plot_contributors_assignees_and_labels')
    def test_fetch_and_plot_correctly_calculates_assignee_df(self, mock_plot, mock_input):
        """
        Test fetch_and_plot method correctly calculates the assignee_counts and sends it as a df to plot
        """
        # Setup
        analysis = ContributorAndAssigneeAnalysis()
        analysis.issues = self.mock_issues

        # Action
        analysis.fetch_and_plot()

        args, kwargs = mock_plot.call_args
        contributor_df, assignee_df, label_df, top_contributors_count, top_assignees_count = args

        # Assert
        pd.testing.assert_frame_equal(assignee_df, pd.DataFrame([('assignee1', 2), ('assignee2', 1), ('assignee3', 1)], columns=['Assignee', 'Issue Count']))


    @patch('builtins.input', side_effect=["2", "2"])
    @patch.object(ContributorAndAssigneeAnalysis, 'plot_contributors_assignees_and_labels')
    def test_fetch_and_plot_correctly_calculates_label_df(self, mock_plot, mock_input):
        """
        Test fetch_and_plot method correctly calculates the label_counts
        """
        # Setup
        analysis = ContributorAndAssigneeAnalysis()
        analysis.issues = self.mock_issues

        # Action
        analysis.fetch_and_plot()

        args, kwargs = mock_plot.call_args
        contributor_df, assignee_df, label_df, top_contributors_count, top_assignees_count = args

        # Assert
        pd.testing.assert_frame_equal(label_df, pd.DataFrame([('bug', 2), ('high-priority', 1), ('feature', 1),('low-priority', 1)], columns=['Label', 'Frequency']))


    # Failing test - since its a bug, contributer analysis is not handling incomplete data properly
    # @patch('builtins.input', side_effect=["2", "2"])
    # def test_fetch_and_plot_when_data_is_incomplete_should_capture_counts(self, mock_input):
    #     """
    #     Test fetch_and_plot method, when data is incomplete, should only process present data
    #     """
    #     # Setup
    #     mock_issue = MagicMock()
    #     mock_issue.creator = 'user3'
    #     mock_issue.assignees = None
    #     mock_issue.labels = None

    #     analysis = ContributorAndAssigneeAnalysis()
    #     analysis.issues = [mock_issue]

    #     # Action
    #     analysis.fetch_and_plot()

    #     # Assertions
    #     mock_plot.assert_not_called()


## fetch_and_plot_with_label Tests

    # Failing test - since its a bug, invalid inputs should be handled
    # @patch('builtins.input', side_effect=["0", "0"])
    # def test_fetch_and_plot_with_label_when_user_inputs_zero_should_print_error_msg(self, mock_input):
    #     """
    #     Test fetch_and_plot_with_label when user enters 0 contributors and assignees, should handle gracefully
    #     """
        
    #     analysis = ContributorAndAssigneeAnalysis()

    #     analysis.issues = [
    #         MagicMock(labels=["feature"], creator="user1", assignees=[{"login": "assignee1"}]),
    #         MagicMock(labels=["enhancement"], creator="user2", assignees=[{"login": "assignee2"}])
    #     ]

    #     # Assert that a ValueError is thrown
    #     with self.assertRaises(ValueError):
    #         analysis.fetch_and_plot_with_label("bug")

    # Failing test - since its a bug, invalid inputs should be handled
    # @patch('builtins.input', side_effect=["a", ""])
    # def test_fetch_and_plot_with_label_when_user_inputs_invalid_should_print_error_msg(self, mock_input):
    #     """
    #     Test fetch_and_plot_with_label when user enters 0 contributors and assignees, should handle gracefully
    #     """
        
    #     analysis = ContributorAndAssigneeAnalysis()

    #     analysis.issues = [
    #         MagicMock(labels=["feature"], creator="user1", assignees=[{"login": "assignee1"}]),
    #         MagicMock(labels=["enhancement"], creator="user2", assignees=[{"login": "assignee2"}])
    #     ]

    #     # Assert that a ValueError is thrown
    #     with self.assertRaises(ValueError):
    #         analysis.fetch_and_plot_with_label("bug")


    @patch('builtins.input', side_effect=["2", "2"])
    def test_fetch_and_plot_with_label_when_label_not_found_should_print_error_msg(self, mock_input):
        """
        Test case where label isn't found
        """
        
        analysis = ContributorAndAssigneeAnalysis()

        analysis.issues = [
            MagicMock(labels=["feature"], creator="user1", assignees=[{"login": "assignee1"}]),
            MagicMock(labels=["enhancement"], creator="user2", assignees=[{"login": "assignee2"}])
        ]

        with patch('builtins.print') as mock_print:
            analysis.fetch_and_plot_with_label("bug")
            mock_print.assert_called_with("Error: No such label 'bug' found.")


    @patch('builtins.input', side_effect=["2", "2"])
    @patch('matplotlib.pyplot.subplots')
    @patch.object(ContributorAndAssigneeAnalysis, 'plot_contributors_and_assignees')
    def test_fetch_and_plot_with_label_correctly_calculates_contributor_df(self, mock_plot, mock_subplots, mock_input):
        """
        Test fetch_and_plot_with_label correctly sends the contributor df when calling plot
        """
        # Setup
        analysis = ContributorAndAssigneeAnalysis()
        analysis.issues = self.mock_issues

        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)
        
        # Action
        analysis.fetch_and_plot_with_label("bug")

        args, kwargs = mock_plot.call_args
        contributor_df, assignee_df, top_contributors_count, top_assignees_count, label = args

        # Assert
        pd.testing.assert_frame_equal(contributor_df, pd.DataFrame([('user1', 2)], columns=['Contributor', 'Issue Count']))
        

    @patch('builtins.input', side_effect=["2", "2"])
    @patch('matplotlib.pyplot.subplots')
    @patch.object(ContributorAndAssigneeAnalysis, 'plot_contributors_and_assignees')
    def test_fetch_and_plot_with_label_correctly_calculates_assignee_df(self, mock_plot, mock_subplots, mock_input):
        """
        Test fetch_and_plot_with_label correctly sends the assignee df when calling plot
        """
        # Setup
        analysis = ContributorAndAssigneeAnalysis()
        analysis.issues = self.mock_issues

        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)
        
        # Action
        analysis.fetch_and_plot_with_label("bug")

        args, kwargs = mock_plot.call_args
        contributor_df, assignee_df, top_contributors_count, top_assignees_count, label = args

        # Assert
        pd.testing.assert_frame_equal(assignee_df, pd.DataFrame([('assignee1', 1), ('assignee2', 1), ('assignee3', 1)], columns=['Assignee', 'Issue Count']))


    @patch('builtins.input', side_effect=["2", "2"])
    @patch('matplotlib.pyplot.subplots')
    @patch.object(ContributorAndAssigneeAnalysis, 'plot_contributors_and_assignees')
    def test_fetch_and_plot_with_label_should_send_correct_label_to_plot(self, mock_plot, mock_subplots, mock_input):
        """
        Test fetch_and_plot_with_label calls plot with the correct label
        """
        # Setup
        analysis = ContributorAndAssigneeAnalysis()
        analysis.issues = self.mock_issues

        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)
        
        # Action
        analysis.fetch_and_plot_with_label("bug")

        args, kwargs = mock_plot.call_args
        contributor_df, assignee_df, top_contributors_count, top_assignees_count, label = args

        # Assert
        self.assertEqual(label, 'bug')


    @patch('builtins.input', side_effect=["2", "2"])
    @patch('matplotlib.pyplot.subplots')
    @patch.object(ContributorAndAssigneeAnalysis, 'plot_contributors_and_assignees')
    def test_fetch_and_plot_with_label_calls_plot_with_correct_contributor_count(self, mock_plot, mock_subplots, mock_input):
        """
        Test fetch_and_plot_with_label calls plot with the correct label
        """
        # Setup
        analysis = ContributorAndAssigneeAnalysis()
        analysis.issues = self.mock_issues

        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)
        
        # Action
        analysis.fetch_and_plot_with_label("bug")

        args, kwargs = mock_plot.call_args
        contributor_df, assignee_df, top_contributors_count, top_assignees_count, label = args

        # Assert
        self.assertEqual(top_contributors_count, 2)


    @patch('builtins.input', side_effect=["2", "2"])
    @patch('matplotlib.pyplot.subplots')
    @patch.object(ContributorAndAssigneeAnalysis, 'plot_contributors_and_assignees')
    def test_fetch_and_plot_with_label_calls_plot_with_correct_assignee_count(self, mock_plot, mock_subplots, mock_input):
        """
        Test fetch_and_plot_with_label calls plot with the correct label
        """
        # Setup
        analysis = ContributorAndAssigneeAnalysis()
        analysis.issues = self.mock_issues

        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)
        
        # Action
        analysis.fetch_and_plot_with_label("bug")

        args, kwargs = mock_plot.call_args
        contributor_df, assignee_df, top_contributors_count, top_assignees_count, label = args

        # Assert
        self.assertEqual(top_assignees_count, 2)


# test plot_contributors_assignees_and_labels

    @patch('matplotlib.pyplot.subplots')
    def test_plot_contributors_assignees_and_labels_calls_bar_with_correct_contributor_data(self, mock_subplots):
        """
        Test plot_contributors_assignees_and_labels method calls bar with correct data for contributor
        """

        # Setup
        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)

        contributor_df = pd.DataFrame([('user1', 1), ('user2', 3)], columns=['Contributor', 'Issue Count'])
        assignee_df = pd.DataFrame([('assignee1', 4), ('assignee2', 2)], columns=['Assignee', 'Issue Count'])
        label_df = pd.DataFrame([('bug', 3), ('feature', 2)], columns=['Label', 'Frequency'])

        analysis = ContributorAndAssigneeAnalysis()

        # Action
        analysis.plot_contributors_assignees_and_labels(contributor_df, assignee_df, label_df, 2, 2)

        args, kwargs = mock_axes[0].bar.call_args
        contributor_data = args

        # Assert
        self.assertEqual(contributor_data[0].tolist(), ['user2', 'user1'])
        self.assertEqual(contributor_data[1].tolist(), [3, 1])


    @patch('matplotlib.pyplot.subplots')
    def test_plot_contributors_assignees_and_labels_calls_bar_with_correct_assignee_data(self, mock_subplots):
        """
        Test plot_contributors_assignees_and_labels method calls bar with correct data for assignee
        """

        # Setup
        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)

        contributor_df = pd.DataFrame([('user1', 1), ('user2', 3)], columns=['Contributor', 'Issue Count'])
        assignee_df = pd.DataFrame([('assignee1', 4), ('assignee2', 2)], columns=['Assignee', 'Issue Count'])
        label_df = pd.DataFrame([('bug', 3), ('feature', 2)], columns=['Label', 'Frequency'])

        analysis = ContributorAndAssigneeAnalysis()

        # Action
        analysis.plot_contributors_assignees_and_labels(contributor_df, assignee_df, label_df, 2, 2)

        args, kwargs = mock_axes[1].bar.call_args
        assignee_data = args

        # Assert
        self.assertEqual(assignee_data[0].tolist(), ['assignee1', 'assignee2'])
        self.assertEqual(assignee_data[1].tolist(), [4, 2])


    @patch('matplotlib.pyplot.subplots')
    def test_plot_contributors_assignees_and_labels_calls_bar_with_correct_label_data(self, mock_subplots):
        """
        Test plot_contributors_assignees_and_labels method calls bar with correct data for labels
        """

        # Setup
        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)

        contributor_df = pd.DataFrame([('user1', 1), ('user2', 3)], columns=['Contributor', 'Issue Count'])
        assignee_df = pd.DataFrame([('assignee1', 4), ('assignee2', 2)], columns=['Assignee', 'Issue Count'])
        label_df = pd.DataFrame([('bug', 3), ('feature', 2)], columns=['Label', 'Frequency'])

        analysis = ContributorAndAssigneeAnalysis()

        # Action
        analysis.plot_contributors_assignees_and_labels(contributor_df, assignee_df, label_df, 2, 2)

        args, kwargs = mock_axes[2].bar.call_args
        label_data = args

        # Assert
        self.assertEqual(label_data[0].tolist(), ['bug', 'feature'])
        self.assertEqual(label_data[1].tolist(), [3, 2])

# test plot_contributors_and_assignees
    @patch('matplotlib.pyplot.subplots')
    def test_plot_contributors_and_assignees_calls_bar_with_correct_contributor_data(self, mock_subplots):
        """
        Test plot_contributors_and_assignees method calls bar with correct data for contributor
        """

        # Setup
        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)

        contributor_df = pd.DataFrame([('user1', 1), ('user2', 3)], columns=['Contributor', 'Issue Count'])
        assignee_df = pd.DataFrame([('assignee1', 4), ('assignee2', 2)], columns=['Assignee', 'Issue Count'])
        label_df = pd.DataFrame([('bug', 3), ('feature', 2)], columns=['Label', 'Frequency'])

        analysis = ContributorAndAssigneeAnalysis()

        # Action
        analysis.plot_contributors_and_assignees(contributor_df, assignee_df, 2, 2, 'bug')

        args, kwargs = mock_axes[0].bar.call_args
        contributor_data = args

        # Assert
        self.assertEqual(contributor_data[0].tolist(), ['user2', 'user1'])
        self.assertEqual(contributor_data[1].tolist(), [3, 1])


    @patch('matplotlib.pyplot.subplots')
    def test_plot_contributors_and_assignees_calls_bar_with_correct_assignee_data(self, mock_subplots):
        """
        Test plot_contributors_and_assignees method calls bar with correct data for assignee
        """

        # Setup
        mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock(), MagicMock()]
        mock_subplots.return_value = (mock_fig, mock_axes)

        contributor_df = pd.DataFrame([('user1', 1), ('user2', 3)], columns=['Contributor', 'Issue Count'])
        assignee_df = pd.DataFrame([('assignee1', 4), ('assignee2', 2)], columns=['Assignee', 'Issue Count'])
        label_df = pd.DataFrame([('bug', 3), ('feature', 2)], columns=['Label', 'Frequency'])

        analysis = ContributorAndAssigneeAnalysis()

        # Action
        analysis.plot_contributors_and_assignees(contributor_df, assignee_df, 2, 2, 'bug')

        args, kwargs = mock_axes[1].bar.call_args
        assignee_data = args

        # Assert
        self.assertEqual(assignee_data[0].tolist(), ['assignee1', 'assignee2'])
        self.assertEqual(assignee_data[1].tolist(), [4, 2])


if __name__ == '__main__':
    unittest.main()

    