# Copyright 2018 Vincent Chen. All Rights Reserved.
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
import logging
import os
import pandas as pd
import sys


# noinspection PyArgumentList,PyCallingNonCallable
class CustomLogging(logging.Logger):
    def __init__(self, log_dir=None, name="log.log", level=logging.NOTSET):
        super(CustomLogging, self).__init__(name=name)

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
            return True
        else:
            self._log(logging.ERROR, "no dataframe was passed in...", None)
            return False

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
        """This functions logs the dataframe.

        The default only logs the first 10 rows, since the dataframe can be
        potentially large.

        Args:
            df (dataframe): Input dataframe.
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

    def dataframe_head_tail(self, df, n=5, h=None, t=None, msg="",
                            level="INFO"):
        """This function logs the head and tail of a dataframe.

        Args:
            df (dataframe): Input dataframe.
            n (int): Number of rows in both head and tail; default is 5.
            h (int): Number of rows in the head, overwrites n.
            t (int): Number of rows in the tail, overwrites n.
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

        head = df.head(h) if h else df.head(n)
        tail = df.tail(t) if t else df.tail(n)
        self._log(level, msg + "\nHEAD\n" + head.to_string() +
                  "\nTAIL\n" + tail.to_string(), None)
        self._collect_level_statistics(level=level)

    def warn_duplicate_values(self, df, subset=None, msg="", keep=False):
        if not self._is_level_allowed(level=logging.WARNING):
            return

        if not self._is_dataframe(df=df):
            return

        df = df[df.duplicated(subset=subset, keep=keep)]
        if not df.empty:
            self._log(logging.WARNING, msg + "\n" + df.to_string(), None)
            self._collect_level_statistics(level=logging.WARNING)

    def warn_null_values(self, df, msg=""):
        if not self._is_level_allowed(level=logging.WARNING):
            return

        if not self._is_dataframe(df=df):
            return

        if df.isnull().any().any():
            self._log(logging.WARNING, msg + "\n" +
                      df[df.isnull().any(axis=1)].to_string(), None)
            self._collect_level_statistics(level=logging.WARNING)

    def get_error_count(self):
        return self.error_count

    def get_warning_count(self):
        return self.warn_count

    def log_error_count(self):
        self._log(logging.INFO, "TOTAL ERRORS: {}".format(self.error_count),
                  None)

    def log_warning_count(self):
        self._log(logging.INFO, "TOTAL WARNINGS: {}".format(self.warn_count),
                  None)
