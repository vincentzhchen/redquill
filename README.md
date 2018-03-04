# customlogging
Custom logging module built on top of the Python logging module.

There are functions specifically to log pandas dataframes as well
as functions to count up the total number of errors and warnings.

## Dependencies
- [pandas](https://github.com/pandas-dev/pandas): Tested on 0.20.3
    and higher.  May work for earlier versions.

## Example
For this example, import both the customlogger and pandas.

```python
import customlogging as cl
import pandas as pd
```

Initialize the logger.  Note, the logger always logs to the console
by default. You may include a log directory and the log file name,
which will allow the logs to flow into a file as well.
```python
log = cl.CustomLogging()
```

The following will log null values in column ```B``` of ```df```.
```python
df = pd.DataFrame({"A": [1, 2, None, 3],
                   "B": [4, 2, 2, 5]})
log.warn_null_values(df=df)

# Out
# 2018-03-04 01:34:33,162 - 23512 - WARNING - test_customlogging.test_warn_null_values - 
#     A  B
# 2 NaN  2
```
