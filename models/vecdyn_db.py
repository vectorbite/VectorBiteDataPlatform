# -*- coding: utf-8 -*-


# VecDyn

###add ondelete='CASCADE' to these tables, so


db.define_table('data_set_upload',
                Field('csvfile','upload',uploadfield=False, requires = IS_UPLOAD_FILENAME(extension='csv')))

DATARIGHTS = ('Open', 'Embargo', 'Closed')

DATATYPE = ('Abundance', 'Presence/Absence')

db.define_table('publication_info',
                Field('title', unique=True, type='string', required=True, comment ='Short title identifying the data collection'),
                Field('collection_author', comment='Name of collection authority'),
                Field('dataset_doi', type='string', comment = 'Digital Object Identifier'),
                Field('publication_doi', type='string', comment = 'Digital Object Identifier'),
                Field('description', type='text',  required=True, comment='Brief description'),
                Field('url', requires=IS_EMPTY_OR(IS_URL()), comment = 'web link to dataset'),
                Field('contact_name', type='string'),
                Field('contact_affiliation', type='string'),
                Field('email', requires=IS_EMAIL()),
                Field('orcid', type='string', comment = 'A digital identifier which provides researchers with a unique ID, see www.orcid.org'),
                Field('dataset_license', type='string'),
                Field('data_rights', requires=IS_IN_SET(DATARIGHTS), default=DATARIGHTS[2]),
                Field('embargo_release_date', type ='date', requires=IS_EMPTY_OR(IS_DATE()), comment = 'Embargo release date'),
                Field('submit', type ='boolean',default=False),
                Field('data_set_type', requires=IS_IN_SET(DATATYPE), default=DATATYPE[0]),
                auth.signature)#,
                #format='%(id)s')

###could write a query to automatically update embargo date once it reaches data >= today
today = datetime.date.today()
embargo_status_updates = db((db.publication_info.data_rights == 'Embargo') & (db.publication_info.embargo_release_date <= today)).select()
for row in embargo_status_updates:
    row.update_record(data_rights='Open', embargo_release_date=None)

def show_data_rights(data_rights,row=None):
    return SPAN(data_rights,_class=data_rights)

db.publication_info.data_rights.represent = show_data_rights


#if db(db.study_meta_data.id>0).count() == 0:
 #   db.study_meta_data.truncate()

db.define_table('study_meta_data',
                Field('title'), #0
                Field('taxon'), #1
                Field('location_description', type = 'string', required=True,  comment='Study location description'),
                Field('study_collection_area', type = 'string', comment='The spatial extent (area or volume) of the sample'), #3
                Field('geo_datum', type='string', comment='Indicate Geodetic datum e.g. wgs 84'),
                Field('gps_obfuscation_info', type='string', comment='Indicate Geodetic datum e.g. wgs 84'),#4
                Field('species_id_method', type = 'string', comment='Species Identification Method'), #5
                Field('study_design', type = 'string', comment='Study design methodology'), #6
                Field('sampling_strategy', type = 'string', comment='Indicate the strategy used to select the sample'), #7
                Field('sampling_method', type = 'string', required=True, comment='Sampling apparatus (e.g.  trap type, observation method)'), #8
                Field('sampling_protocol', type = 'string', comment='How entities were sampled'), #9
                Field('measurement_unit', type = 'string', required=True, comment='Unit of measurement'), #10
                Field('value_transform', type = 'string', comment='Note if the original values have been transformed'), #11
                Field('taxonID', default=None), #12
                Field('ADM_CODE', default=None), #13
                Field('publication_info_id', 'reference publication_info')) #14

db.study_meta_data.publication_info_id.requires = IS_IN_DB(db, db.publication_info.id)#, '%(title)s')

if db(db.study_meta_data.id>0).count() == 0:
    db.study_meta_data.truncate()


db.define_table('time_series_data',
                Field('sample_start_date', type = 'date', requires=IS_DATE(), comment='date of sample was set, leave blank if not applicable to the study'),
                Field('sample_start_time', type = 'time', required=False, comment='time of sample was set, leave blank if not applicable to the study'),
                Field('sample_end_date', type = 'date', requires=IS_DATE(), comment='Date of sample collection'),
                Field('sample_end_time', type = 'time', required=False, comment='time of sample collection'),
                Field('value'),#type = 'integer', comment='The numerical amount or result from the sample collection'),
                Field('sample_sex', type = 'string', comment='sex of sample if applicable'),
                Field('sample_stage', type = 'string', comment='life stage of sample if applicable'),
                Field('sample_location', type = 'string', comment='Additional sample information'),
                Field('sample_collection_area', type='string', comment='The spatial extent (area or volume) of the sample'),
                Field('sample_lat_dd', type = 'string', comment='Latitude of sample area as a decimal degree'),
                Field('sample_long_dd', type = 'string', comment='Longitude of sample area as a decimal degree'),
                Field('sample_environment', type = 'string', comment='General description about the sample location'),
                Field('additional_location_info', type = 'string', comment='Additional sample information'),
                Field('additional_sample_info', type = 'string', comment='Additional sample information'),
                Field('sample_name', type = 'string', comment ='A human readable sample name'),
                Field('study_meta_data_id'))


if db(db.time_series_data.id>0).count() == 0:
    db.time_series_data.truncate()




