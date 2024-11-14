from typing import Any
from unittest.mock import mock_open, patch

import pandas as pd

from src.reports import recording_data


@patch("builtins.open", new_callable=mock_open)
def test_recording_data_decorator(mock_file: Any):
    test_data = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})

    @recording_data("test_report.json")
    def function():
        return test_data

    returned_value = function()

    pd.testing.assert_frame_equal(returned_value, test_data)