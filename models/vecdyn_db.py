# -*- coding: utf-8 -*-

db.define_table('csvfile',
                    Field('csv', 'upload', default='path/'))



db.define_table('person',
                    Field('name'),
                    Field('age'),
                    Field('country'),
                    format='%(name)s')

db.define_table('thing',
                    Field('person_id', 'reference person'),
                    Field('thing_name'),
                    Field('value'),
                    Field('location'))
# VecDyn

###add ondelete='CASCADE' to these tables, so

db.define_table('collection_info',
                Field('title', unique=True, type='string', required=True, comment ='Short title identifying the data collection'),
                Field('collection_authority', comment='Name of collection authority'),
                Field('DOI', type='string', comment = 'Digital Object Identifier'),
                Field('publication_date', type='date'),
                Field('description', type='text',  required=True, comment='Brief description of data series'),
                Field('URL', requires=IS_URL(), comment = 'web link to dataset'),
                Field('contact_name', type='string'),
                Field('contact_affiliation', type='string'),
                Field('contact_email', requires=IS_EMAIL()),
                Field('ORCID', type='string', comment = 'A digital identifier which provides researchers with a unique ID, see www.orcid.org'),
                Field('keywords', type='string', comment='Keywords for web searches, seperate each keyword with a comma'),
                auth.signature,
                common_filter = lambda query: db.collection_info.created_by == auth.user.id)

#if db(db.collection_info.id>0).count() == 0:
 #   db.collection_info.truncate()



db.define_table('study_data',
                Field('title'),
                Field('taxon'),
                Field('location_description', type = 'string', required=True,  comment='Study location description'),
                #Field('location_environment', type = 'string', comment='General description about the location'),
                #Field('study_lat_DD', type = 'double', required=True, comment='Latitude of study area as a decimal degree'),
                #Field('study_long_DD', type = 'double', required=True, comment='Longitude of study area as a decimal degree'),
                #Field('geo_datum', type='string', comment='Indicate Geodetic datum e.g. wgs 84'),
                #Field('spatial_accuracy', type = 'integer', comment='Spatial accuracy of the given coordinates'),
                #Field('location_extent', type = 'string', comment='Indicating the extent of the study site'),
                #Field('species_id_method', type = 'string', comment='Species Identification Method'),
                #Field('study_design', type = 'string', comment='Study design methodology'),
                #Field('sampling_strategy', type = 'string', comment='Indicate the strategy used to select the sample'),
                #Field('sampling_method', type = 'string', required=True, comment='Sampling apparatus (e.g.  trap type, observation method)'),
                #Field('sampling_protocol', type = 'string', comment='How entities were sampled'),
                #Field('measurement_unit', type = 'string', required=True, comment='Unit of measurement'),
                #Field('study_collection_area', type = 'string', comment='The spatial extent (area or volume) of the sample'),
                #Field('value_transform', type = 'string', comment='Note if the original values have been transformed')
                Field('taxon_id'),
                Field('location_ID'),
                Field('collection_info_id'))

if db(db.study_data.id>0).count() == 0:
    db.study_data.truncate()

db.define_table('sample_data',
                Field('study_data_id', 'reference study_data'), #length=1, default=""),
                Field('sample_start_date', type = 'date', required=False, comment='date of sample was set, leave blank if not applicable to the study'),
                #Field('sample_start_time'))#, type = 'time', required=False, comment='time of sample was set, leave blank if not applicable to the study'),
                Field('sample_end_date', type = 'date', requires=IS_DATE(), comment='Date of sample collection'))
                #Field('sample_end_time', type = 'time', required=False, comment='time of sample collection'),
                #Field('value', type = 'integer', comment='The numerical amount or result from the sample collection'),
                #Field('sample_sex', type = 'string', comment='sex of sample if applicable'),
                #Field('sample_info', type = 'string', comment='Additional sample information'),
                #Field('sample_location_info', type = 'string', comment='Additional sample information'),
                #Field('sample_lat_DD', type = 'string', comment='Latitude of sample area as a decimal degree'),
                #Field('sample_long_DD', type = 'string', comment='Longitude of sample area as a decimal degree'),
                #Field('sample_name', type = 'string', comment ='A human readable sample name'))

if db(db.sample_data.id>0).count() == 0:
    db.sample_data.truncate()

