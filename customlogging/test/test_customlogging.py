import pandas as pd
import pytest
import customlogging as cl


@pytest.fixture(scope="class")
def log():
    return cl.CustomLogging()


@pytest.mark.usefixtures("log")
class TestStandardLogging(object):
    def test_info(self, log):
        log.info("This is an info message.")

    def test_error(self, log):
        log.error("This is an error message.")

    def test_warning(self, log):
        log.warn("This is a warning message.")
        log.warning("This is a warning message.")

    def test_get_error_count(self, log):
        assert log.get_error_count() == 1

    def test_get_warn_count(self, log):
        assert log.get_warning_count() == 2


@pytest.mark.usefixtures("log")
class TestDataFrameLogging(object):
    @pytest.fixture(autouse=True)
    def data(self):
        df = pd.DataFrame({"A": range(0, 20),
                           "B": range(20, 40)})
        return df

    def test_log_dataframe_info(self, log, data):
        log.log_dataframe(df=data.head(1), msg="Test df info.")

    def test_log_dataframe_error(self, log, data):
        log.log_dataframe(df=data.head(1), msg="Test df error.", level="ERROR")

    def test_dataframe_head_tail(self, log, data):
        log.dataframe_head_tail(df=data)

    def test_warn_duplicate_values(self, log):
        df = pd.DataFrame({"A": [1, 2, None, 3],
                           "B": [4, 2, 2, 5]})
        log.warn_duplicate_values(df=df, subset="B", msg="Duplicates on B.")

    def test_warn_null_values(self, log):
        df = pd.DataFrame({"A": [1, 2, None, 3],
                           "B": [4, 2, 2, 5]})
        log.warn_null_values(df=df)

    def test_get_error_count(self, log):
        assert log.get_error_count() == 1

    def test_get_warn_count(self, log):
        assert log.get_warning_count() == 2