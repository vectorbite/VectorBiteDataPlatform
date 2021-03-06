import sys
import csv
from applications.VectorBiteDataPlatform.modules.vecdyn_validator_script import *

vecdyn_field_names = ('taxon', 'location_description', 'study_collection_area', 'geo_datum',
                      'gps_obfuscation_info', 'species_id_method', 'study_design', 'sampling_strategy',
                      'sampling_method', 'sampling_protocol', 'measurement_unit', 'value_transform',
                      'sample_start_date', 'sample_start_time',
                      'sample_end_date', 'sample_end_time', 'sample_value', 'sample_sex',
                      'sample_stage', 'sample_location', 'sample_collection_area', 'sample_lat_dd',
                      'sample_long_dd', 'sample_environment', 'additional_location_info',
                      'additional_sample_info', 'sample_name')

with open('vecdyn_mcm_2012.csv', 'r') as csvfile:
    # pass the file object to reader() to get the reader object

    csvfile = csv.reader(csvfile)
    # Get all rows of csv from csv_reader object as list of tuples
    #csvfile = list(map(tuple, csvfile))
    # a simple validator to be tested
    validator = CSVValidator(vecdyn_field_names)
    # basic header and record length checks
    validator.add_header_check('dataset_check', 'bad header')

    validator.add_value_check('taxon', datatype_required(str),
                              'taxon error', 'entry must not be empty and =< 250 characters')
    validator.add_value_check('location_description', datatype_required(str),
                              'location_description error', 'entry must not be empty  and =< 250 characters')
    validator.add_value_check('study_collection_area', datatype_not_required(str),
                              'study_collection_area error', 'entry must be string and =< 250 characters')
    validator.add_value_check('geo_datum', datatype_not_required(str),
                              'geo_datum error', 'entry must be string and =< 250 characters')
    validator.add_value_check('gps_obfuscation_info', datatype_not_required(str),
                              'gps_obfuscation_info', 'entry must be string and =< 250 characters')
    validator.add_value_check('species_id_method', datatype_not_required(str),
                              'species_id_method error', 'entry must be string and =< 250 characters')
    validator.add_value_check('study_design', datatype_not_required(str),
                              'study_design', 'entry must be string and =< 250 characters')
    validator.add_value_check('sampling_strategy', datatype_not_required(str),
                              'sampling_strategy error', 'entry must be string and =< 250 characters')
    validator.add_value_check('sampling_method', datatype_not_required(str),
                              'sampling_method error', 'entry must be string and =< 250 characters')
    validator.add_value_check('sampling_protocol', datatype_not_required(str),
                              'sampling_protocol error', 'entry must be string and =< 250 characters')
    validator.add_value_check('sampling_method', datatype_not_required(str),
                              'sampling_method error', 'entry must be string and =< 250 characters')
    validator.add_value_check('measurement_unit', datatype_not_required(str),
                              'measurement_unit error', 'entry must be string and =< 250 characters')
    validator.add_value_check('sample_start_date', datetime_string_not_required('%Y-%m-%d'),
                              'sample_start_date error', 'entry must be in date format: %Y-%m-%d')
    validator.add_value_check('sample_start_time', datetime_string_not_required('%H:%M:%S'),
                              'sample_start_time error', 'entry must be in time format: %H:%M:%S')
    validator.add_value_check('sample_end_date', datetime_string('%Y-%m-%d'),
                              'sample_end_date error', 'entry must be in date format: %Y-%m-%d')
    validator.add_value_check('sample_end_time', datetime_string_not_required('%H:%M:%S'),
                              'sample_end_time error', 'entry must be in time format: %H:%M:%S')
    validator.add_value_check('sample_value', float_or_int_required(),
                              'sample_value error', 'entry must be numeric')
    validator.add_value_check('sample_sex', datatype_not_required(str),
                              'sample_sex error', 'entry must be string and =< 250 characters')
    validator.add_value_check('sample_stage', datatype_not_required(str),
                              'sample_stage error', 'entry must be string and =< 250 characters')
    validator.add_value_check('sample_location', datatype_not_required(str),
                              'sample_location error', 'entry must be string and =< 250 characters')
    validator.add_value_check('sample_collection_area', datatype_not_required(str),
                              'sample_collection_area error', 'entry must be string and =< 250 characters')
    validator.add_value_check('sample_lat_dd', float,
                              'sample_lat_dd error', 'sample_long_dd must be a float or not empty')
    validator.add_value_check('sample_long_dd', float,
                              'sample_long_dd error', 'sample_long_dd must be a float or not empty')
    validator.add_value_check('sample_environment', datatype_not_required(str),
                              'sample_environment error', 'entry must be string and =< 250 characters')
    validator.add_value_check('additional_location_info', datatype_not_required(str),
                              'additional_location_info error', 'entry must be string and =< 250 charactersg')
    validator.add_value_check('additional_sample_info', datatype_not_required(str),
                              'additional_sample_info error', 'entry must be string and =< 250 characters')
    validator.add_value_check('sample_name', datatype_not_required(str),
                              'sample_name error', 'entry must be string and =< 250 characters')

    # run the validator on the test data
    problems = validator.ivalidate(csvfile)

    # validate the data and write problems to stdout
    write_problems(problems, sys.stdout)