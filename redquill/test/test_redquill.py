# Copyright 2017 Vincent Chen. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# STANDARD LIB
import logging
import pandas as pd
import pytest

# PROJECT LIB
import redquill as rq


@pytest.fixture(scope="class")
def log():
    return rq.RedQuill()


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
        log.log_dataframe_head_tail(df=data)

    def test_warn_duplicate_values(self, log):
        df = pd.DataFrame({"A": [1, 2, None, 3],
                           "B": [4, 2, 2, 5]})
        log.warn_duplicate_values(df=df, subset="B", msg="Duplicates on B.")
        log.warn_duplicate_values(df=df, msg="No subset.")

    def test_warn_null_values(self, log):
        df = pd.DataFrame({"A": [1, 2, None, 3],
                           "B": [4, 2, 2, 5]})
        log.warn_null_values(df=df)

    def test_get_error_count(self, log):
        assert log.get_error_count() == 1

    def test_get_warn_count(self, log):
        assert log.get_warning_count() == 2


@pytest.mark.parametrize("log_dir, name, level", [
    # no log dir, no log name
    pytest.param(None, None, logging.INFO),

    # no log dir, log name
    pytest.param(None, "log_file.log", logging.INFO),

    # custom log level not supported
    pytest.param(None, "log_file.log", "TEST", marks=pytest.mark.xfail),
])
def test_initialize_logger(log_dir, name, level):
    rq.initialize_logger(log_dir, name, level)
