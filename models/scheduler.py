from gluon.scheduler import Scheduler
# import vtfuncs
import csv
import logging
import codecs

logger = logging.getLogger("web2py.app.vbdp")


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
                # 'dict(zip' creates a dictionary from three lists i.e. field names and one data row from the csv
                study = dict(zip(('taxon', 'location_description', 'study_collection_area', 'geo_datum',
                                  'gps_obfuscation_info', 'species_id_method', 'study_design', 'sampling_strategy',
                                  'sampling_method', 'sampling_protocol', 'measurement_unit', 'value_transform'),
                                 row[:13]))
                study.update({'publication_info_id': publication_info_id})
                # Check for a match in the db against the 'study' dict
                # we also need to append the publication id to this so that we do not get confused with data sets from other years
                # https://thispointer.com/python-how-to-add-append-key-value-pairs-in-dictionary-using-dict-update/
                record_2 = db.study_meta_data(**study)
                study_meta_data_id = record_2.id if record_2 else db.study_meta_data.insert(**study)

                samples = dict(zip(('sample_start_date', 'sample_start_time',
                                    'sample_end_date', 'sample_end_time', 'sample_value', 'sample_sex',
                                    'sample_stage', 'sample_location', 'sample_collection_area', 'sample_lat_dd',
                                    'sample_long_dd', 'sample_environment', 'additional_location_info',
                                    'additional_sample_info', 'sample_name'), row[13:27]))

                pub_meta_ids = {'study_meta_data_id': study_meta_data_id, 'publication_info_id': publication_info_id}

                samples.update(pub_meta_ids)

                record_3 = db.time_series_data(**samples)

                time_series_data_id = record_3.id if record_3 else db.time_series_data.insert(**samples)
            dataset.update_record(status='complete')
            db.commit()
            # add a send mailto here
        except:
            db.rollback()
            dataset.update_record(status='failed')
            db.commit()
        finally:
            csvfile.close()


def vecdyn_bulk_importer():
    # reverse select by date to be set to select by oldest
    dataset = db(db.data_set_bulk_upload.status == 'pending').select(
        orderby=db.data_set_bulk_upload.submit_datetime).first()
    if dataset != None:
        try:
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
                study.update({'publication_info_id': publication_info_id})
                # Check for a match in the db against the 'study' dict
                # we also need to append the publication id to this so that we do not get confused with data sets from other years
                # https://thispointer.com/python-how-to-add-append-key-value-pairs-in-dictionary-using-dict-update/
                record_2 = db.study_meta_data(**study)
                study_meta_data_id = record_2.id if record_2 else db.study_meta_data.insert(**study)

                samples = dict(zip(('sample_start_date', 'sample_start_time',
                                    'sample_end_date', 'sample_end_time', 'sample_value', 'sample_sex',
                                    'sample_stage', 'sample_location', 'sample_collection_area', 'sample_lat_dd',
                                    'sample_long_dd', 'sample_environment', 'additional_location_info',
                                    'additional_sample_info', 'sample_name'), row[24:39]))

                pub_meta_ids = {'study_meta_data_id': study_meta_data_id, 'publication_info_id': publication_info_id}

                samples.update(pub_meta_ids)

                #record_3 = db.time_series_data(**samples)

                #time_series_data_id = record_3.id if record_3 else

                db.time_series_data.insert(**samples)

            dataset.update_record(status='complete')
            db.commit()
            # add a send mailto here
        except:
            db.rollback()
            dataset.update_record(status='failed')
            db.commit()
        finally:
            csvfile.close()



def vecdyn_taxon_standardiser():
    tax_un_stan = db(db.study_meta_data.taxon_id == None).select(db.study_meta_data.taxon_id)
    if tax_un_stan != None:
        tax_match = db(
            (db.study_meta_data.taxon_id == None) & (db.study_meta_data.taxon == db.gbif_taxon.canonical_name)). \
            select(db.study_meta_data.id, db.gbif_taxon.taxon_id, db.gbif_taxon.canonical_name,
                   db.gbif_taxon.genus_or_above,
                   db.gbif_taxon.taxonomic_rank, limitby=(0, 200))
        for row in tax_match:
            id = row.study_meta_data.id
            taxon_id = row.gbif_taxon.taxon_id
            canonical_name = row.gbif_taxon.canonical_name
            genus_or_above = row.gbif_taxon.genus_or_above
            taxonomic_rank = row.gbif_taxon.taxonomic_rank
            db(db.study_meta_data.id == id).update(taxon_id=taxon_id, canonical_name=canonical_name,
                                                   genus_or_above=genus_or_above, taxonomic_rank=taxonomic_rank)

        db.commit()
    else:
        pass


scheduler = Scheduler(db,
                      tasks=dict(vecdyn_importer=vecdyn_importer,
                                 vecdyn_bulk_importer=vecdyn_bulk_importer,
                                 vecdyn_taxon_standardiser=vecdyn_taxon_standardiser
                                 )
                      )


def vt_eod(oneoff=False):
    import datetime

    # logger = logging.getLogger("web2py.app.vbdp")

    # Log directly to the web2py log as scheduler seems not to run in the same context as the webapp.
    import logzero
    logger = logzero.setup_logger(logfile="web2py.log",
                                  formatter=logging.Formatter(
                                      '%(asctime)s - %(levelname)-7s - %(funcName)s - %(message)s'),
                                  disableStderrLogger=True)

    # Determine next start timestamp
    nextstarttime = datetime.time(22, 0, 0, 0)
    nextstartdate = datetime.date.today() + datetime.timedelta(days=1)
    nextstart = datetime.datetime.combine(nextstartdate, nextstarttime)

    # Run uploader
    result = False
    try:
        result = vtfuncs.eod_upload_run(logger)
    except Exception:
        logger.exception("Unhandled exception in vt_eod schedule runner!")
    finally:
        # if not oneoff:
        #     # ALWAYS requeue new scheduler run!
        #     logger.info("Queueing next run for {}".format(nextstart.strftime("%d/%m/%Y %H:%M:%S")))
        #     vtscheduler.queue_task(vt_eod, start_time=nextstart, repeats=1)     # Set pvars={"oneoff":True} if oneoff
        #     db2.commit()
        return result


vtscheduler = Scheduler(db2, tasks=dict(vt_eod=vt_eod))
