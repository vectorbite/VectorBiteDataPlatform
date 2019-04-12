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
import shutil
from gluon.validators import *
import datetime
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


def validate_vectraits_rowdict(rowdict, buf):
    """

    :param rowdict:
    :param buf:
    :param failcounter:
    :return:

    >>> validate_vectraits_rowdict({'originaltraitname': 'test'}, StringIO())
    (set([]), 0)

    >>> validate_vectraits_rowdict({'fail': 1}, StringIO())
    (set(['fail']), 1)

    >>> validate_vectraits_rowdict({'fail': 1, 'originaltraitname': 'test'}, StringIO())
    (set(['fail']), 1)

    >>> validate_vectraits_rowdict({'fail': 1, 'fail2': 2}, StringIO())
    (set(['fail', 'fail2']), 2)

    """

    validator_dict = {
        'uid': [placeholder(1)],
        'individualid': [placeholder(1)],
        'originalid': [placeholder(1)],
        'originaltraitname': [placeholder(1)],  # IS_INT_IN_RANGE(minimum=0)],
        'originaltraitdef': [placeholder(1)],
        'standardisedtraitname': [placeholder(1)],
        'standardisedtraitdef': [placeholder(1)],
        'originaltraitvalue': [placeholder(1)],
        'originaltraitunit': [placeholder(1)],
        'originalerrorpos': [placeholder(1)],
        'originalerrorneg': [placeholder(1)],
        'originalerrorunit': [placeholder(1)],
        'standardisedtraitvalue': [placeholder(1)],
        'standardisedtraitunit': [placeholder(1)],
        'standardisederrorpos': [placeholder(1)],
        'standardisederrorneg': [placeholder(1)],
        'standardisederrorunit': [placeholder(1)],
        'replicates': [placeholder(1)],
        'habitat': [placeholder(1)],
        'labfield': [placeholder(1)],
        'arenavalue': [placeholder(1)],
        'arenaunit': [placeholder(1)],
        'arenavaluesi': [placeholder(1)],
        'arenaunitsi': [placeholder(1)],
        'ambienttemp': [placeholder(1)],
        'ambienttempmethod': [placeholder(1)],
        'ambienttempunit': [placeholder(1)],
        'ambientlight': [placeholder(1)],
        'ambientlightunit': [placeholder(1)],
        'secondstressor': [placeholder(1)],
        'secondstressordef': [placeholder(1)],
        'secondstressorvalue': [placeholder(1)],
        'secondstressorunit': [placeholder(1)],
        'timestart': [placeholder(1)],
        'timeend': [placeholder(1)],
        'totalobstimevalue': [placeholder(1)],
        'totalobstimeunit': [placeholder(1)],
        'totalobstimevaluesi': [placeholder(1)],
        'totalobstimeunitsi': [placeholder(1)],
        'totalobstimenotes': [placeholder(1)],
        'resrepvalue': [placeholder(1)],
        'resrepunit': [placeholder(1)],
        'resrepvaluesi': [placeholder(1)],
        'resrepunitsi': [placeholder(1)],
        'climate': [placeholder(1)],
        'location': [placeholder(1)],
        'locationtype': [placeholder(1)],
        'originallocationdate': [placeholder(1)],
        'locationdate': [placeholder(1)],
        'locationdateprecision': [placeholder(1)],
        'coordinatetype': [placeholder(1)],
        'latitude': [placeholder(1)],
        'longitude': [placeholder(1)],
        'interactiontype': [placeholder(1)],
        'interactor1': [placeholder(1)],
        'interactor1common': [placeholder(1)],
        'interactor1wholepart': [placeholder(1)],
        'interactor1wholeparttype': [placeholder(1)],
        'interactor1number': [placeholder(1)],
        'interactor1kingdom': [placeholder(1)],
        'interactor1phylum': [placeholder(1)],
        'interactor1class': [placeholder(1)],
        'interactor1order': [placeholder(1)],
        'interactor1family': [placeholder(1)],
        'interactor1genus': [placeholder(1)],
        'interactor1species': [placeholder(1)],
        'interactor1stage': [placeholder(1)],
        'interactor1temp': [placeholder(1)],
        'interactor1tempunit': [placeholder(1)],
        'interactor1tempmethod': [placeholder(1)],
        'interactor1growthtemp': [placeholder(1)],
        'interactor1growthtempunit': [placeholder(1)],
        'interactor1growthdur': [placeholder(1)],
        'interactor1growthdurunit': [placeholder(1)],
        'interactor1growthtype': [placeholder(1)],
        'interactor1acc': [placeholder(1)],
        'interactor1acctemp': [placeholder(1)],
        'interactor1acctempnotes': [placeholder(1)],
        'interactor1acctime': [placeholder(1)],
        'interactor1acctimenotes': [placeholder(1)],
        'interactor1acctimeunit': [placeholder(1)],
        'interactor1origtemp': [placeholder(1)],
        'interactor1origtempnotes': [placeholder(1)],
        'interactor1origtime': [placeholder(1)],
        'interactor1origtimenotes': [placeholder(1)],
        'interactor1origtimeunit': [placeholder(1)],
        'interactor1equilibtimevalue': [placeholder(1)],
        'interactor1equilibtimeunit': [placeholder(1)],
        'interactor1size': [placeholder(1)],
        'interactor1sizeunit': [placeholder(1)],
        'interactor1sizetype': [placeholder(1)],
        'interactor1sizesi': [placeholder(1)],
        'interactor1sizeunitsi': [placeholder(1)],
        'interactor1denvalue': [placeholder(1)],
        'interactor1denunit': [placeholder(1)],
        'interactor1dentypesi': [placeholder(1)],
        'interactor1denvaluesi': [placeholder(1)],
        'interactor1denunitsi': [placeholder(1)],
        'interactor1massvaluesi': [placeholder(1)],
        'interactor1massunitsi': [placeholder(1)],
        'interactor2': [placeholder(1)],
        'interactor2common': [placeholder(1)],
        'interactor2kingdom': [placeholder(1)],
        'interactor2phylum': [placeholder(1)],
        'interactor2class': [placeholder(1)],
        'interactor2order': [placeholder(1)],
        'interactor2family': [placeholder(1)],
        'interactor2genus': [placeholder(1)],
        'interactor2species': [placeholder(1)],
        'interactor2stage': [placeholder(1)],
        'interactor2temp': [placeholder(1)],
        'interactor2tempunit': [placeholder(1)],
        'interactor2tempmethod': [placeholder(1)],
        'interactor2growthtemp': [placeholder(1)],
        'interactor2growthtempunit': [placeholder(1)],
        'interactor2growthdur': [placeholder(1)],
        'interactor2growthdurunit': [placeholder(1)],
        'interactor2growthtype': [placeholder(1)],
        'interactor2acc': [placeholder(1)],
        'interactor2acctemp': [placeholder(1)],
        'interactor2acctempnotes': [placeholder(1)],
        'interactor2acctime': [placeholder(1)],
        'interactor2acctimenotes': [placeholder(1)],
        'interactor2acctimeunit': [placeholder(1)],
        'interactor2origtemp': [placeholder(1)],
        'interactor2origtempnotes': [placeholder(1)],
        'interactor2origtime': [placeholder(1)],
        'interactor2origtimenotes': [placeholder(1)],
        'interactor2origtimeunit': [placeholder(1)],
        'interactor2equilibtimevalue': [placeholder(1)],
        'interactor2equilibtimeunit': [placeholder(1)],
        'interactor2size': [placeholder(1)],
        'interactor2sizeunit': [placeholder(1)],
        'interactor2sizetype': [placeholder(1)],
        'interactor2sizesi': [placeholder(1)],
        'interactor2sizeunitsi': [placeholder(1)],
        'interactor2denvalue': [placeholder(1)],
        'interactor2denunit': [placeholder(1)],
        'interactor2dentypesi': [placeholder(1)],
        'interactor2denvaluesi': [placeholder(1)],
        'interactor2denunitsi': [placeholder(1)],
        'interactor2massvaluesi': [placeholder(1)],
        'interactor2massunitsi': [placeholder(1)],
        'physicalprocess': [placeholder(1)],
        'physicalprocess_1': [placeholder(1)],
        'physicalprocess_2': [placeholder(1)],
        'citation': [placeholder(1)],
        'doi': [placeholder(1)],
        'published': [placeholder(1)],
        'embargorelease': [placeholder(1)],
        'figuretable': [placeholder(1)],
        'notes': [placeholder(1)],
        'submittedby': [placeholder(1)],
        'contributoremail': [placeholder(1)]
    }

    failcounter = 0
    failed_columns = set()
    for column in rowdict.keys():
        try:
            for v in validator_dict[column]:    # Get validator from validator list
                if v(rowdict[column])[1]:           # If it fails...
                    failed_columns.add(column)   # Append to failed column set
                    failcounter += 1
                    # Write to log and report
                    logger.info('Column "{}" failed validator "{}"'.format(column, v.__class__.__name__))
                    buf.write('    Column "{}" failed validator "{}"\n'.format(column, v.__class__.__name__))
                else:
                    logger.debug('Column "{}" passed validator "{}"'.format(column, v.__class__.__name__))

        except KeyError:
            failed_columns.add(column)      # If failed column does not exist, add to failed set
            failcounter += 1
            # Write to log and report
            logger.info('Invalid column name: "{}"'.format(column))
            buf.write('    Invalid column name: "{}"\n'.format(column))
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
        # TODO: if length of dataset is over 100, output to system log every 10% of progress...
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
    report.write('{}\n'.format('-' * (17 + len(filename))))

    logger.info(failed_dict)    # TODO: return this dict in the correct format.
    # TODO: convert this dict to a nice report and put into report buffer.
    if not long_dataset:
        logger.info(report.getvalue())
    report.close()  # TODO: Just for now
    return None
