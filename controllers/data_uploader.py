
import csv


def importer():
    response.flash = 'Now upload a time series data set, make sure this is in csv format'
    page = request.get_vars.page
    page = page
    publication_info_id = request.get_vars.id
    #form = SQLFORM.factory(Field('csvfile','upload',uploadfield=False, requires = IS_UPLOAD_FILENAME(extension='csv')))
    form = SQLFORM(db.data_set_upload, comments = False, fields = ['csvfile'],labels={'csvfile': 'Click to search and select a file:'})
    if form.validate():
        try:
            a = request.vars.csvfile.file
            readCSV = csv.reader(a, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                #dict(zip creates a dictionary from two lists i.e. from the field names and the row from the csv)
                study = dict(zip(('title', 'taxon', 'location_description', 'study_collection_area', 'geo_datum', \
                'species_id_method', 'study_design', 'sampling_strategy', 'sampling_method', \
                'sampling_protocol', 'measurement_unit', 'value_transform'), row[:12]))
                record = db.study_meta_data(**study)
                #####the following code checks to see if a data set has already been uploaded but under a different publication instance
                check2 = int(publication_info_id)
                check1 = record.publication_info_id if record else None
                if check1 == None:
                    pass
                elif check1 == check2:
                    pass
                else:
                    return 'It seems like this dataset has already been submitted under a different name, ' \
                           'You cannot submit the same dataset twice'
                study_meta_data_id = record.id if record else db.study_meta_data.insert(publication_info_id=publication_info_id,**study)
                samples = dict(zip(('sample_start_date','sample_start_time',
                                    'sample_end_date','sample_end_time','trap_duration','value','sample_sex',
                                    'sample_stage','sample_location','sample_collection_area','sample_lat_DD','sample_long_DD',\
                'sample_environment', 'additional_location_info', 'additional_sample_info',
                                    'sample_name'), row[12:27]))
                time_series_data = db.time_series_data.insert(study_meta_data_id=study_meta_data_id,**samples)
            #redirect(URL("vecdyn", "view_study_meta_datas", vars={'study_meta_data_id': study_meta_data_id}))
        except:
            response.flash = 'Errors, no data submitted. Please ensure the data set meets all the validation requirements, hit cancel to go back to data collections page'#response.flash = 'Thank you, your data has been submitted'
        else:
            session.flash = 'Thank you, your data has been submitted. Now standardise  taxonomic information'
            redirect(URL("data_uploader", "taxon_checker", vars={'publication_info_id': publication_info_id}))
    return dict(form=form)


#####The next controller checks to see if taxon and geographic names are already in a standardized format, if so then it will add them to the dataset standardizing it
def taxon_checker():
    publication_info_id = request.get_vars.publication_info_id
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
    for row in rows:
        tax_match = db(db.taxon.tax_species == row.taxon).select()
        for match in tax_match:
            row.update_record(taxonID=match.taxonID)
    redirect(URL("vecdyn", "standardise_taxon", vars={'publication_info_id': publication_info_id}))
    return locals()

