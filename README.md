# redquill
[![PyPI version shields.io](https://img.shields.io/pypi/v/redquill.svg)](https://pypi.org/project/redquill/)
[![Build Status](https://travis-ci.org/vincentzhchen/redquill.png?branch=master)](https://travis-ci.org/vincentzhchen/redquill)
[![codecov](https://codecov.io/gh/vincentzhchen/redquill/coverage.svg?branch=master)](https://codecov.io/gh/vincentzhchen/redquill)

Logging for pandas and more.

## Description

There are functions specifically to log pandas dataframes as well
as functions to count up the total number of errors and warnings.

## Dependencies
- [pandas](https://github.com/pandas-dev/pandas): Tested on 0.20.3
    and higher.  May work for earlier versions.

## Example
For this example, import both the customlogger and pandas.

```python
import redquill as rq
import pandas as pd
```

Initialize the logger.  Note, the logger always logs to the console
by default. You may inrqude a log directory and the log file name,
which will allow the logs to flow into a file as well.
```python
log = rq.redquill()
```

The following will log any null values found in ```df```.
```python
df = pd.DataFrame({"A": [1, 2, None, 3],
                   "B": [4, 2, 2, 5]})
log.warn_null_values(df=df)
```

Console output.
```
2018-03-04 01:34:33,162 - 23512 - WARNING - test_redquill.test_warn_null_values - 
    A  B
2 NaN  2
```

The following will log any duplicates found in column
```B``` of ```df```.
```python
df = pd.DataFrame({"A": [1, 2, None, 3],
                   "B": [4, 2, 2, 5]})
log.warn_duplicate_values(df=df, subset="B", msg="Duplicates on B.")
```

Console output.
```
2018-03-04 02:29:41,419 - 31825 - WARNING - test_redquill.test_warn_duplicate_values - Duplicates on B.
     A  B
1  2.0  2
2  NaN  2
```
