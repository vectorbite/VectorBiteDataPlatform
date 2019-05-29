from gluon.scheduler import Scheduler
import csv



def vecdyn_importer():
    # reverse select by date to be set to select by oldest
    dataset = db(db.data_set_upload.status == 'pending').select(orderby=~db.data_set_upload.submit_datetime).first()
    if dataset != None:
        try:
            publication_info_id = dataset.publication_info_id
            filename, csvfile = db.data_set_upload.csvfile.retrieve(dataset.csvfile)
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV, None)
            # if any changes are mad to main collection template, these changes need to be reflected in the following slices
            for row in readCSV:
                # 'dict(zip' creates a dictionary from two lists i.e. field names and one data row from the csv
                # TODO delete title, skip slicing at start position 0, check for match by adding appending publication_id tp dictionary
                study = dict(zip(('title', 'taxon', 'location_description', 'study_collection_area', 'geo_datum',
                                  'gps_obfuscation_info', 'species_id_method', 'study_design', 'sampling_strategy',
                                  'sampling_method', 'sampling_protocol', 'measurement_unit', 'value_transform'),
                                 row[:13]))

                # Check for a match in the db against the 'study' dict
                record = db.study_meta_data(**study)
                study_meta_data_id = record.id if record else db.study_meta_data.insert(publication_info_id=publication_info_id,
                                                                                        **study)
                # TODO in order to avoid importing duplicate entries should also check for a match between these entries, study_meta_data_id & pub_id should be appended to samples dictionary
                samples = dict(zip(('sample_start_date', 'sample_start_time',
                                    'sample_end_date', 'sample_end_time', 'sample_value', 'sample_sex',
                                    'sample_stage', 'sample_location', 'sample_collection_area', 'sample_lat_DD',
                                    'sample_long_DD', 'sample_environment', 'additional_location_info',
                                    'additional_sample_info', 'sample_name'), row[13:27]))
                time_series_data = db.time_series_data.insert(study_meta_data_id=study_meta_data_id, publication_info_id=publication_info_id, **samples)
            rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
            for row in rows:
                tax_match = db(db.gbif_taxon.canonical_name == row.taxon).select()
                for match in tax_match:
                    row.update_record(taxon_id=match.taxon_id)
            dataset.update_record(status='complete')
            db.commit()
            # add a send mailto here
        except:
            db.rollback()
            dataset.update_record(status='failed')
            db.commit()
    else:
        pass

def vecdyn_bulk_importer():
    # reverse select by date to be set to select by oldest
    dataset = db(db.data_set_bulk_upload.status == 'pending').select(orderby=~db.data_set_bulk_upload.submit_datetime).first()
    if dataset != None:
        try:
            # When uploaded files are stored on filesystem, retrieves the original file name (filename) /
            # as seen by the user at upload time and the name of stored file (fullname, with path relative to application folder). /
            # retrieves the original file name (filename) and a file-like object ready to access uploaded file data (stream).
            # Notice that the stream returned by retrieve is a real file object in the case that uploaded files are stored on filesystem./
            # In that case remember to close the file when you have done calling stream.close().
            filename, csvfile = db.data_set_bulk_upload.csvfile.retrieve(dataset.csvfile)
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV, None)
            # if any changes are madẹ to main collection template, these changes need to be reflected in the following slices
            for row in readCSV:
                # 'dict(zip' creates a dictionary from three lists i.e. field names and one data row from the csv
                pubinfo = dict(zip(('title', 'dataset_citation', 'publication_citation',
                                  'description', 'url', 'contact_name', 'contact_affiliation',
                                  'email', 'orcid', 'dataset_license', 'project_identifier', 'publication_status'),
                                 row[:12]))

                # check to see if there is a collection author name in the db.collection_author table, if not insert it
                # if pubinfo.collection_author != None:
                #     db.collection_author.update_or_insert(name=pubinfo.collection_author)

                # Check for a match in the db against the 'pubinfo ' dict, note that this information will have a one to many relationship with metadata table
                record_1 = db.publication_info(**pubinfo)
                publication_info_id = record_1.id if record_1 else db.publication_info.insert(**pubinfo)

                # 'dict(zip' creates a dictionary from three lists i.e. field names and one data row from the csv
                study = dict(zip(('taxon', 'location_description', 'study_collection_area', 'geo_datum',
                                  'gps_obfuscation_info', 'species_id_method', 'study_design', 'sampling_strategy',
                                  'sampling_method', 'sampling_protocol', 'measurement_unit', 'value_transform'),
                                 row[12:24]))

                # Check for a match in the db against the 'study' dict
                record_2 = db.study_meta_data(**study)
                study_meta_data_id = record_2.id if record_2 else db.study_meta_data.insert(publication_info_id=publication_info_id, **study)
                samples = dict(zip(('sample_start_date', 'sample_start_time',
                                    'sample_end_date', 'sample_end_time', 'sample_value', 'sample_sex',
                                    'sample_stage', 'sample_location', 'sample_collection_area', 'sample_lat_dd',
                                    'sample_long_dd', 'sample_environment', 'additional_location_info',
                                    'additional_sample_info', 'sample_name'), row[24:40]))
                time_series_data = db.time_series_data.insert(study_meta_data_id=study_meta_data_id, publication_info_id=publication_info_id, **samples)


            rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
            for row in rows:
                tax_match = db(db.gbif_taxon.canonical_name == row.taxon).select()
                for match in tax_match:
                    row.update_record(taxon_id=match.taxon_id)
            dataset.update_record(status='complete')
            db.commit()
            #add a send mailto here
        except:
            db.rollback()
            dataset.update_record(status='failed')
            db.commit()
    else:
        pass
    return locals()

# Here is an example of safe usage of retrieve:

# from contextlib import closing
# import shutil
# row = db(db.myfile).select().first()
# (filename, stream) = db.myfile.image.retrieve(row.image)
# with closing(stream) as src, closing(open(filename, 'wb')) as dest:
#     shutil.copyfileobj(src, dest)

scheduler = Scheduler(db, tasks=dict(vecdyn_importer=vecdyn_importer, vecdyn_bulk_importer=vecdyn_bulk_importer))





