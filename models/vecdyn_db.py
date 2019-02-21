# -*- coding: utf-8 -*-


import datetime

from gluon.tools import prettydate

week = datetime.timedelta(days=7)



db.define_table('collection_author',
    Field('name', 'string', notnull=True, unique=True),
    Field('description', 'text'),
                format='%(name)s')


# VecDyn

'''all datasets submitted thorugh the website will go into this folder'''

db.define_table('data_set_upload',
                Field('csvfile','upload',uploadfield=False, requires = IS_UPLOAD_FILENAME(extension='csv')))


DATARIGHTS = ('open', 'embargo', 'closed')

DATATYPE = ('abundance', 'presence/absence')

db.define_table('publication_info',
                Field('title', unique=True, type='string', required=True, comment ='Short title identifying the data collection'),
                Field('collection_author', db.collection_author,
                      requires=IS_IN_DB(db, 'collection_author.id', 'collection_author.name')),
                Field('dataset_doi', type='string', comment = 'Digital Object Identifier for the dataset'),
                Field('publication_doi', type='string', comment = 'If linked to a publication, enter the Digital Object Identifier of the publication'),
                Field('description', type='text',  required=True, comment='Brief description of the dataset'),
                Field('url', requires=IS_EMPTY_OR(IS_URL()), comment = 'Web link to dataset or collection author website'),
                Field('contact_name', type='string', comment = 'Lead author or best person to contact with any enquiries about the dataset'),
                Field('contact_affiliation', type='string', comment = 'Name of main organization is the contact above affiliated with'),
                Field('email', requires=IS_EMAIL()),
                Field('orcid', type='string', comment = 'Enter for name of main contact, ORCID is a digital identifier which provides researchers with a unique ID, see www.orcid.org'),
                Field('dataset_license', type='string', comment = 'e.g. Creative Commons license CC0 “No Rights Reserved”'),
                Field('data_rights', requires=IS_IN_SET(DATARIGHTS), default=DATARIGHTS[2]),
                Field('embargo_release_date', type ='date', requires=IS_EMPTY_OR(IS_DATE()), comment = 'If dataset is under embargo for a period of time please add its release date'),
                Field('data_set_type', requires=IS_IN_SET(DATATYPE), default=DATATYPE[0]),
                auth.signature)#,
                #format='%(id)s')

'''the following code updates the DATARIGHTS status,  once the  embargo date is reached it sets the dataset to open'''
today = datetime.date.today()
embargo_status_updates = db((db.publication_info.data_rights == 'embargo') & (db.publication_info.embargo_release_date <= today)).select()
for row in embargo_status_updates:
    row.update_record(data_rights='open', embargo_release_date=None)

'''gives colour coding to various data rights statuses, go to /views/layout.html to edit colour coding '''
def show_data_rights(data_rights,row=None):
    return SPAN(data_rights,_class=data_rights)

db.publication_info.data_rights.represent = show_data_rights

'''use the following code to reset the db, un comment and refresh, should only be commented out when not in use'''
# if db(db.publication_info.id>0).count() == 0:
#    db.publication_info.truncate()

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
                Field('taxon_id', 'reference gbif_taxon', default=None),
                Field('geo_id', type = 'string', default=None),
                Field('publication_info_id', 'reference publication_info')) #14

#db.study_meta_data.publication_info_id.requires = IS_IN_DB(db, db.publication_info.id)#, '%(title)s')

#db.study_meta_data.drop()



db.define_table('time_series_data',
                Field('sample_start_date', type = 'date', requires=IS_DATE(), comment='date of sample was set, leave blank if not applicable to the study'),
                Field('sample_start_time', type = 'time', required=False, comment='time of sample was set, leave blank if not applicable to the study'),
                Field('sample_end_date', type = 'date', requires=IS_DATE(), comment='Date of sample collection'),
                Field('sample_end_time', type = 'time', required=False, comment='time of sample collection'),
                Field('sample_value'),#type = 'integer', comment='The numerical amount or result from the sample collection'),
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
                Field('study_meta_data_id', 'reference study_meta_data'))

'''this adds the select or add widget to the'''

add_option = SelectOrAdd(form_title=T("Add a new something"),
                                              controller="vecdyn",
                                              function="add_collection_author",
                                              button_text=T("Add New"),
                                              dialog_width=600)

db.publication_info.collection_author.widget = add_option.widget
