

import csv
def importer2():
    #form = SQLFORM.factory(Field('csvfile','upload',uploadfield=False))
    #form = SQLFORM.factory(Field('csvfile','upload',uploadfield=False))
    form = SQLFORM(db.csvfile)
    if form.process().accepted:
            a = request.vars.csv.file
            readCSV = csv.reader(a, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                person = dict(zip(('name', 'age', 'country'), row[:3]))
                record = db.person(**person) # Check for a match.
                person_id = record.id if record else db.person.insert(**person)
                thing = dict(zip(('thing_name', 'value', 'location'), row[3:6]))
                db.thing.insert(person_id=person_id, **thing)
    return dict(form=form)



def importer():
    #form = SQLFORM.factory(Field('csvfile','upload',uploadfield=False))
    form = SQLFORM.factory(Field('csvfile','upload',uploadfield=False))
    #form = SQLFORM(db.csvfile)
    if form.process().accepted:
            a = request.vars.csvfile.file
            readCSV = csv.reader(a, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                study = dict(zip(('title', 'taxon', 'location_description'), row[:3]))
                record = db.study_data(**study) # Check for a match.
                study_data_id = record.id if record else db.study_data.insert(**study)
                samples = dict(zip(('sample_start_date',\
                'sample_end_date','value'), row[3:6]))
                db.sample_data.insert(study_data_id=study_data_id, **samples)
    return dict(form=form)


'''def importer():
    #form = SQLFORM.factory(Field('csvfile','upload',uploadfield=False))
    form = SQLFORM.factory(Field('csvfile','upload',uploadfield=False))
    #form = SQLFORM(db.csvfile)
    if form.process().accepted:
            a = request.vars.csvfile.file
            readCSV = csv.reader(a, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                study = dict(zip(('title', 'taxon', 'location_description', 'location_environment', 'study_lat_DD',
                'study_long_DD', 'geo_datum', \
                'spatial_accuracy', 'location_extent', 'species_id_method', 'study_design', 'sampling_strategy', 'sampling_method', \
                'sampling_protocol', 'measurement_unit', 'study_collection_area', 'value_transform'), row[:17]))
                record = db.study_data(**study) # Check for a match.
                study_data_id = record.id if record else db.study_data.insert(**study)
                samples = dict(zip(('sample_start_date','sample_start_time',\
                'sample_end_date','sample_end_time','value,sample_sex','sample_info','sample_location_info','sample_lat_DD','sample_long_DD',\
                'sample_name'), row[17:27]))
                db.sample_data.insert(study_data_id=study_data_id, **samples)
    return dict(form=form)'''