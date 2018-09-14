
import csv

'''Validator, need to suss out classes and objects to build a validator, on upload data sets is validated, if any field\
fails validation then this is added to a report which informs user where failures have occured. if data has no erros then data set is saved\
for upload via a scheduler\

Look at safe tracker
'''

'''   def _validate_fields(self, fields, defattr='default'):
        response = Row()
        response.id, response.errors, new_fields = None, Row(), Row()
        for field in self:
            # we validate even if not passed in case it is required
            error = default = None
            if not field.required and not field.compute:
                default = getattr(field, defattr)
                if callable(default):
                    default = default()
            if not field.compute:
                value = fields.get(field.name, default)
                value, error = field.validate(value)
            if error:
                response.errors[field.name] = "%s" % error
            elif field.name in fields:
                # only write if the field was passed and no error
                new_fields[field.name] = value
        return response, new_fields'''


def importer():
    response.flash = 'Now upload a time series data set, make sure this is in csv format'
    data_set_id = request.get_vars.id
    #form = SQLFORM.factory(Field('csvfile','upload',uploadfield=False, requires = IS_UPLOAD_FILENAME(extension='csv')))
    form = SQLFORM(db.data_set_upload, comments = False)
    if form.validate():
        try:
            a = request.vars.csvfile.file
            readCSV = csv.reader(a, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                #dict(zip creates a dictionary from two lists i.e. from the field names and the row from the csv)
                study = dict(zip(('title', 'taxon', 'location_description', 'location_environment', 'study_lat_DD',
                'study_long_DD', 'geo_datum', \
                'spatial_accuracy', 'location_extent', 'species_id_method', 'study_design', 'sampling_strategy', 'sampling_method', \
                'sampling_protocol', 'measurement_unit', 'study_collection_area', 'value_transform'), row[:17]))
                record = db.study_data(**study) # Check for a match.
                study_data_id = record.id if record else db.study_data.insert(data_set_id=data_set_id,**study)
                samples = dict(zip(('sample_start_date','sample_start_time',\
                'sample_end_date','sample_end_time','value','sample_sex','sample_info','sample_location_info','sample_lat_DD','sample_long_DD',\
                'sample_name'), row[17:28]))
                sample_data = db.sample_data.insert(study_data_id=study_data_id,**samples)
            #redirect(URL("vecdyn", "view_data_sets", vars={'data_set_id': data_set_id}))
        except:
            response.flash = 'Errors, no data submitted. Please ensure the data set meets all the validation requirements, hit cancel to go back to data collections page'#response.flash = 'Thank you, your data has been submitted'
        else:
            session.flash = 'Thank you, your data has been submitted. Now standardise  taxonomic information'
            redirect(URL("data_uploader", "taxon_checker", vars={'data_set_id': data_set_id}))
    return dict(form=form)


#####The next controller checks to see if taxon and geographic names are already in a standardized format, if so then it will add them to the dataset standardizing it
def taxon_checker():
    data_set_id = request.get_vars.data_set_id
    rows = db(db.study_data.data_set_id == data_set_id).select()
    for row in rows:
        tax_match = db(db.taxon.tax_species == row.taxon).select()
        for match in tax_match:
            row.update_record(taxon_st=match.tax_species, taxon_st_id=match.taxonID)
    redirect(URL("vecdyn", "standardise_taxon", vars={'data_set_id': data_set_id}))
    return locals()

