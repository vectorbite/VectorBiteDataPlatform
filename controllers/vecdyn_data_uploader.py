
import csv

####the following function imports a vecdyn csv

@auth.requires_membership('VectorbiteAdmin')
def vecdyn_importer():
    publication_info_id = request.get_vars.publication_info_id
    response.flash = 'Now upload a time series data set, make sure this is in csv format'
    #Get the publicaton infor id from the previous page
    form = SQLFORM(db.data_set_upload, comments = False, fields = ['csvfile'],labels={'csvfile': 'Click to search and select a file:'})
    if form.validate():
        try:
            # read the upload csv
            a = request.vars.csvfile.file
            readCSV = csv.reader(a, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                # 'dict(zip' creates a dictionary from two lists i.e. field names and one data row from the csv
                study = dict(zip(('title', 'taxon', 'location_description', 'study_collection_area', 'geo_datum', \
                'gps_obfuscation_info', 'species_id_method', 'study_design', 'sampling_strategy', 'sampling_method', \
                'sampling_protocol', 'measurement_unit', 'value_transform'), row[:13]))
                ##### check for a match in the db against the 'study' dict
                record = db.study_meta_data(**study)
                ##### the following code checks to see if a data set has already been uploaded but under a different publication instance
                check2 = int(publication_info_id)
                check1 = int(record.publication_info_id) if record else None
                if (check1 == None) | (check1 == check2):
                    pass
                elif (check1 != None) & (check1 != check2):
                    return 'It seems like this dataset has already been submitted under a different name, you cannot submit the same dataset twice!'
                else:
                    pass
                ####A similar checker should also be implemented for the time series data to avoid duplicate time series entries, although this could take up a lot of memory
                study_meta_data_id = record.id if record else db.study_meta_data.insert(publication_info_id=publication_info_id,**study)
                samples = dict(zip(('sample_start_date','sample_start_time',
                                    'sample_end_date','sample_end_time','value','sample_sex',
                                    'sample_stage','sample_location','sample_collection_area','sample_lat_DD','sample_long_DD',\
                'sample_environment', 'additional_location_info', 'additional_sample_info',
                                    'sample_name'), row[13:27]))
                time_series_data = db.time_series_data.insert(study_meta_data_id=study_meta_data_id,**samples)
        except:
            response.flash = 'Errors, no data submitted. Please ensure the data set meets all the validation requirements, hit cancel to go back to data collections page'#response.flash = 'Thank you, your data has been submitted'
        else:
            session.flash = 'Thank you, your data has been submitted. Now standardise  taxonomic information'
            redirect(URL("vecdyn_data_uploader", "taxon_checker", vars={'publication_info_id': publication_info_id}))
    return dict(form=form, publication_info_id=publication_info_id)


#####The next controller checks to see if taxon  names are already in a standardized format, if so then it will add them to the dataset standardizing it

def taxon_checker():
    publication_info_id = request.get_vars.publication_info_id
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
    for row in rows:
        tax_match = db(db.taxon.tax_species == row.taxon).select()
        for match in tax_match:
            row.update_record(taxonID=match.taxonID)
    redirect(URL("vecdyn", "standardise_taxon", vars={'publication_info_id': publication_info_id}))
    return locals()

