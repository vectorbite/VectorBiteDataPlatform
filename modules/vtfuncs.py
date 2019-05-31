#!/bin/env python
# -*- coding: utf-8 -*-

"""
vtfuncs.py
Author: Francis Windram
Created: 27/03/19
Docstr: This file contains many generic VecTraits functions with which to perform validation and other jobs
"""

import logging
from cStringIO import StringIO
from gluon.validators import *
import datetime
from distutils.util import strtobool
import csv
moduledebug = False

if moduledebug:
    import logzero
    logger = logzero.setup_logger(logfile="/tmp/vtfuncsdebug.log",
                                  formatter=logging.Formatter('%(asctime)s - %(levelname)-7s - %(funcName)s - %(message)s')
                                  )
else:
    logger = logging.getLogger("web2py.app.vbdp")


def list_to_dict(h, l):
    """
    Convert a set of two lists to a dictionary

        >>> list_to_dict(["test1", "test2"], [1, 2])
        {'test1': 1, 'test2': 2}

    """
    try:
        return dict(zip(h, l))
    except TypeError:
        raise TypeError("Both headers and values must be in list format")


def data_to_dicts(h, d):
    """
    Convert a list of lists to a list of dicts given a header list

        >>> data_to_dicts(["test1", "test2"], [[1,2], [3,4]])
        [{'test1': 1, 'test2': 2}, {'test1': 3, 'test2': 4}]

        >>> data_to_dicts(["test1", "test2"], [[1,2], [3]])
        [{'test1': 1, 'test2': 2}, {'test1': 3}]

    """
    return [list_to_dict(h, x) for x in d]


def placeholder(x):
    def ph2(y):
        return [y, None]
    return ph2


class IS_BOOL():
    """
    Determines that the argument is (or can be represented as) an bool.

    True values are y, yes, t, true, on and 1.
    False values are "", n, no, f, false, off and 0.
    (Values are case-insensitive)

    Example:
        Used as::

            INPUT(_type='text', _name='name', requires=IS_BOOL())

            >>> IS_BOOL()(True)
            (True, None)
            >>> IS_BOOL()(False)
            (False, None)
            >>> IS_BOOL()("True")
            (True, None)
            >>> IS_BOOL()("False")
            (False, None)
            >>> IS_BOOL()("Yes")
            (True, None)
            >>> IS_BOOL()(100)
            (100, 'enter a boolean')


    """

    def __init__(
        self,
        error_message=None,
    ):
        if not error_message:
            self.error_message = "enter a boolean"
        else:
            self.error_message = error_message

    def __call__(self, value):
        # If value converts nicely to a bool
        try:
            v = bool(strtobool(str(value).lower()))
            return (v, None)
        except ValueError:
            pass
        return (value, self.error_message)


def validate_vectraits_rowdict(rowdict, buf):
    """

    :param rowdict:
    :param buf:
    :return:

    >>> validate_vectraits_rowdict({'originaltraitname': 'test'}, StringIO())
    (set([]), 0)

    >>> validate_vectraits_rowdict({'fail': 1}, StringIO())
    (set(['fail']), 1)

    >>> validate_vectraits_rowdict({'fail': 1, 'originaltraitname': 'test'}, StringIO())
    (set(['fail']), 1)

    >>> validate_vectraits_rowdict({'fail': 1, 'fail2': 2}, StringIO())
    (set(['fail', 'fail2']), 2)

    >>> validate_vectraits_rowdict({'originaltraitunit': "x"*256}, StringIO())
    (set(['originaltraitunit']), 1)

    >>> validate_vectraits_rowdict({'originaltraitvalue': "x"}, StringIO())
    (set(['originaltraitvalue']), 1)

    >>> validate_vectraits_rowdict({'originaltraitvalue': None}, StringIO())
    (set(['originaltraitvalue']), 2)

    >>> validate_vectraits_rowdict({'replicates': -1}, StringIO())
    (set(['replicates']), 1)

    >>> validate_vectraits_rowdict({'published': "1"}, StringIO())
    (set([]), 0)

    >>> validate_vectraits_rowdict({'published': "try again"}, StringIO())
    (set(['published']), 1)

    >>> validate_vectraits_rowdict({'contributoremail': ""}, StringIO())
    (set(['contributoremail']), 2)

    >>> validate_vectraits_rowdict({'contributoremail': "mrfrancis"}, StringIO())
    (set(['contributoremail']), 1)

    >>> validate_vectraits_rowdict({'locationdate': "04/08/1992"}, StringIO())
    (set([]), 0)

    >>> validate_vectraits_rowdict({'locationdate': "4 August 92"}, StringIO())
    (set(['locationdate']), 1)

    """

    validator_dict = {
        'originalid': [IS_NOT_EMPTY(), IS_LENGTH(20)],
        'originaltraitname': [IS_LENGTH(255)],
        'originaltraitdef': [],
        'standardisedtraitname': [IS_LENGTH(255)],
        'standardisedtraitdef': [],
        'originaltraitvalue': [IS_NOT_EMPTY(), IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'originaltraitunit': [IS_NOT_EMPTY(), IS_LENGTH(255)],
        'originalerrorpos': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'originalerrorneg': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'originalerrorunit': [IS_LENGTH(255)],
        'standardisedtraitvalue': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'standardisedtraitunit': [IS_LENGTH(255)],
        'standardisederrorpos': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'standardisederrorneg': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'standardisederrorunit': [IS_LENGTH(255)],
        'replicates': [IS_INT_IN_RANGE(1, 2**31)],
        'habitat': [IS_LENGTH(20)],
        'labfield': [IS_LENGTH(11)],
        'arenavalue': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'arenaunit': [IS_LENGTH(255)],
        'arenavaluesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'arenaunitsi': [IS_LENGTH(255)],
        'ambienttemp': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'ambienttempmethod': [IS_LENGTH(255)],
        'ambienttempunit': [IS_LENGTH(255)],
        'ambientlight': [IS_LENGTH(255)],
        'ambientlightunit': [IS_LENGTH(255)],
        'secondstressor': [IS_LENGTH(255)],
        'secondstressordef': [IS_LENGTH(255)],
        'secondstressorvalue': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'secondstressorunit': [IS_LENGTH(255)],
        'timestart': [IS_LENGTH(255)],
        'timeend': [IS_LENGTH(255)],
        'totalobstimevalue': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'totalobstimeunit': [IS_LENGTH(255)],
        'totalobstimevaluesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'totalobstimeunitsi': [IS_LENGTH(255)],
        'totalobstimenotes': [IS_LENGTH(255)],
        'resrepvalue': [IS_INT_IN_RANGE(-2**31, 2**31)],
        'resrepunit': [IS_LENGTH(255)],
        'resrepvaluesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'resrepunitsi': [IS_LENGTH(255)],
        'location': [IS_NOT_EMPTY()],
        'locationtype': [IS_LENGTH(255)],
        'originallocationdate': [IS_LENGTH(255)],
        'locationdate': [IS_DATE(format='%d/%m/%Y', error_message='must be DD/MM/YYYY!')],
        'locationdateprecision': [IS_NOT_EMPTY(), IS_INT_IN_RANGE(0,6)],
        'coordinatetype': [IS_LENGTH(255)],
        'latitude': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'longitude': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1': [IS_LENGTH(255)],     #, Custom Validator, at least one filled:],
        'interactor1common': [IS_LENGTH(255)],     #, Custom Validator, at least one filled:],
        'interactor1wholepart': [IS_LENGTH(255)],
        'interactor1wholeparttype': [IS_LENGTH(255)],
        'interactor1number': [IS_LENGTH(255)],
        'interactor1kingdom': [IS_LENGTH(50)],
        'interactor1phylum': [IS_LENGTH(50)],
        'interactor1class': [IS_LENGTH(50)],
        'interactor1order': [IS_LENGTH(50)],
        'interactor1family': [IS_LENGTH(50)],
        'interactor1genus': [IS_LENGTH(50)],
        'interactor1species': [IS_LENGTH(255)],
        'interactor1stage': [IS_LENGTH(255)],
        'interactor1temp': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1tempunit': [IS_LENGTH(255)],
        'interactor1tempmethod': [IS_LENGTH(255)],
        'interactor1growthtemp': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1growthtempunit': [IS_LENGTH(255)],
        'interactor1growthdur': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1growthdurunit': [IS_LENGTH(255)],
        'interactor1growthtype': [IS_LENGTH(255)],
        'interactor1acc': [IS_LENGTH(255)],
        'interactor1acctemp': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1acctempnotes': [IS_LENGTH(255)],
        'interactor1acctime': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1acctimenotes': [IS_LENGTH(255)],
        'interactor1acctimeunit': [IS_LENGTH(255)],
        'interactor1origtemp': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1origtempnotes': [IS_LENGTH(255)],
        'interactor1origtime': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1origtimenotes': [IS_LENGTH(255)],
        'interactor1origtimeunit': [IS_LENGTH(255)],
        'interactor1equilibtimevalue': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1equilibtimeunit': [IS_LENGTH(255)],
        'interactor1size': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1sizeunit': [IS_LENGTH(255)],
        'interactor1sizetype': [IS_LENGTH(255)],
        'interactor1sizesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1sizeunitsi': [IS_LENGTH(255)],
        'interactor1denvalue': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1denunit': [IS_LENGTH(255)],
        'interactor1dentypesi': [IS_LENGTH(255)],
        'interactor1denvaluesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1denunitsi': [IS_LENGTH(255)],
        'interactor1massvaluesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1massunitsi': [IS_LENGTH(255)],
        'interactor2': [IS_LENGTH(255)],
        'interactor2common': [IS_LENGTH(255)],
        'interactor2kingdom': [IS_LENGTH(50)],
        'interactor2phylum': [IS_LENGTH(50)],
        'interactor2class': [IS_LENGTH(50)],
        'interactor2order': [IS_LENGTH(50)],
        'interactor2family': [IS_LENGTH(50)],
        'interactor2genus': [IS_LENGTH(50)],
        'interactor2species': [IS_LENGTH(255)],
        'interactor2stage': [IS_LENGTH(255)],
        'interactor2temp': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2tempunit': [IS_LENGTH(255)],
        'interactor2tempmethod': [IS_LENGTH(255)],
        'interactor2growthtemp': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2growthtempunit': [IS_LENGTH(255)],
        'interactor2growthdur': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2growthdurunit': [IS_LENGTH(255)],
        'interactor2growthtype': [IS_LENGTH(255)],
        'interactor2acc': [IS_LENGTH(255)],
        'interactor2acctemp': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2acctempnotes': [IS_LENGTH(255)],
        'interactor2acctime': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2acctimenotes': [IS_LENGTH(255)],
        'interactor2acctimeunit': [IS_LENGTH(255)],
        'interactor2origtemp': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2origtempnotes': [IS_LENGTH(255)],
        'interactor2origtime': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2origtimenotes': [IS_LENGTH(255)],
        'interactor2origtimeunit': [IS_LENGTH(255)],
        'interactor2equilibtimevalue': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2equilibtimeunit': [IS_LENGTH(255)],
        'interactor2size': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2sizeunit': [IS_LENGTH(255)],
        'interactor2sizetype': [IS_LENGTH(255)],
        'interactor2sizesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2sizeunitsi': [IS_LENGTH(255)],
        'interactor2denvalue': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2denunit': [IS_LENGTH(255)],
        'interactor2dentypesi': [IS_LENGTH(255)],
        'interactor2denvaluesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2denunitsi': [IS_LENGTH(255)],
        'interactor2massvaluesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor2massunitsi': [IS_LENGTH(255)],
        'physicalprocess': [IS_LENGTH(255)],
        'physicalprocess_1': [IS_LENGTH(255)],
        'physicalprocess_2': [IS_LENGTH(255)],
        'citation': [IS_NOT_EMPTY(), IS_LENGTH(1500)],
        'doi': [IS_LENGTH(255)],
        'published': [IS_NOT_EMPTY(), IS_BOOL()],
        'embargorelease': [IS_NOT_EMPTY(), IS_DATE(format='%d/%m/%Y', error_message='must be DD/MM/YYYY!')],
        'figuretable': [IS_LENGTH(255)],
        'notes': [IS_LENGTH(2055)],
        'submittedby': [IS_NOT_EMPTY(), IS_LENGTH(255)],
        'contributoremail': [IS_NOT_EMPTY(), IS_EMAIL(), IS_LENGTH(255)],
    }

    notnull_cols = {
        "originalid",
        "originaltraitvalue",
        "originaltraitunit",
        "location",
        "locationdateprecision",
        "citation",
        "published",
        "embargorelease",
        "submittedby",
        "contributoremail",
    }

    failcounter = 0
    failed_columns = set()
    for column in rowdict.keys():
        if column not in notnull_cols and rowdict[column] == "":
            # Don't fail empty strings if they are not required columns
            continue
        try:
            for v in validator_dict[column]:    # Get validator from validator list
                if v(rowdict[column])[1]:           # If it fails...
                    failed_columns.add(column)   # Append to failed column set
                    failcounter += 1
                    # Write to log and report
                    logger.info('Column "{}" failed validator "{}, value:"{}"'.format(column, v.__class__.__name__, rowdict[column]))
                    buf.write('    Column "{}" failed validator "{}, value:"{}"\n'.format(column, v.__class__.__name__, rowdict[column]))
                else:
                    logger.debug('Column "{}" passed validator "{}"'.format(column, v.__class__.__name__))

        except KeyError:
            failed_columns.add(column)      # If failed column does not exist, add to failed set
            failcounter += 1
            # Write to log and report
            logger.info('Invalid column name: "{}"'.format(column))
            buf.write('    Invalid column name: "{}"\n'.format(column))
    # Validate that either interactor1 or interactor1common is filled.
    return failed_columns, failcounter


def validate_vectraits(data, filename='test.csv'):
    """
    Validate a list of vectraits data and determine whether the form is correct for upload.

    :param data:
    :return: A dict of all columns which contain errors and on which line/s they occur

    >>> validate_vectraits([["test1", "originaltraitname"], [1,2], [3,4]])

    """
    # Print setup to log
    start = datetime.datetime.now()
    logger.info('{}'.format('-'*(38+len(filename))))
    logger.info('  Validation of {} started at {}'.format(filename, start.strftime('%H:%M:%S')))
    logger.debug('  File length: {} rows'.format(len(data)-1))
    logger.info('{}'.format('-' * (38 + len(filename))))

    # Print report setup to report buffer
    report = StringIO()
    report.write('\n{}\n'.format('-'*(17+len(filename))))
    report.write('  VALIDATION REPORT\n\n')
    report.write('    File name: {}\n'.format(filename))
    report.write('  File length: {} rows\n'.format(len(data)-1))
    report.write('      Started: {}\n'.format(start.strftime('%d-%m-%y %H:%M:%S')))
    report.write('{}\n\n'.format('-' * (17 + len(filename))))

    # Isolate header
    header = data.pop(0)

    errcounter = 0
    errlinecounter = 0
    failed = False

    # Validate header to make sure all columns are present, and reject if so.

    output = data_to_dicts(header, data)
    failed_dict = {}
    long_dataset = False
    log_triggers = {}

    if len(output) > 500:
        long_dataset = True
        trigger_list = [int(len(output)*(x/float(10)))-1 for x in range(0, 11)]
        trigger_list[0] = 0
        percentile_list = [x*10 for x in range(0, 11)]
        log_triggers = dict(zip(trigger_list, percentile_list))

    # Validate rows against validators using validate_vectraits_rows
    for i, item in enumerate(output):
        if long_dataset:
            if i in log_triggers.keys():
                logger.info('Validating row {}/{} ({}%)...'.format(i + 1, len(output), log_triggers[i]))
        else:
            logger.info('Validating row {}...'.format(i+1))
        report.write('Validating row {}...\n'.format(i+1))
        failed_items, errdelta = validate_vectraits_rowdict(item, report)
        if errdelta > 0:
            errcounter += errdelta
            errlinecounter += 1
            for entry in failed_items:
                try:
                    failed_dict[entry].append(i+1)
                except KeyError:
                    failed_dict[entry] = [i+1]

    # Return Validation dictionary

    # Finish up in log
    logger.info('{}'.format('-' * (38 + len(filename))))
    end = datetime.datetime.now()
    logger.info('Validation finished at {}'.format(end.strftime('%H:%M:%S')))
    logger.info('         Errors: {}'.format(errcounter))
    logger.info('   Failed lines: {}'.format(errlinecounter))
    time_elapsed = end - start
    logger.info('Validation time: {}'.format(time_elapsed))
    logger.info('{}'.format('-' * (38 + len(filename))))

    # Finish up in report
    report.write('\n{}\n'.format('-' * (17 + len(filename))))
    report.write('  VALIDATION COMPLETE\n\n')
    report.write('         Ended: {}\n'.format(end.strftime('%H:%M:%S')))
    report.write('        Errors: {}\n'.format(errcounter))
    report.write('  Failed lines: {}\n'.format(errlinecounter))
    report.write('  Time elapsed: {}\n'.format(time_elapsed))
    report.write('{}\n\n'.format('-' * (17 + len(filename))))
    report.write('  COLUMN REPORT  \n\n')
    logger.info(failed_dict)    # TODO: return this dict in the correct format.
    # TODO: convert this dict to a nice report and put into report buffer.
    for x, y in failed_dict.iteritems():
        if len(y) == 1:
            report.write('"{}" failed on row: {}\n'.format(x, y))
        else:
            report.write('"{}" failed on rows: {}\n'.format(x, y))
    report_str = report.getvalue()
    if not long_dataset:
        logger.info(report_str)
    try:
        report.close()  # TODO: Just for now
    except ValueError:
        pass
    if errcounter:
        failed = True
    return report_str, failed


def upload_vectraits_dataset(csvpath):
    logger.info("Starting data upload from {}".format(csvpath))
    import pandas as pd

    # Load csv
    logger.debug("Opening data file")
    try:
        datafile = pd.read_csv(csvpath)
    except IOError:
        logger.exception("Error opening data file")
        return False

    # Extract unique locations
    logger.info("Extracting unique locations")


    # Extract unique Taxonomy entries
    # Extract unique trait descriptions
    # Extract contributor
    # Extract citation
    # Extract source info (incl. contrib & citation ids)
    # Extract experimental conditions
    # Make maintable (incl ids for all other tables)
    # Upload to db
    return True
