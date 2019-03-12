# Logging details and notebook
There are four levels of logging in python: `DEBUG`, `INFO`, `WARNING` and `ERROR`. Below is an example of how to use each level in python, along with a brief style guide for their usage in the QMEE CDT webapp.
### `DEBUG`
`logger.debug("Something minor")`

The `DEBUG` level is the lowest log level. It is used to provide detailed information about the application state and data flow for the purposes of debugging and bug recreation. This should be used for any direct logging of arguments and form data (formatted or otherwise), but be aware that in normal execution conditions, this will not show up in the logs.

### `INFO`
`logger.info("Something of interest")`

The `INFO` level is used for information which the system administrator probably should know about. This should be normal app behaviour, including normal responses to user error. Most logging is done at either this level or at `DEBUG`. Note that the convention presently implemented is that any action which includes a write to the DB should be logged with an `INFO` level log, e.g. submission of proposals or new PIs.

Sometimes it may be nice to put a notification of incorrect user input at the `INFO` level, followed by more detailed information at the `DEBUG` level, e.g.:
```python
logger.info("Form errors: {}".format(len(form.errors)))
logger.debug("in the following fields: {}".format(form.errors.keys()))
```

Which would write the following to the log:
```
22-10-18 18:12:16 - INFO    - add_proposal - Form errors: 16
22-10-18 18:12:16 - DEBUG   - add_proposal - in the following fields: ['training', 'proj_realworld', 'project_description', 'nerc_relevance', 'project_title', 'proj_quant', 'training_loc', 'proj_innov', 'quant_superv', 'case_partner', 'expertise', 'PI2_name', 'multidisciplinarity', 'PI_name', 'proj_evoeco_theory', 'proj_transform']
```
### `WARNING`
`logger.warning("Something went a bit wrong")`

The `WARNING` level is designed for execution states outside of the usual. When a form has returned something outside of the usual, or if a database seems to be lacking an auxiliary table, this should be a `WARNING`. Anything tagged as `WARNING` should be recoverable from for the application.
### `ERROR`
`logger.error("Something is seriously broken!")`

The `ERROR` level is reserved for potentially system-breaking errors. If a form fails to return anything, or a database is impossible to reach, we should be seeing `ERROR` messages in the logs!

#### `EXCEPTION`
`logger.exception("An unhandled exception occurred:")`

The `EXCEPTION` level is a subclass of the `ERROR` level with a bit of extra magic. When executed in the context of a caught exception, this will return not only the message provided, but also the stack trace generated by the exception. This can be used in the following context to catch and log all exceptions before raising them up to the next level:

```python
try:
    foo()
except Exception:
    logger.exception("An unhandled exception occurred")
    raise
```