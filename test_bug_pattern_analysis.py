import unittest
from io import StringIO
from unittest.mock import patch, Mock

import warnings
warnings.simplefilter("ignore", category=UserWarning)

import matplotlib as plt
plt.use("Agg")  # Non-interactive backend 

from features.bug_pattern_analysis import BugPatternsAnalysis


class TestBugPatternAnalysis(unittest.TestCase):

    def setUp(self):
        self.analysis = BugPatternsAnalysis()

    @patch("sys.stdout", new_callable=StringIO)
    def test_user_failure(self, mock_stdout):
        """
        Check that an invalid user prints the error.
        """
        # Create BugPatternsAnalysis object/user and plot
        user:str = "NotARealUser"
        self.analysis.user = user
        self.analysis.fetch_and_plot()

        # Ensure printed output has the analysis's failure
        output = mock_stdout.getvalue()
        self.assertIn(f"No bug patterns found for creator '{user}'.", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("matplotlib.pyplot.show")
    def test_plot_once(self, mock_show, _):
        """
        Check show is called only once
        """
        self.analysis.fetch_and_plot()
        mock_show.assert_called_once()

if __name__ == "__main__":
    unittest.main()
