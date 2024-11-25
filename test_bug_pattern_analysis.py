# import unittest
# from unittest.mock import patch
# from io import StringIO
# import os
# import copy

# from features.bug_pattern_analysis import BugPatternsAnalysis
# from data_loader import DataLoader
# from model import Issue


# class TestBugPatternAnalysis(unittest.TestCase):

#     def setUp(self):
#         pass


#     ##########
#     ### Ensure fetch_and_plot() calls analyze_bug_patterns_for_creator() and no bugs are found for an invalid user.
#     ##########

#     @patch("sys.stdout", new_callable=StringIO)
#     def test_user_failure(self, mock_stdout):
#         """
#         Check that an invalid user prints the error.
#         """
#         analysis = BugPatternsAnalysis()
#         user:str = "NotARealUser"
#         analysis.user = user
#         analysis.fetch_and_plot()

#         # Ensure printed output has the analysis's failure
#         self.assertIn(f"No bug patterns found for creator '{user}'.", mock_stdout.getvalue())


#     ##########
#     ### Test the user can be parsed from the environment
#     ##########

#     @patch("sys.stdout", new_callable=StringIO)
#     def test_environment_user(self, _):
#         user:str = "json:SomeUser"
#         os.environ["user"] = user
#         analysis = BugPatternsAnalysis()
#         self.assertEqual(f"json:{analysis.user}", user)

#         # Cleanup
#         os.environ.pop("user", None)


#     ##########
#     ### Test plots: Ensure functions succeed and show() is called once
#     ##########
    
#     @patch("sys.stdout", new_callable=StringIO)
#     @patch("matplotlib.pyplot.show")
#     def test_general_plot(self, mock_show, _):
#         """
#         Check function succeeds and show() is called once
#         """
#         analysis = BugPatternsAnalysis()
#         analysis.user = ""
#         analysis.fetch_and_plot()
#         mock_show.assert_called_once()
    
#     @patch("sys.stdout", new_callable=StringIO)
#     @patch("matplotlib.pyplot.show")
#     def test_creator_plot(self, mock_show, _):
#         """
#         Check function succeeds and show() is called once
#         """
#         analysis = BugPatternsAnalysis()
#         analysis.user = "tigerhawkvok"
#         analysis.fetch_and_plot()
#         mock_show.assert_called_once()


#     ##########
#     ### Empty issues: Ensure functions fail with proper message if an empty issue list is supplied
#     ##########

#     @patch("sys.stdout", new_callable=StringIO)
#     def test_general_no_issues(self, mock_stdout):
#         issues:list = []
#         analysis = BugPatternsAnalysis()
#         analysis.analyze_general_bug_patterns(issues)
#         self.assertIn("No bug patterns found.", mock_stdout.getvalue())

#     @patch("sys.stdout", new_callable=StringIO)
#     def test_no_issues_creator(self, mock_stdout):
#         issues:list = []
#         user:str = "tigerhawkvok"
#         analysis = BugPatternsAnalysis()
#         analysis.user = user
#         analysis.analyze_bug_patterns_for_creator(issues)
#         self.assertIn(f"No bug patterns found for creator '{user}'.", mock_stdout.getvalue())
    

#     ##########
#     ### None issues: Ensure functions fail if an issues list (or title fields) contains an issue with undeclared fields
#     ##########

#     @patch("sys.stdout", new_callable=StringIO)
#     def test_general_none_issue(self, _):
#         issues:list = [Issue()]
#         analysis = BugPatternsAnalysis()
#         try:
#             analysis.analyze_general_bug_patterns(issues)
#         except TypeError as e:
#             self.fail(f"BugPatternsAnalysis().analyze_general_bug_patterns() failed with: {e}")

#     @patch("sys.stdout", new_callable=StringIO)
#     def test_creator_none_issue(self, _):
#         issues:list = [Issue()]
#         analysis = BugPatternsAnalysis()
#         analysis.user = None
#         try:
#             analysis.analyze_bug_patterns_for_creator(issues)
#         except TypeError as e:
#             self.fail(f"BugPatternsAnalysis().analyze_bug_patterns_for_creator() failed with: {e}")


#     ##########
#     ### None titles: Ensure functions fail if an issues title is None
#     ##########

#     @patch("sys.stdout", new_callable=StringIO)
#     def test_general_none_title(self, _):
#         global_issues = DataLoader().get_issues()
#         issue_index:int = 10
#         issue = copy.deepcopy(global_issues[issue_index])
#         issue.title = None

#         issues:list[Issue] = [issue]
#         analysis = BugPatternsAnalysis()
#         try:
#             analysis.analyze_general_bug_patterns(issues)
#         except TypeError as e:
#             self.fail(f"BugPatternsAnalysis().analyze_general_bug_patterns() failed with: {e}")

#     @patch("sys.stdout", new_callable=StringIO)
#     def test_creator_none_title(self, _):
#         global_issues = DataLoader().get_issues()
#         issue_index:int = 20
#         issue = copy.deepcopy(global_issues[issue_index])
#         issue.title = None

#         issues:list[Issue] = [issue]
#         analysis = BugPatternsAnalysis()
#         analysis.user = issue.creator
#         try:
#             analysis.analyze_bug_patterns_for_creator(issues)
#         except TypeError as e:
#             self.fail(f"BugPatternsAnalysis().analyze_bug_patterns_for_creator() failed with: {e}")


# if __name__ == "__main__":
#     unittest.main()
