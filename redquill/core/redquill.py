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

"""A custom logging library with pandas supported methods

"""

# STANDARD LIB
import sys
import warnings
import logging
import os
import pandas as pd

LOG_NAME = "log.log"  # default log name


# noinspection PyArgumentList,PyCallingNonCallable
class RedQuill(logging.Logger):
    """Main logging class.

    An instance of RedQuill is supposed to behave like a logger instance
    from the logging module.

    """

    def __init__(self, log_dir=None, name=LOG_NAME, level=logging.NOTSET):
        super(RedQuill, self).__init__(name=name)

        # --- SET UP LOGGING ---
        formatter = logging.Formatter("%(asctime)s - "
                                      "%(process)d - "
                                      "%(levelname)s - "
                                      "%(module)s.%(funcName)s - "
                                      "%(message)s")
        sys.excepthook = self.log_exception

        # --- SET UP HANDLERS ---
        if log_dir is not None:
            file_handler = logging.FileHandler(os.path.realpath(os.path.join(
                log_dir, name)), encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)
        else:
            print("NO LOG DIRECTORY was specified... only log to console.")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        # --- SET UP LEVEL ---
        self.setLevel(level)

        # --- SET UP COUNTERS ---
        self.error_count = 0
        self.warn_count = 0

    def _collect_level_statistics(self, level):
        if level == logging.ERROR:
            self.error_count += 1
        elif level == logging.WARNING:
            self.warn_count += 1

    def _is_level_allowed(self, level):
        return self.level <= level

    def _is_dataframe(self, df):
        if df.__class__ == pd.DataFrame:
            ret = True
        else:
            self._log(logging.ERROR, "no dataframe was passed in...", None)
            ret = False
        return ret

    def info(self, msg, *args, **kwargs):
        if not self._is_level_allowed(level=logging.INFO):
            return

        self._log(logging.INFO, msg, args, kwargs)

    def error(self, msg, *args, **kwargs):
        if not self._is_level_allowed(level=logging.ERROR):
            return

        self._log(logging.ERROR, msg, args, kwargs)
        self._collect_level_statistics(level=logging.ERROR)

    def warning(self, msg, *args, **kwargs):
        if not self._is_level_allowed(level=logging.WARNING):
            return

        self._log(logging.WARNING, msg, args, kwargs)
        self._collect_level_statistics(level=logging.WARNING)

    def warn(self, msg, *args, **kwargs):
        if not self._is_level_allowed(level=logging.WARNING):
            return

        self._log(logging.WARNING, msg, args, kwargs)
        self._collect_level_statistics(level=logging.WARNING)

    def log_exception(self, type, value, traceback):
        if not self._is_level_allowed(level=logging.ERROR):
            return

        self._log(logging.ERROR, "Uncaught exception.", args=None,
                  exc_info=(type, value, traceback))
        self._collect_level_statistics(level=logging.ERROR)

    def log_dataframe(self, df, n=10, msg="", level="INFO"):
        """Logs a pandas dataframe.

        The default only logs the first 10 rows, since the dataframe can be
        potentially large.

        Args:
            df (pd.DataFrame): Input dataframe.
            n (int): Number of rows to log.
            msg (str): Log message.
            level (str): Log level name; default is "INFO".

        Returns:
            void
        """
        level = eval("logging." + level.upper())
        if not self._is_level_allowed(level=level):
            return

        if not self._is_dataframe(df=df):
            return

        self._log(level, msg + "\n" + df.head(n).to_string(), None)
        self._collect_level_statistics(level=level)

    def log_dataframe_head_tail(self, df, n=5, msg="", level="INFO"):
        """Logs the top and bottom n rows of a dataframe.

        Args:
            df (pd.DataFrame): Input dataframe.
            n (int): Number of rows in both head and tail; default is 5.
            msg (str): Log message; default is no message (empty string).
            level (str): Log level name; default is "INFO".

        Returns:
            void
        """
        level = eval("logging." + level.upper())
        if not self._is_level_allowed(level=level):
            return

        if not self._is_dataframe(df=df):
            return

        head = df.head(n)
        tail = df.tail(n)
        self._log(level, msg + "\nHEAD\n" + head.to_string() +
                  "\nTAIL\n" + tail.to_string(), None)
        self._collect_level_statistics(level=level)

    def warn_duplicate_values(self, df, subset=None, msg=""):
        """Warn on duplicate data frame records.

        Args:
            df (pd.DataFrame): A pandas data frame.
            subset (str or list-like of str): The subset of columns to
                check for duplicates against.
            msg (str): Optional log message.

        Returns:
            void
        """
        if not self._is_level_allowed(level=logging.WARNING):
            return

        if not self._is_dataframe(df=df):
            return

        df = df[df.duplicated(subset=subset, keep=False)]
        if not df.empty:
            self._log(logging.WARNING, msg + "\n" + df.to_string(), None)
            self._collect_level_statistics(level=logging.WARNING)

    def warn_null_values(self, df, msg=""):
        """Warn on NULL data frame values.

        Args:
            df (pd.DataFrame): A pandas data frame.
            msg (str): Optional log message.

        Returns:
            void
        """
        if not self._is_level_allowed(level=logging.WARNING):
            return

        if not self._is_dataframe(df=df):
            return

        if df.isnull().any().any():
            self._log(logging.WARNING, msg + "\n" +
                      df[df.isnull().any(axis=1)].to_string(), None)
            self._collect_level_statistics(level=logging.WARNING)

    def get_error_count(self):
        """Get number of errors logged.

        Returns:
            anonymous (int): Total number of errors so far.
        """
        return self.error_count

    def get_warning_count(self):
        """Get number of warnings logged.

        Returns:
            anonymous (int): Total number of warnings so far.
        """
        return self.warn_count

    def log_error_count(self):
        """Log the total number of errors so far.

        """
        self._log(logging.INFO, f"TOTAL ERRORS: {self.error_count}", None)

    def log_warning_count(self):
        """Log the total number of warnings so far.

        """
        self._log(logging.INFO, f"TOTAL WARNINGS: {self.warn_count}", None)


def initialize_logger(log_dir=None, name=None, level=logging.NOTSET):
    """API to construct RedQuill instance.

    Args:
        log_dir (str): Root directory of the log file.
        name (str): Basename of the log file with extension,
            e.g. "log_file.log".
        level (int): Log level value, e.g. logging.INFO, logging.DEBUG, etc.

    Returns:
        anonymous (RedQuill): Returns a RedQuill instance.
    """
    if log_dir is None:
        warnings.warn("log_dir is None, no log file will be generated.")

    if name is None:
        warnings.warn(f"Log name is not specified, setting to default "
                      f"log name: {LOG_NAME}.")
        name = LOG_NAME

    if level not in logging._levelToName:
        raise ValueError("Custom levels not supported at this time.")

    return RedQuill(log_dir=log_dir, name=name, level=level)
