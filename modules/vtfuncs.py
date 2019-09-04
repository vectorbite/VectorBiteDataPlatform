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
from gluon.sqlhtml import ExportClass
from gluon import current
import datetime
from distutils.util import strtobool
import hashlib
from random import randint
from os.path import basename

import csv

# make it so this is only turned on when web2py is not the context
moduledebug = False

if moduledebug:
    import logzero

    logger = logzero.setup_logger(logfile="/tmp/vtfuncsdebug.log",
                                  formatter=logging.Formatter(
                                      '%(asctime)s - %(levelname)-7s - %(funcName)s - %(message)s')
                                  )
else:
    logger = logging.getLogger("web2py.app.vbdp")


def asciilogo():
    out = """
    
                                                    /.                                                                 
                                                 #@%/% ,%%*#                                                           
                                               /@/  ,@@&.  %                                                           
                                     *%&@@&(  %%    #,&/   %                                                           
               .&@@/  .#,#/      ,&@@@@@@@@@@@/   (/  ,&.  &.  .*%@&(/(&@&%%%(*.*/                                     
                &%.(@#/*   ,%* .&@@@@@@@@@@@@@&&@@&&%#(@@%*&%@@&/  .*#%%&@,      #                                     
                %(   %@*     *@@@@@@@@@@@@@@%.         (@@@%(((#%&@@/*.,@#     ./                                    
             ,# #(   .@@/    .@@@@@@@@@@@@@@@@@@@@@@@*&@@@,             .*%@@&/.  %*                                   
              .&%%   ,. ,@(  .@@@@@@@@@@                %@@.                 (&. .(%@(.                                
               ,@@,  #    /@(.@@@@@@@@@@ VECTORBYTE.ORG @@@@@&(,              .&/     .(                             
         ,#/.   #@@/,%      %@#/#@@@@@@@                @@@@@@@@@@@&(,          #&        %(                           
            *%%.(@*,@@      /@@@&@@@@@@@@@@@(&@@@@@@@@@@@@@@@@@@@@@@@@@&(/,,,,,%@#*,*/(((/.                          
               ,@@&@%.,/* .@@@@@@@@*.@@@&*.       *&@@@@@@@@@@@@@@@@@@@@@@#.      #@&,&,                               
                (@,#. ,/#&@@@@@@@@@%  (@*           ,&@@@@@@@@@@@@@@@@@@@@@@#      .&@@%                               
                (@//       #@@@@@@@@&                  (@@@@@@@@@@@@@@@@@@@@@@,      #@@/                              
                %@&.        *@@@@@&   #,                  (@@@@@@@@@@@@@@@@@@@@@(     ,@@*                             
               .&@/           *&@@/   (,                   @(./%@@@@@@@@@@@@@@@@@@/    ,@@                             
               ,@&.       .,,, (@/   #.                    &(      *(%&@@@@@@@@@@@@@@/  ,@/                            
               *@(            ,,#  //                      %&               ..,***,,     .@%.                          
               %&              /@%.                         %@#                            ,%@@#,                      
              ,@*              %%                            ,&@&*                            ./&@&/.                  
           .(@@/              .&,                               /&@#,                             ,#@@&(.              
      .(&@@%*.                *&.                                  /&@@#,                             ./&@,          
*#@@*                       #(                                        ./&@@&%#(,                          .*#&@@&%#(/
                              &,                                               ...                                  ...
                              &                                                                                        
                             .(                                                                                        
                             *,                                                                                        
                             #                                                                                         
                            .%                                                                                         
                            *#                                                                                         
                            #*                                                                                         
                            #.                                                                                         
                           ,#                                                                                          
                           (,                                                                                          
                           #.                                                                                          
                          .(                                                                                           
                          */                                                                                           
                          #,                                                                                           
                     ,&@@@@@,                                                                                          
                   ,@@@@@@@@@%                                                                                         
                  ,@@@@@@@@@@@,                                                                                        
                  *@@@@@@@@@@@/                                                                                        
                  .&@@@@@@@@@@.                                                                                        
                   .&@@@@@@@@#                                                                                         
                      *#%#*.
                      """
    return out


def list_to_dict(h, l):
    """
    Convert a set of two lists to a dictionary

        >>> list_to_dict(["test1", "test2"], [1, 2])
        {'test1': 1, 'test2': 2}
        >>> list_to_dict(["test1", "test2"], ["NA", "nan"])
        {'test1': '', 'test2': ''}

    """
    try:
        l = ["" if (x in {"", "NA", "na", "NaN", "nan"}) else x for x in l]
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
        'replicates': [IS_INT_IN_RANGE(1, 2 ** 31)],
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
        'resrepvalue': [IS_INT_IN_RANGE(-2 ** 31, 2 ** 31)],
        'resrepunit': [IS_LENGTH(255)],
        'resrepvaluesi': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'resrepunitsi': [IS_LENGTH(255)],
        'location': [IS_NOT_EMPTY()],
        'locationtype': [IS_LENGTH(255)],
        'originallocationdate': [IS_LENGTH(255)],
        'locationdate': [IS_DATE(format='%d/%m/%Y', error_message='must be DD/MM/YYYY!')],
        'locationdateprecision': [IS_NOT_EMPTY(), IS_INT_IN_RANGE(0, 6)],
        'coordinatetype': [IS_LENGTH(255)],
        'latitude': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'longitude': [IS_FLOAT_IN_RANGE(-1e100, 1e100)],
        'interactor1': [IS_LENGTH(255)],  # , Custom Validator, at least one filled:],
        'interactor1common': [IS_LENGTH(255)],  # , Custom Validator, at least one filled:],
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

    notnull_trackerset = set()

    failcounter = 0
    failed_columns = set()
    for column in rowdict.keys():
        if column not in notnull_cols and rowdict[column] in {"", "NA", "na", "NaN", "nan"}:
            # Don't fail empty strings if they are not required columns
            continue
        if column in notnull_cols:
            notnull_trackerset.add(column)
        try:
            for v in validator_dict[column]:  # Get validator from validator list
                if v(rowdict[column])[1]:  # If it fails...
                    failed_columns.add(column)  # Append to failed column set
                    failcounter += 1
                    # Write to log and report
                    logger.info('Column "{}" failed validator "{}, value:"{}"'.format(column, v.__class__.__name__,
                                                                                      rowdict[column]))
                    buf.write('    Column "{}" failed validator "{}, value:"{}"\n'.format(column, v.__class__.__name__,
                                                                                          rowdict[column]))
                else:
                    logger.debug('Column "{}" passed validator "{}"'.format(column, v.__class__.__name__))

        except KeyError:
            failed_columns.add(column)  # If failed column does not exist, add to failed set
            failcounter += 1
            # Write to log and report
            logger.info('Invalid column name: "{}"'.format(column))
            buf.write('    Invalid column name: "{}"\n'.format(column))
    # Validate that either interactor1 or interactor1common is filled.

    missing_cols = notnull_cols.difference(notnull_trackerset)
    if missing_cols:
        failed_columns = failed_columns | missing_cols
        failcounter += len(missing_cols)
        logger.info('Missing essential columns: {}'.format(" ,".join(missing_cols)))
        buf.write('    Missing essential columns: {}\n'.format(", ".join(missing_cols)))
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
    logger.info('{}'.format('-' * (38 + len(filename))))
    logger.info('  Validation of {} started at {}'.format(filename, start.strftime('%H:%M:%S')))
    logger.debug('  File length: {} rows'.format(len(data) - 1))
    logger.info('{}'.format('-' * (38 + len(filename))))

    # Print report setup to report buffer
    report = StringIO()
    report.write('\n{}\n'.format('-' * (17 + len(filename))))
    report.write('  VALIDATION REPORT\n\n')
    report.write('    File name: {}\n'.format(filename))
    report.write('  File length: {} rows\n'.format(len(data) - 1))
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
        trigger_list = [int(len(output) * (x / float(10))) - 1 for x in range(0, 11)]
        trigger_list[0] = 0
        percentile_list = [x * 10 for x in range(0, 11)]
        log_triggers = dict(zip(trigger_list, percentile_list))

    # Validate rows against validators using validate_vectraits_rows
    for i, item in enumerate(output):
        if long_dataset:
            if i in log_triggers.keys():
                logger.info('Validating row {}/{} ({}%)...'.format(i + 1, len(output), log_triggers[i]))
        else:
            logger.info('Validating row {}...'.format(i + 1))
        report.write('Validating row {}...\n'.format(i + 1))
        failed_items, errdelta = validate_vectraits_rowdict(item, report)
        if errdelta > 0:
            errcounter += errdelta
            errlinecounter += 1
            for entry in failed_items:
                try:
                    failed_dict[entry].append(i + 1)
                except KeyError:
                    failed_dict[entry] = [i + 1]

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
    logger.info(failed_dict)  # TODO: return this dict in the correct format.
    # TODO: convert this dict to a nice report and put into report buffer.
    for x, y in failed_dict.iteritems():
        if len(y) == 1:
            report.write('"{}" failed on row: {}\n'.format(x, y))
        else:
            report.write('"{}" failed on rows: {}\n'.format(x, y))

    if not randint(0, 19):
        report.write("\n\n\n")
        report.write(asciilogo())
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


class DataIntegrityError(Exception):
    pass


class VTUploadError(Exception):
    pass


def upload_vectraits_dataset(csvpath, templatepath="../static/templates/vectraits_template.csv", logger=False):
    """

    :param csvpath:
    :param templatepath:
    :return:

    >>> upload_vectraits_dataset("../uploads/tests/missingcols.csv", "path/to/nothing.csv")
    False
    >>> upload_vectraits_dataset("../uploads/tests/passing.csv")
    True
    >>> upload_vectraits_dataset("../uploads/tests/passing_long.csv")
    True
    >>> upload_vectraits_dataset("../uploads/tests/missingcols.csv")
    True
    >>> upload_vectraits_dataset("../uploads/tests/missingcols_long.csv")
    True


    """

    def md5sum(filename, blocksize=65536):
        """
        Generate md5 hash of a file in a memory-efficient manner

        :param filename:    Path of file to be hashed
        :param blocksize:   Size of block to read in each loop (default 64kB)
        :return:            Hex representation of file hash (32B str)
        """
        hash = hashlib.md5()
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hash.update(block)
        return hash.hexdigest()

    def noneadapter(x):
        """
        Return None rather than NaN to allow correct selection of null values in DAL.

        Seems hacky, but hopefully should be fast enough.
        """

        if pd.isna(x):
            return None
        return x

    import logzero
    if not logger:
        logger = logzero.setup_logger(logfile="logs/vtuploads.log",
                                      formatter=logging.Formatter(
                                          '%(asctime)s - %(levelname)-7s - %(funcName)s - %(message)s'),
                                      disableStderrLogger=True)
        logger.info("Turned on logger in upload_vectraits_dataset")

    # Load db connection
    db2 = current.db2

    # Simple check to make sure dataset hasn't been uploaded before.
    logger.info("Checking whether file is unique...")
    filemd5 = md5sum(csvpath)
    logger.debug("File hash = {}".format(filemd5))
    search = db2(
        (db2.dataset_hash.filehash == filemd5)
    ).select()

    if len(search) > 0:
        logger.error("File hash already in database!")
        raise VTUploadError("File hash {} for {} already in database".format(filemd5, csvpath))
    else:
        logger.info("New file! Processing...")

    logger.info("Starting data upload from {}".format(basename(csvpath)))
    import pandas as pd
    import numpy as np

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                        DATA PREP                                        │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Load csv
    logger.info("Opening data file...")
    try:
        datafile = pd.read_csv(csvpath)
    except IOError:
        logger.exception("Error opening data file {}".format(csvpath))
        raise VTUploadError("Error opening data file {}".format(csvpath))

    try:
        template = pd.read_csv(templatepath)
    except IOError:
        logger.exception("Error opening template file {}".format(templatepath))
        raise VTUploadError("Error opening template file {}".format(templatepath))

    # Check for missing columns, and if missing, insert with blank values
    logger.debug("datafile keys:{}".format(len(datafile.keys())))
    logger.debug("template keys:{}".format(len(template.keys())))
    difflist = list(set(template.keys()).difference(set(datafile.keys())))

    if difflist:
        logger.info("Creating missing columns: {}".format(difflist))
        missing_cols = pd.DataFrame(np.nan, index=range(0, len(datafile.index)), columns=difflist)
        logger.debug(missing_cols.dtypes)
        datafile = pd.concat([datafile, missing_cols], axis=1)

    # Create id fields in main table
    def idcat(*args):
        return " ".join([str(x) for x in args])

    datafile["locationidstr"] = np.vectorize(idcat)(datafile.location, datafile.locationtype,
                                                    datafile.originallocationdate, datafile.locationdate,
                                                    datafile.locationdateprecision, datafile.latitude,
                                                    datafile.longitude)
    datafile["traitdescripidstr"] = np.vectorize(idcat)(datafile.physicalprocess, datafile.physicalprocess_1,
                                                        datafile.physicalprocess_2)
    datafile["expcondidstr"] = np.vectorize(idcat)(datafile.replicates, datafile.habitat, datafile.labfield,
                                                   datafile.arenavalue, datafile.arenaunit, datafile.arenavaluesi,
                                                   datafile.arenaunitsi, datafile.resrepvalue, datafile.resrepunit,
                                                   datafile.resrepvaluesi, datafile.resrepunitsi)
    datafile["interactor1idstr"] = np.vectorize(idcat)(datafile.interactor1kingdom,
                                                       datafile.interactor1phylum,
                                                       datafile.interactor1class,
                                                       datafile.interactor1order,
                                                       datafile.interactor1family,
                                                       datafile.interactor1genus,
                                                       datafile.interactor1species)
    datafile["interactor2idstr"] = np.vectorize(idcat)(datafile.interactor2kingdom,
                                                       datafile.interactor2phylum,
                                                       datafile.interactor2class,
                                                       datafile.interactor2order,
                                                       datafile.interactor2family,
                                                       datafile.interactor2genus,
                                                       datafile.interactor2species)
    datafile["sourceinfoidstr"] = np.vectorize(idcat)(datafile.originalid,
                                                      datafile.figuretable,
                                                      datafile.submittedby,
                                                      datafile.contributoremail,
                                                      datafile.citation,
                                                      datafile.doi,
                                                      datafile.published,
                                                      datafile.embargorelease)

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                        LOCATIONS                                        │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Extract unique locations
    logger.info("Extracting unique locations...")
    locationnames = ["location", "locationtype", "originallocationdate", "locationdate", "locationdateprecision",
                     "latitude", "longitude", "locationidstr"]
    locations = datafile[locationnames]
    locations_uni = locations.drop_duplicates().reset_index(drop=True)
    locations_uni["locationid"] = np.int(-1)

    # locations = locations.fillna(None)    # Cannot replace with None as None is a different type to float64...

    # logger.debug(locations_uni)
    inscount = 0
    foundcoconut = 0
    errcount = 0
    for index, entry in locations_uni.iterrows():
        locationid = np.nan
        search = db2(
            (db2.studylocation.locationtext == noneadapter(entry.location)) &
            (db2.studylocation.locationtype == noneadapter(entry.locationtype)) &
            (db2.studylocation.originallocationdate == noneadapter(entry.originallocationdate)) &
            (db2.studylocation.locationdate == noneadapter(entry.locationdate)) &
            (db2.studylocation.locationdateprecision == noneadapter(entry.locationdateprecision)) &
            (db2.studylocation.latitude == noneadapter(entry.latitude)) &
            (db2.studylocation.longitude == noneadapter(entry.longitude))
        ).select(db2.studylocation.locationid)
        # logger.debug(len(search))
        if len(search) < 1:
            # insert into db
            inscount += 1
            locationid = db2.studylocation.insert(locationtext=noneadapter(entry.location),
                                                  locationtype=noneadapter(entry.locationtype),
                                                  originallocationdate=noneadapter(entry.originallocationdate),
                                                  locationdate=noneadapter(entry.locationdate),
                                                  locationdateprecision=noneadapter(entry.locationdateprecision),
                                                  latitude=noneadapter(entry.latitude),
                                                  longitude=noneadapter(entry.longitude))
            logger.debug("Inserted location id {}".format(locationid))
        elif len(search) == 1:
            # Use the found id
            foundcoconut += 1
            locationid = search[0].locationid
        else:
            errcount += 1
            logger.warning("Ambiguous location entry provided:\n\n{}\n\n{}".format(entry, search))
            locationid = search[0].locationid

        locations_uni.ix[index, "locationid"] = locationid

    logger.debug("--- TABLE: studylocation ---")
    logger.debug("Inserted: {}".format(inscount))
    logger.debug("Found: {}".format(foundcoconut))
    logger.debug("Errors: {}".format(errcount))
    logger.debug("----------------------------")
    # left join locations_uni to main df on locationidstr
    locations_uni = locations_uni[["locationidstr", "locationid"]]
    datafile = pd.merge(datafile, locations_uni, on="locationidstr", how="left")

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                        TAXONOMY                                         │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Extract unique Taxonomy entries
    logger.info("Extracting unique taxonomic groups...")
    interactor1_names = ["interactor1kingdom", "interactor1phylum", "interactor1class", "interactor1order",
                         "interactor1family", "interactor1genus", "interactor1species", "interactor1idstr"]
    interactor2_names = ["interactor2kingdom", "interactor2phylum", "interactor2class", "interactor2order",
                         "interactor2family", "interactor2genus", "interactor2species", "interactor2idstr"]
    interactor1_tax = datafile[interactor1_names]
    interactor2_tax = datafile[interactor2_names]

    # Rename columns in both dfs and merge together
    interactor1_tax.columns = ["taxkingdom", "taxphylum", "taxclass", "taxorder",
                               "taxfamily", "taxgenus", "taxspecies", "interactoridstr"]
    interactor2_tax.columns = ["taxkingdom", "taxphylum", "taxclass", "taxorder",
                               "taxfamily", "taxgenus", "taxspecies", "interactoridstr"]

    interactor_tax = pd.concat([interactor1_tax, interactor2_tax])
    interactor_tax_uni = interactor_tax.drop_duplicates().reset_index(drop=True)
    interactor_tax_uni["interactorxid"] = np.int(-1)

    inscount = 0
    foundcoconut = 0
    errcount = 0
    for index, entry in interactor_tax_uni.iterrows():
        interactorxid = np.nan
        search = db2(
            (db2.taxonomy.taxkingdom == noneadapter(entry.taxkingdom)) &
            (db2.taxonomy.taxphylum == noneadapter(entry.taxphylum)) &
            (db2.taxonomy.taxclass == noneadapter(entry.taxclass)) &
            (db2.taxonomy.taxorder == noneadapter(entry.taxorder)) &
            (db2.taxonomy.taxfamily == noneadapter(entry.taxfamily)) &
            (db2.taxonomy.taxgenus == noneadapter(entry.taxgenus)) &
            (db2.taxonomy.taxspecies == noneadapter(entry.taxspecies))
        ).select(db2.taxonomy.taxid)
        if len(search) < 1:
            # insert into db
            inscount += 1
            interactorxid = db2.taxonomy.insert(taxkingdom=noneadapter(entry.taxkingdom),
                                                taxphylum=noneadapter(entry.taxphylum),
                                                taxclass=noneadapter(entry.taxclass),
                                                taxorder=noneadapter(entry.taxorder),
                                                taxfamily=noneadapter(entry.taxfamily),
                                                taxgenus=noneadapter(entry.taxgenus),
                                                taxspecies=noneadapter(entry.taxspecies))
            logger.debug("Inserted taxonomy id {}".format(interactorxid))
        elif len(search) == 1:
            # Use the found id
            foundcoconut += 1
            interactorxid = search[0].taxid
        else:
            errcount += 1
            logger.warning("Ambiguous taxonomy entry provided:\n\n{}\n\n{}".format(entry, search))
            interactorxid = search[0].taxid

        interactor_tax_uni.ix[index, "interactorxid"] = interactorxid

    logger.debug("----- TABLE: taxonomy ------")
    logger.debug("Inserted: {}".format(inscount))
    logger.debug("Found: {}".format(foundcoconut))
    logger.debug("Errors: {}".format(errcount))
    logger.debug("----------------------------")

    # left join interactor_tax_uni to main df on interactoridstr
    interactor_tax_uni = interactor_tax_uni[["interactoridstr", "interactorxid"]]

    # We need to use a slightly different method here as this foreignid gets left-joined twice, once for each spp
    datafile = pd.merge(datafile, interactor_tax_uni, left_on="interactor1idstr", right_on="interactoridstr",
                        how="left")
    datafile = datafile.rename(columns={"interactorxid": "interactor1id"})

    datafile = pd.merge(datafile, interactor_tax_uni, left_on="interactor2idstr", right_on="interactoridstr",
                        how="left")
    datafile = datafile.rename(columns={"interactorxid": "interactor2id"})

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                        TRAITDESC                                        │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Extract unique trait descriptions
    logger.info("Extracting unique trait descriptions...")
    traitdescrip_names = ["physicalprocess", "physicalprocess_1", "physicalprocess_2", "traitdescripidstr"]
    traitdescrips = datafile[traitdescrip_names]
    traitdescrips_uni = traitdescrips.drop_duplicates().reset_index(drop=True)
    traitdescrips_uni["traitdescriptionid"] = np.int(-1)

    inscount = 0
    foundcoconut = 0
    errcount = 0
    for index, entry in traitdescrips_uni.iterrows():
        traitdescriptionid = np.nan
        search = db2(
            (db2.traitdescription.physicalprocess == noneadapter(entry.physicalprocess)) &
            (db2.traitdescription.physicalprocess_1 == noneadapter(entry.physicalprocess_1)) &
            (db2.traitdescription.physicalprocess_2 == noneadapter(entry.physicalprocess_2))
        ).select(db2.traitdescription.traitdesid)
        if len(search) < 1:
            # insert into db
            inscount += 1
            traitdescriptionid = db2.traitdescription.insert(physicalprocess=noneadapter(entry.physicalprocess),
                                                             physicalprocess_1=noneadapter(entry.physicalprocess_1),
                                                             physicalprocess_2=noneadapter(entry.physicalprocess_2))
            logger.debug("Inserted traitdescrip id {}".format(traitdescriptionid))
        elif len(search) == 1:
            # Use the found id
            foundcoconut += 1
            traitdescriptionid = search[0].traitdesid
        else:
            errcount += 1
            logger.warning("Ambiguous trait description entry provided:\n\n{}\n\n{}".format(entry, search))
            traitdescriptionid = search[0].traitdesid

        traitdescrips_uni.ix[index, "traitdescriptionid"] = traitdescriptionid

    logger.debug("--- TABLE: traitdescription ---")
    logger.debug("Inserted: {}".format(inscount))
    logger.debug("Found: {}".format(foundcoconut))
    logger.debug("Errors: {}".format(errcount))
    logger.debug("-------------------------------")
    # left join traitdescrips_uni to main df on traitdescripidstr
    traitdescrips_uni = traitdescrips_uni[["traitdescripidstr", "traitdescriptionid"]]
    datafile = pd.merge(datafile, traitdescrips_uni, on="traitdescripidstr", how="left")

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                    SOURCE INFO SETUP                                    │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Extract source info (incl. contrib & citation ids)
    logger.info("Extracting source information...")
    source_names = ["originalid", "figuretable", "submittedby", "contributoremail",
                    "citation", "doi", "published", "embargorelease", "sourceinfoidstr"]
    source = datafile[source_names]
    source_uni = source.drop_duplicates().reset_index(drop=True)
    source_uni["sourceinfoid"] = np.int(-1)

    source_uni["contributoridstr"] = np.vectorize(idcat)(source_uni.submittedby, source_uni.contributoremail)
    source_uni["citationidstr"] = np.vectorize(idcat)(source_uni.citation, source_uni.doi,
                                                      source_uni.published, source_uni.embargorelease)

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                       CONTRIBUTORS                                      │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Extract contributor
    logger.info("Extracting contributors...")
    contrib_names = ["submittedby", "contributoremail", "contributoridstr"]
    contrib = source_uni[contrib_names]
    contrib_uni = contrib.drop_duplicates().reset_index(drop=True)
    contrib_uni["contributorid"] = np.int(-1)

    inscount = 0
    foundcoconut = 0
    errcount = 0
    for index, entry in contrib_uni.iterrows():
        contributorid = np.nan
        search = db2(
            (db2.contributor.submittedby == noneadapter(entry.submittedby)) &
            (db2.contributor.contributoremail == noneadapter(entry.contributoremail))
        ).select(db2.contributor.contributorid)
        if len(search) < 1:
            # insert into db
            inscount += 1
            contributorid = db2.contributor.insert(submittedby=noneadapter(entry.submittedby),
                                                   contributoremail=noneadapter(entry.contributoremail))
            logger.debug("Inserted contributor id {}".format(contributorid))
        elif len(search) == 1:
            # Use the found id
            foundcoconut += 1
            contributorid = search[0].contributorid
        else:
            errcount += 1
            logger.warning("Ambiguous contributor entry provided:\n\n{}\n\n{}".format(entry, search))
            contributorid = search[0].contributorid

        contrib_uni.ix[index, "contributorid"] = contributorid

    logger.debug("---- TABLE: contributor ----")
    logger.debug("Inserted: {}".format(inscount))
    logger.debug("Found: {}".format(foundcoconut))
    logger.debug("Errors: {}".format(errcount))
    logger.debug("----------------------------")
    # left join contrib_uni to source df on contributoridstr
    contrib_uni = contrib_uni[["contributoridstr", "contributorid"]]
    source_uni = pd.merge(source_uni, contrib_uni, on="contributoridstr", how="left")

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                        CITATIONS                                        │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Extract citation
    logger.info("Extracting citations...")
    citation_names = ["citation", "doi", "published", "embargorelease", "citationidstr"]
    citation = source_uni[citation_names]
    citation_uni = citation.drop_duplicates().reset_index(drop=True)
    citation_uni["citationid"] = np.int(-1)

    inscount = 0
    foundcoconut = 0
    errcount = 0
    for index, entry in citation_uni.iterrows():
        citationid = np.nan
        search = db2(
            (db2.citation.citation == noneadapter(entry.citation)) &
            (db2.citation.doi == noneadapter(entry.doi)) &
            (db2.citation.published == noneadapter(entry.published)) &
            (db2.citation.embargorelease == noneadapter(entry.embargorelease))
        ).select(db2.citation.citationid)
        if len(search) < 1:
            # insert into db
            inscount += 1
            citationid = db2.citation.insert(citation=noneadapter(entry.citation),
                                             doi=noneadapter(entry.doi),
                                             published=noneadapter(entry.published),
                                             embargorelease=noneadapter(entry.embargorelease))
            logger.debug("Inserted citation id {}".format(citationid))
        elif len(search) == 1:
            # Use the found id
            foundcoconut += 1
            citationid = search[0].citationid
        else:
            errcount += 1
            logger.warning("Ambiguous citation entry provided:\n\n{}\n\n{}".format(entry, search))
            citationid = search[0].citationid

        citation_uni.ix[index, "citationid"] = citationid

    logger.debug("----- TABLE: citation ------")
    logger.debug("Inserted: {}".format(inscount))
    logger.debug("Found: {}".format(foundcoconut))
    logger.debug("Errors: {}".format(errcount))
    logger.debug("----------------------------")
    # left join contrib_uni to source df on contributoridstr
    citation_uni = citation_uni[["citationidstr", "citationid"]]
    source_uni = pd.merge(source_uni, citation_uni, on="citationidstr", how="left")

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                    SOURCE INFO UPLOAD                                   │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    inscount = 0
    foundcoconut = 0
    errcount = 0
    for index, entry in source_uni.iterrows():
        sourceinfoid = np.nan
        search = db2(
            (db2.sourceinfo.originalid == noneadapter(entry.originalid)) &
            (db2.sourceinfo.contributorid == noneadapter(entry.contributorid)) &
            (db2.sourceinfo.citationid == noneadapter(entry.citationid)) &
            (db2.sourceinfo.figuretable == noneadapter(entry.figuretable))
        ).select(db2.sourceinfo.sourceid)
        if len(search) < 1:
            # insert into db
            inscount += 1
            sourceinfoid = db2.sourceinfo.insert(originalid=noneadapter(entry.originalid),
                                                 contributorid=noneadapter(entry.contributorid),
                                                 citationid=noneadapter(entry.citationid),
                                                 figuretable=noneadapter(entry.figuretable))
            logger.debug("Inserted source info id {}".format(sourceinfoid))
        elif len(search) == 1:
            # Use the found id
            foundcoconut += 1
            sourceinfoid = search[0].sourceid
        else:
            errcount += 1
            logger.warning("Ambiguous source info entry provided:\n\n{}\n\n{}".format(entry, search))
            sourceinfoid = search[0].sourceid

        source_uni.ix[index, "sourceinfoid"] = sourceinfoid

    logger.debug("---- TABLE: sourceinfo -----")
    logger.debug("Inserted: {}".format(inscount))
    logger.debug("Found: {}".format(foundcoconut))
    logger.debug("Errors: {}".format(errcount))
    logger.debug("----------------------------")
    # left join source_uni to main df on sourceinfoidstr
    source_uni = source_uni[["sourceinfoidstr", "sourceinfoid"]]
    datafile = pd.merge(datafile, source_uni, on="sourceinfoidstr", how="left")

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                        EXP COND                                         │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Extract experimental conditions
    logger.info("Extracting experimental conditions...")
    expcond_names = ["replicates", "habitat", "labfield", "arenavalue", "arenaunit", "arenavaluesi", "arenaunitsi",
                     "resrepvalue", "resrepunit", "resrepvaluesi", "resrepunitsi", "expcondidstr"]
    expcond = datafile[expcond_names]
    expcond_uni = expcond.drop_duplicates().reset_index(drop=True)
    expcond_uni["expcondid"] = np.int(-1)

    # logger.debug(locations_uni)
    inscount = 0
    foundcoconut = 0
    errcount = 0
    for index, entry in expcond_uni.iterrows():
        expcondid = np.nan
        search = db2(
            (db2.experimentalconditions.replicates == noneadapter(entry.replicates)) &
            (db2.experimentalconditions.habitat == noneadapter(entry.habitat)) &
            (db2.experimentalconditions.labfield == noneadapter(entry.labfield)) &
            (db2.experimentalconditions.arenavalue == noneadapter(entry.arenavalue)) &
            (db2.experimentalconditions.arenaunit == noneadapter(entry.arenaunit)) &
            (db2.experimentalconditions.arenavaluesi == noneadapter(entry.arenavaluesi)) &
            (db2.experimentalconditions.arenaunitsi == noneadapter(entry.arenaunitsi)) &
            (db2.experimentalconditions.resrepvalue == noneadapter(entry.resrepvalue)) &
            (db2.experimentalconditions.resrepunit == noneadapter(entry.resrepunit)) &
            (db2.experimentalconditions.resrepvaluesi == noneadapter(entry.resrepvaluesi)) &
            (db2.experimentalconditions.resrepunitsi == noneadapter(entry.resrepunitsi))
        ).select(db2.experimentalconditions.experimentid)
        if len(search) < 1:
            # insert into db
            inscount += 1
            expcondid = db2.experimentalconditions.insert(replicates=noneadapter(entry.replicates),
                                                          habitat=noneadapter(entry.habitat),
                                                          labfield=noneadapter(entry.labfield),
                                                          arenavalue=noneadapter(entry.arenavalue),
                                                          arenaunit=noneadapter(entry.arenaunit),
                                                          arenavaluesi=noneadapter(entry.arenavaluesi),
                                                          arenaunitsi=noneadapter(entry.arenaunitsi),
                                                          resrepvalue=noneadapter(entry.resrepvalue),
                                                          resrepunit=noneadapter(entry.resrepunit),
                                                          resrepvaluesi=noneadapter(entry.resrepvaluesi),
                                                          resrepunitsi=noneadapter(entry.resrepunitsi))
            logger.debug("Inserted experimentalconditions id {}".format(expcondid))
        elif len(search) == 1:
            # Use the found id
            foundcoconut += 1
            expcondid = search[0].experimentid
        else:
            errcount += 1
            # logger.warning("Ambiguous experimentalconditions entry provided:\n\n{}\n\n{}".format(entry, search))
            expcondid = search[0].experimentid

        expcond_uni.ix[index, "expcondid"] = expcondid

    logger.debug("--- TABLE: experimentalconditions ---")
    logger.debug("Inserted: {}".format(inscount))
    logger.debug("Found: {}".format(foundcoconut))
    logger.debug("Errors: {}".format(errcount))
    logger.debug("-------------------------------------")
    # left join expcond_uni to main df on expcondidstr
    expcond_uni = expcond_uni[["expcondidstr", "expcondid"]]
    datafile = pd.merge(datafile, expcond_uni, on="expcondidstr", how="left")

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                        MAIN TABLE                                       │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Make maintable (incl ids for all other tables)
    logger.info("Creating maintable data entries...")
    maintable_names = ['originalid', 'originaltraitname', 'originaltraitdef', 'standardisedtraitname',
                       'standardisedtraitdef', 'originaltraitvalue', 'originaltraitunit', 'originalerrorpos',
                       'originalerrorneg', 'originalerrorunit', 'standardisedtraitvalue', 'standardisedtraitunit',
                       'standardisederrorpos', 'standardisederrorneg', 'standardisederrorunit', 'ambienttemp',
                       'ambienttempmethod', 'ambienttempunit', 'ambientlight', 'ambientlightunit', 'secondstressor',
                       'secondstressordef', 'secondstressorvalue', 'secondstressorunit', 'timestart', 'timeend',
                       'totalobstimevalue', 'totalobstimeunit', 'totalobstimevaluesi', 'totalobstimeunitsi',
                       'totalobstimenotes', 'interactor1', 'interactor1common', 'interactor1wholepart',
                       'interactor1wholeparttype', 'interactor1number', 'interactor1stage', 'interactor1temp',
                       'interactor1tempunit', 'interactor1tempmethod', 'interactor1growthtemp',
                       'interactor1growthtempunit', 'interactor1growthdur', 'interactor1growthdurunit',
                       'interactor1growthtype', 'interactor1acc', 'interactor1acctemp', 'interactor1acctempnotes',
                       'interactor1acctime', 'interactor1acctimenotes', 'interactor1acctimeunit', 'interactor1origtemp',
                       'interactor1origtempnotes', 'interactor1origtime', 'interactor1origtimenotes',
                       'interactor1origtimeunit', 'interactor1equilibtimevalue', 'interactor1equilibtimeunit',
                       'interactor1size', 'interactor1sizeunit', 'interactor1sizetype', 'interactor1sizesi',
                       'interactor1sizeunitsi', 'interactor1denvalue', 'interactor1denunit', 'interactor1dentypesi',
                       'interactor1denvaluesi', 'interactor1denunitsi', 'interactor1massvaluesi',
                       'interactor1massunitsi', 'interactor2', 'interactor2common', 'interactor2stage',
                       'interactor2temp', 'interactor2tempunit', 'interactor2tempmethod', 'interactor2growthtemp',
                       'interactor2growthtempunit', 'interactor2growthdur', 'interactor2growthdurunit',
                       'interactor2growthtype', 'interactor2acc', 'interactor2acctemp', 'interactor2acctempnotes',
                       'interactor2acctime', 'interactor2acctimenotes', 'interactor2acctimeunit', 'interactor2origtemp',
                       'interactor2origtempnotes', 'interactor2origtime', 'interactor2origtimenotes',
                       'interactor2origtimeunit', 'interactor2equilibtimevalue', 'interactor2equilibtimeunit',
                       'interactor2size', 'interactor2sizeunit', 'interactor2sizetype', 'interactor2sizesi',
                       'interactor2sizeunitsi', 'interactor2denvalue', 'interactor2denunit', 'interactor2dentypesi',
                       'interactor2denvaluesi', 'interactor2denunitsi', 'interactor2massvaluesi',
                       'interactor2massunitsi', 'locationid', 'interactor1id', 'interactor2id', 'traitdescriptionid',
                       'sourceinfoid', 'expcondid', 'notes']
    maintable = datafile[maintable_names]

    # ┌─────────────────────────────────────────────────────────────────────────────────────────┐ #
    # │                                         UPLOAD                                          │ #
    # └─────────────────────────────────────────────────────────────────────────────────────────┘ #

    # Upload to db
    logger.info("Uploading data to db...")
    inscount = 0
    log_triggers = {}
    short_dataset = True

    if len(maintable) > 100:
        short_dataset = False
        trigger_list = [int(len(maintable) * (x / float(10))) - 1 for x in range(0, 11)]
        trigger_list[0] = 0
        percentile_list = [x * 10 for x in range(0, 11)]
        log_triggers = dict(zip(trigger_list, percentile_list))

    for index, entry in maintable.iterrows():
        if not short_dataset:
            if index in log_triggers.keys():
                logger.info('Uploading row {}/{} ({}%)...'.format(index + 1, len(maintable), log_triggers[index]))
        # insert into db
        inscount += 1
        mainid = db2.maintable.insert(
            originalid=noneadapter(entry.originalid),
            originaltraitname=noneadapter(entry.originaltraitname),
            originaltraitdef=noneadapter(entry.originaltraitdef),
            standardisedtraitname=noneadapter(entry.standardisedtraitname),
            standardisedtraitdef=noneadapter(entry.standardisedtraitdef),
            originaltraitvalue=noneadapter(entry.originaltraitvalue),
            originaltraitunit=noneadapter(entry.originaltraitunit),
            originalerrorpos=noneadapter(entry.originalerrorpos),
            originalerrorneg=noneadapter(entry.originalerrorneg),
            originalerrorunit=noneadapter(entry.originalerrorunit),
            standardisedtraitvalue=noneadapter(entry.standardisedtraitvalue),
            standardisedtraitunit=noneadapter(entry.standardisedtraitunit),
            standardisederrorpos=noneadapter(entry.standardisederrorpos),
            standardisederrorneg=noneadapter(entry.standardisederrorneg),
            standardisederrorunit=noneadapter(entry.standardisederrorunit),
            ambienttemp=noneadapter(entry.ambienttemp),
            ambienttempmethod=noneadapter(entry.ambienttempmethod),
            ambienttempunit=noneadapter(entry.ambienttempunit),
            ambientlight=noneadapter(entry.ambientlight),
            ambientlightunit=noneadapter(entry.ambientlightunit),
            secondstressor=noneadapter(entry.secondstressor),
            secondstressordef=noneadapter(entry.secondstressordef),
            secondstressorvalue=noneadapter(entry.secondstressorvalue),
            secondstressorunit=noneadapter(entry.secondstressorunit),
            timestart=noneadapter(entry.timestart),
            timeend=noneadapter(entry.timeend),
            totalobstimevalue=noneadapter(entry.totalobstimevalue),
            totalobstimeunit=noneadapter(entry.totalobstimeunit),
            totalobstimevaluesi=noneadapter(entry.totalobstimevaluesi),
            totalobstimeunitsi=noneadapter(entry.totalobstimeunitsi),
            totalobstimenotes=noneadapter(entry.totalobstimenotes),
            interactor1=noneadapter(entry.interactor1),
            interactor1common=noneadapter(entry.interactor1common),
            interactor1wholepart=noneadapter(entry.interactor1wholepart),
            interactor1wholeparttype=noneadapter(entry.interactor1wholeparttype),
            interactor1number=noneadapter(entry.interactor1number),
            interactor1stage=noneadapter(entry.interactor1stage),
            interactor1temp=noneadapter(entry.interactor1temp),
            interactor1tempunit=noneadapter(entry.interactor1tempunit),
            interactor1tempmethod=noneadapter(entry.interactor1tempmethod),
            interactor1growthtemp=noneadapter(entry.interactor1growthtemp),
            interactor1growthtempunit=noneadapter(entry.interactor1growthtempunit),
            interactor1growthdur=noneadapter(entry.interactor1growthdur),
            interactor1growthdurunit=noneadapter(entry.interactor1growthdurunit),
            interactor1growthtype=noneadapter(entry.interactor1growthtype),
            interactor1acc=noneadapter(entry.interactor1acc),
            interactor1acctemp=noneadapter(entry.interactor1acctemp),
            interactor1acctempnotes=noneadapter(entry.interactor1acctempnotes),
            interactor1acctime=noneadapter(entry.interactor1acctime),
            interactor1acctimenotes=noneadapter(entry.interactor1acctimenotes),
            interactor1acctimeunit=noneadapter(entry.interactor1acctimeunit),
            interactor1origtemp=noneadapter(entry.interactor1origtemp),
            interactor1origtempnotes=noneadapter(entry.interactor1origtempnotes),
            interactor1origtime=noneadapter(entry.interactor1origtime),
            interactor1origtimenotes=noneadapter(entry.interactor1origtimenotes),
            interactor1origtimeunit=noneadapter(entry.interactor1origtimeunit),
            interactor1equilibtimevalue=noneadapter(entry.interactor1equilibtimevalue),
            interactor1equilibtimeunit=noneadapter(entry.interactor1equilibtimeunit),
            interactor1size=noneadapter(entry.interactor1size),
            interactor1sizeunit=noneadapter(entry.interactor1sizeunit),
            interactor1sizetype=noneadapter(entry.interactor1sizetype),
            interactor1sizesi=noneadapter(entry.interactor1sizesi),
            interactor1sizeunitsi=noneadapter(entry.interactor1sizeunitsi),
            interactor1denvalue=noneadapter(entry.interactor1denvalue),
            interactor1denunit=noneadapter(entry.interactor1denunit),
            interactor1dentypesi=noneadapter(entry.interactor1dentypesi),
            interactor1denvaluesi=noneadapter(entry.interactor1denvaluesi),
            interactor1denunitsi=noneadapter(entry.interactor1denunitsi),
            interactor1massvaluesi=noneadapter(entry.interactor1massvaluesi),
            interactor1massunitsi=noneadapter(entry.interactor1massunitsi),
            interactor2=noneadapter(entry.interactor2),
            interactor2common=noneadapter(entry.interactor2common),
            interactor2stage=noneadapter(entry.interactor2stage),
            interactor2temp=noneadapter(entry.interactor2temp),
            interactor2tempunit=noneadapter(entry.interactor2tempunit),
            interactor2tempmethod=noneadapter(entry.interactor2tempmethod),
            interactor2growthtemp=noneadapter(entry.interactor2growthtemp),
            interactor2growthtempunit=noneadapter(entry.interactor2growthtempunit),
            interactor2growthdur=noneadapter(entry.interactor2growthdur),
            interactor2growthdurunit=noneadapter(entry.interactor2growthdurunit),
            interactor2growthtype=noneadapter(entry.interactor2growthtype),
            interactor2acc=noneadapter(entry.interactor2acc),
            interactor2acctemp=noneadapter(entry.interactor2acctemp),
            interactor2acctempnotes=noneadapter(entry.interactor2acctempnotes),
            interactor2acctime=noneadapter(entry.interactor2acctime),
            interactor2acctimenotes=noneadapter(entry.interactor2acctimenotes),
            interactor2acctimeunit=noneadapter(entry.interactor2acctimeunit),
            interactor2origtemp=noneadapter(entry.interactor2origtemp),
            interactor2origtempnotes=noneadapter(entry.interactor2origtempnotes),
            interactor2origtime=noneadapter(entry.interactor2origtime),
            interactor2origtimenotes=noneadapter(entry.interactor2origtimenotes),
            interactor2origtimeunit=noneadapter(entry.interactor2origtimeunit),
            interactor2equilibtimevalue=noneadapter(entry.interactor2equilibtimevalue),
            interactor2equilibtimeunit=noneadapter(entry.interactor2equilibtimeunit),
            interactor2size=noneadapter(entry.interactor2size),
            interactor2sizeunit=noneadapter(entry.interactor2sizeunit),
            interactor2sizetype=noneadapter(entry.interactor2sizetype),
            interactor2sizesi=noneadapter(entry.interactor2sizesi),
            interactor2sizeunitsi=noneadapter(entry.interactor2sizeunitsi),
            interactor2denvalue=noneadapter(entry.interactor2denvalue),
            interactor2denunit=noneadapter(entry.interactor2denunit),
            interactor2dentypesi=noneadapter(entry.interactor2dentypesi),
            interactor2denvaluesi=noneadapter(entry.interactor2denvaluesi),
            interactor2denunitsi=noneadapter(entry.interactor2denunitsi),
            interactor2massvaluesi=noneadapter(entry.interactor2massvaluesi),
            interactor2massunitsi=noneadapter(entry.interactor2massunitsi),
            locationid=noneadapter(entry.locationid),
            interactor1id=noneadapter(entry.interactor1id),
            interactor2id=noneadapter(entry.interactor2id),
            traitdescriptionid=noneadapter(entry.traitdescriptionid),
            sourceinfoid=noneadapter(entry.sourceinfoid),
            expcondid=noneadapter(entry.expcondid),
            notes=noneadapter(entry.notes),
        )

    logger.debug("----- TABLE: maintable -----")
    logger.debug("Inserted: {}".format(inscount))
    logger.debug("----------------------------")
    logger.info("Data upload complete.")
    logger.info("Adding successful hash to db")
    hashid = db2.dataset_hash.insert(filehash=filemd5,
                                     filename=basename(csvpath)[:128])
    logger.info(asciilogo())
    return True


def eod_upload_run(logger=False):
    """Upload all validated datafiles, then move to 'complete' when complete or 'errored' when errored."""
    import os
    import time
    import shutil
    import logzero
    if not logger:
        logger = logzero.setup_logger(logfile="logs/vtuploads.log",
                                      formatter=logging.Formatter(
                                          '%(asctime)s - %(levelname)-7s - %(funcName)s - %(message)s'),
                                      disableStderrLogger=True)
        logger.info("Turned on logger in eod_upload_run")

    success = True

    # Load db connection
    db2 = current.db2

    logger.info("Starting upload run at {}".format(time.strftime("%H:%M:%S", time.gmtime())))

    # Find all files in validated and set up paths
    cwd = os.getcwd()
    logger.info("CWD: {}".format(cwd))     # Just to check that the cwd is where we think it is when the scheduler is run...
    uploadpath = os.path.join(cwd, "applications/VectorBiteDataPlatform/uploads")
    validatedpath = os.path.join(uploadpath, "validated")
    successpath = os.path.join(uploadpath, "completed")
    failpath = os.path.join(uploadpath, "errored")
    templatepath = os.path.join(cwd, "applications/VectorBiteDataPlatform/static/templates/vectraits_template.csv")
    uploadfiles = [f for f in os.listdir(validatedpath) if os.path.isfile(os.path.join(validatedpath, f))]
    logger.debug("Files to upload: {}".format(uploadfiles))

    # Run upload_vectraits_dataset on each file
    for candidatefile in uploadfiles:
        candidatepath = os.path.join(validatedpath, candidatefile)
        logger.info("Starting upload of {}".format(candidatepath))
        uploadsuccess = False

        try:
            uploadsuccess = upload_vectraits_dataset(candidatepath, templatepath, logger)
            db2.commit()
        except VTUploadError:
            logger.exception("Handled error encountered when processing {}".format(candidatefile))
            success = False
            db2.rollback()
        except Exception:
            logger.exception("Unhandled error encountered when processing {}".format(candidatefile))
            success = False
            db2.rollback()

        try:
            if uploadsuccess:
                logger.info("Upload successful")
                shutil.move(candidatepath, os.path.join(successpath, candidatefile))
            else:
                logger.info("Upload failed")
                shutil.move(candidatepath, os.path.join(failpath, candidatefile))
        except IOError:
            logger.exception("File move failed, remains in validated folder.")

    logger.info("Completed upload run at {}".format(time.strftime("%H:%M:%S", time.gmtime())))
    return success


if __name__ == "__main__":
    # run testing code
    import time

    moduledebug = True

    if moduledebug:
        import logzero

        logger = logzero.setup_logger(logfile="/tmp/vtfuncsdebug.log",
                                      formatter=logging.Formatter(
                                          '%(asctime)s - %(levelname)-7s - %(funcName)s - %(message)s'),
                                      level=logging.DEBUG
                                      )
    else:
        logger = logging.getLogger("web2py.app.vbdp")

    logger.info("Test commencing at {}".format(time.strftime("%H:%M:%S", time.gmtime())))
    # upload_vectraits_dataset("applications/VectorBiteDataPlatform/uploads/tests/passing_superlong.csv",
    #                          "applications/VectorBiteDataPlatform/static/templates/vectraits_template.csv")
    eod_upload_run(logger)
    logger.info("Test completed at {}".format(time.strftime("%H:%M:%S", time.gmtime())))
