import logging
import traceback
import os
import pandas as pd
from functools import wraps


# noinspection PyArgumentList,PyCallingNonCallable
class CustomLogging(logging.Logger):
    def __init__(self, log_dir, name=__name__, level=logging.DEBUG):
        super(CustomLogging, self).__init__(name=name)

        # --- SET UP LOGGING ---
        formatter = logging.Formatter("%(asctime)s - %(process)d - %(levelname)s - %(module)s.%(funcName)s - %(message)s")
        file_handler = logging.FileHandler(os.path.realpath(os.path.join(log_dir, "log.log")), encoding="utf-8")
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.setLevel(level)
        self.addHandler(file_handler)
        self.addHandler(console_handler)

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

    def error(self, msg, *args, **kwargs):
        if not self._is_level_allowed(level=logging.ERROR):
            return None

        self._log(logging.ERROR, msg, args, **kwargs)
        self._collect_level_statistics(level=logging.ERROR)

    def warning(self, msg, *args, **kwargs):
        if not self._is_level_allowed(level=logging.WARNING):
            return None

        self._log(logging.WARNING, msg, args, **kwargs)
        self._collect_level_statistics(level=logging.WARNING)

    def log_exception(self):
        if not self._is_level_allowed(level=logging.ERROR):
            return None

        self._log(logging.ERROR, "Stack...\n%s" % traceback.format_exc(), None)
        self._collect_level_statistics(level=logging.ERROR)

    def log_dataframe(self, df, msg="", level="INFO"):
        level = eval("logging." + level.upper())
        if not self._is_level_allowed(level=level):
            return None

        if not self._is_dataframe(df=df):
            return None

        self._log(level, msg + "\n" + df.to_string(), None)
        self._collect_level_statistics(level=level)

    def dataframe_head_tail(self, df, n=5, h=None, t=None, msg="", level="INFO"):
        """
        Logs the head and tail of a dataframe.

        :param df:     input dataframe
        :param n:      default number of rows in both head and tail; default is 5
        :param h:      number of rows in the head, overwrites n
        :param t:      number of rows in the tail, overwrites n
        :param msg:    log message; default is no message (empty string)
        :param level:  log level; default is INFO
        :param args:
        :return:       log level for level counting purposes
        """
        level = eval("logging." + level.upper())
        if not self._is_level_allowed(level=level):
            return None

        if not self._is_dataframe(df=df):
            return None

        head = df.head(h) if h else df.head(n)
        tail = df.tail(t) if t else df.tail(n)
        self._log(level, msg + "\nHEAD\n" + head.to_string() + "\nTAIL\n" + tail.to_string(), None)
        self._collect_level_statistics(level=level)

    def warn_duplicate_values(self, df, subset=None, msg="", keep=False):
        if not self._is_level_allowed(level=logging.WARNING):
            return None

        if not self._is_dataframe(df=df):
            return None

        df = df[df.duplicated(subset=subset, keep=keep)]
        if not df.empty:
            self._log(logging.WARNING, msg + "\n" + df.to_string(), None)
            self._collect_level_statistics(level=logging.WARNING)

    def warn_missing_values(self, df, msg=""):
        if not self._is_level_allowed(level=logging.WARNING):
            return None

        if not self._is_dataframe(df=df):
            return None

        if df.isnull().any().any():
            self._log(logging.WARNING, msg + "\n" + df[df.isnull().any(axis=1)].to_string(), None)
            self._collect_level_statistics(level=logging.WARNING)

    def get_error_count(self):
        self._log(logging.INFO, "TOTAL ERRORS: {}".format(self.error_count), None)

    def get_warning_count(self):
        self._log(logging.INFO, "TOTAL WARNINGS: {}".format(self.warn_count), None)
