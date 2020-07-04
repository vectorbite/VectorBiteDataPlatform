import sys
import csv
from vecdyn_csv_validator import *
import os
import cStringIO
from gluon.serializers import xml


vecdyn_field_names = ('taxon', 'location_description', 'study_collection_area', 'geo_datum',
                      'gps_obfuscation_info', 'species_id_method', 'study_design', 'sampling_strategy',
                      'sampling_method', 'sampling_protocol', 'measurement_unit', 'value_transform',
                      'sample_start_date', 'sample_start_time',
                      'sample_end_date', 'sample_end_time', 'sample_value', 'sample_sex',
                      'sample_stage', 'sample_location', 'sample_collection_area', 'sample_lat_dd',
                      'sample_long_dd', 'sample_environment', 'additional_location_info',
                      'additional_sample_info', 'sample_name')

def vecdyn_csv_checker():
    form = SQLFORM(db.vecdyn_validator, comments=False, fields=['csvfile'],
                   labels={'csvfile': 'Click to search and select a file:'})
    if form.process().accepted:
        session.flash = 'Validating, please wait'
        filename, csvfile = db.vecdyn_validator.csvfile.retrieve(form.vars.csvfile)
        csvfile = csv.reader(csvfile)
        # Get all rows of csv from csv_reader object as list of tuples
        csvfile = list(map(tuple, csvfile))
        # a simple validator to be tested
        validator = CSVValidator(vecdyn_field_names)

        validator.add_value_check('taxon',string_required(str),
                                  'taxon error', 'Taxon entry must be a string')
        # validator.add_value_check('location_description', str,
        #                           'location_description error', 'entry must be a string')
        # validator.add_value_check('study_collection_area', datatype_not_required(float),
        #                            'study_collection_area', 'entry must be a string')
        # validator.add_value_check('geo_datum', datatype_not_required(str),
        #                           'geo_datum error', 'entry must be a string')
        # validator.add_value_check('gps_obfuscation_info', datatype_not_required(str),
        #                           'gps_obfuscation_info', 'entry must be a string')
        # validator.add_value_check('species_id_method', datatype_not_required(str),
        #                           'species_id_method', 'entry must be a string')
        # validator.add_value_check('study_design', datatype_not_required(str),
        #                           'study_design', 'entry must be a string')
        # validator.add_value_check('sampling_strategy', datatype_not_required(str),
        #                           'sampling_strategy', 'entry must be a string')
        # validator.add_value_check('sampling_method', datatype_not_required(str),
        #                           'sampling_method', 'entry must be a string')
        # validator.add_value_check('sampling_protocol', datatype_not_required(str),
        #                           'sampling_protocol', 'entry must be a string')
        # validator.add_value_check('sampling_method', datatype_not_required(str),
        #                           'sampling_method', 'entry must be a string')
        # validator.add_value_check('measurement_unit', datatype_not_required(str),
        #                           'measurement_unit', 'entry must be a string')
        # validator.add_value_check('sample_start_date', datetime_string('%Y-%m-%d'),
        #                           'value_transform', 'entry must be a string')
        # validator.add_value_check('sample_start_time', datetime_string('%hh:%mm:%ss'),
        #                           'sampling_method', 'entry must be a string')
        # validator.add_value_check('taxon', datatype_not_required(),
        #                           'foo', 'not an integer')
        # validator.add_value_check('bar', not_required_datatype(float),
        #                           'bar', 'not a float')


        summarize = False
        limit = 0
        # some test data
        problems = validator.validate(csvfile)
        """
            Write problems as restructured text to a file (or stdout/stderr).
            """
        #file = open('myfile.txt', 'w')
        file = cStringIO.StringIO()
        w = file.write  # convenience variable
        w("""
        =================
        Vecdyn Validation Report
        =================
        """)
        counts = dict()  # store problem counts per problem code
        total = 0
        for i, p in enumerate(problems):
            if limit and i >= limit:
                break  # bail out
            if total == 0 and not summarize:
                w("""
        Problems
        ========
        """)
            total += 1
            code = p['code']
            if code in counts:
                counts[code] += 1
            else:
                counts[code] = 1
            if not summarize:
                ptitle = '\n%s - %s\n' % (p['code'], p['message'])
                w(ptitle)
                underline = ''
                for i in range(len(ptitle.strip())):
                    underline += '-'
                underline += '\n'
                w(underline)
                for k in sorted(p.viewkeys() - set(['code', 'message', 'context'])):
                    w(':%s: %s\n' % (k, p[k]))
                if 'context' in p:
                    c = p['context']
                    for k in sorted(c.viewkeys()):
                        w(':%s: %s\n' % (k, c[k]))

        w("""
        Summary
        =======
        Found %s%s problem%s in total.
        """ % ('at least ' if limit else '', total, 's' if total != 1 else ''))
        for code in sorted(counts.viewkeys()):
            w(':%s: %s\n' % (code, counts[code]))
        file.seek(0)  # <---
        #return file
        return response.stream(file, attachment=True, filename='Vecdyn-Validation-Report.txt')
    return locals()

