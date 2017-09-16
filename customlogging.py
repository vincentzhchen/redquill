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

    def _level_counter(func):
        @wraps(func)
        def wrapper(self, *arg, **kwargs):
            level = func(self, *arg, **kwargs)
            if level == logging.ERROR:
                self.error_count += 1
            elif level == logging.WARNING:
                self.warn_count += 1
        return wrapper

    def _is_level_allowed(self, level):
        return self.level <= level

    @_level_counter
    def error(self, msg, *args, **kwargs):
        if not self._is_level_allowed(level=logging.ERROR):
            return None

        self._log(logging.ERROR, msg, args, **kwargs)
        return logging.ERROR

    @_level_counter
    def warning(self, msg, *args, **kwargs):
        if not self._is_level_allowed(level=logging.WARNING):
            return None

        self._log(logging.WARNING, msg, args, **kwargs)
        return logging.WARNING

    @_level_counter
    def log_exception(self, *args):
        if not self._is_level_allowed(level=logging.ERROR):
            return None

        self._log(logging.ERROR, "Stack...\n%s" % traceback.format_exc(), args)
        return logging.ERROR

    @_level_counter
    def log_dataframe(self, df, msg="", level="INFO", *args):
        level = eval("logging." + level.upper())
        if not self._is_level_allowed(level=level):
            return None

        if df.__class__ == pd.DataFrame:
            self._log(level, msg + "\n" + df.to_string(), args)
        else:
            self._log(logging.ERROR, "no dataframe was passed in...", args)
        return level

    @_level_counter
    def dataframe_head_tail(self, df, n=5, msg="", level="INFO", *args):
        level = eval("logging." + level.upper())
        if not self._is_level_allowed(level=level):
            return None

        if df.__class__ == pd.DataFrame:
            df = pd.concat([df.head(n), df.tail(n)])
            self._log(level, msg + "\n" + df.to_string(), args)
        else:
            self._log(logging.ERROR, "no dataframe was passed in...", args)
        return level

    def get_error_count(self, *args):
        self._log(logging.INFO, "TOTAL ERRORS: {}".format(self.error_count), args)

    def get_warning_count(self, *args):
        self._log(logging.INFO, "TOTAL WARNINGS: {}".format(self.warn_count), args)
