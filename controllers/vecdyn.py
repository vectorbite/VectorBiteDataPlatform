# -*- coding: utf-8 -*-

me = auth.user_id

### The following code is for USER upload and download of data, ignore_common_filters are applied so only the users who have created a dataset can access the,

def user_collection_registration():
    form = SQLFORM(db.data_set)
    if form.process().accepted:
        session.flash = 'Thank you, your data set has been registered, now upload the data'
        redirect(URL('my_collections'))
    return locals()
#lambda row: A('Add new data set to collection',_href=URL("vecdyn", "taxon_select",vars={'id':row.id})),\


def my_collections():
    query = db.data_set.id
    data_set_id = db.data_set.id
    [setattr(f, 'readable', False)
    for f in db.data_set
        if f.name not in ('db.data_set.title,db.data_set.collection_authority')]
    #db.data_set.title.represent = lambda title,row:\
    #    A(title,_href=URL('view_my_collection',vars={'id':row.id}))
    links = [lambda row: A('Add time series data',_href=URL("data_uploader", "importer",vars={'id':row.id})),\
             lambda row: A('View time series data', _href=URL("vecdyn", "view_data_sets", vars={'data_set_id': row.id}))]
    form = SQLFORM.grid(db.data_set, ignore_common_filters=False, links = links, searchable=False, deletable=False,\
                        editable=True, details=True, create=False,csv=False, maxtextlength=40)
    if db(db.data_set.id).count() == 0:
        response.flash = 'You have not yet registered any data sets'
    else:
        response.flash = 'data sets'
    return locals()


def view_data_sets():
    data_set_id = request.get_vars.data_set_id
    query = db(db.study_data.taxon_st == None)
    #db.study_data.taxon.writable = False
    #db.study_data.taxon_st_id.writable = False
    #db.study_data.data_set_id.writable = False
    #db.study_data.location_st_id.writable = False
    [setattr(f, 'readable', False)
     for f in db.study_data
     if f.name not in ('db.study_data.title,db.study_data.taxon,'
                       'db.study_data.location_description, db.study_data.taxon_st')]
    db.study_data.data_set_id.represent = lambda title, row: \
        A(title, _href=URL('edit_data_set', vars={'id':row.id}))
    links = [lambda row: A('View sample data', _href=URL("vecdyn", "view_sample_data", vars={'id':row.id})),\
             lambda row: A('Standardise taxon',_href=URL("vecdyn", "taxon_select", vars={'id':row.id, \
                                                                                         'data_set_id':data_set_id}))]
    form = SQLFORM.grid((db.study_data.data_set_id == data_set_id) & (db.study_data.taxon_st == None), ignore_common_filters=True, links=links, maxtextlength=200, searchable=False, deletable=False, editable=True,
                            details=False, create=False,csv=False)
    if db(db.study_data.data_set_id).count() == 0:
        response.flash = 'You have not yet submitted any study data to this collection!'
    else:
        response.flash = 'This is a list of time series data linked to this data set!'
    form2 = FORM(INPUT(_type='submit',_value='Add time series data to data set',_class="btn btn-primary"))
    if form2.process().accepted:
        redirect(URL("data_uploader", "importer", vars={'id': data_set_id}))
    return locals()


def standardise_data_sets():
    data_set_id = request.get_vars.data_set_id
    #db.study_data.taxon.writable = False
    #db.study_data.taxon_st_id.writable = False
    #db.study_data.data_set_id.writable = False
    #db.study_data.location_st_id.writable = False
    if db(db.study_data.taxon_st == None):
        [setattr(f, 'readable', False)
         for f in db.study_data
         if f.name not in ('db.study_data.title,db.study_data.taxon,'
                           'db.study_data.taxon_st')]
    else:
        [setattr(f, 'readable', False)
         for f in db.study_data
         if f.name not in ('db.study_data.title,db.study_data.taxon,'
                       'db.study_data.location_description, db.study_data.taxon_st')]
    db.study_data.data_set_id.represent = lambda title, row: \
        A(title, _href=URL('edit_data_set', vars={'id':row.id}))
    links = [lambda row: A('View sample data', _href=URL("vecdyn", "view_sample_data", vars={'id':row.id})),\
             lambda row: A('Standardise taxon',_href=URL("vecdyn", "taxon_select", vars={'id':row.id, \
                                                                                         'data_set_id':data_set_id}))]
    form = SQLFORM.grid((db.study_data.data_set_id == data_set_id) & (db.study_data.taxon_st == None), ignore_common_filters=True, links=links, maxtextlength=200, searchable=False, deletable=False, editable=True,
                            details=False, create=False,csv=False)
    if db(db.study_data.data_set_id).count() == 0:
        response.flash = 'You have not yet submitted any study data to this collection!'
    else:
        response.flash = 'This is a list of time series data linked to this data set!'
    form2 = FORM(INPUT(_type='submit',_value='Add time series data to data set',_class="btn btn-primary"))
    if form2.process().accepted:
        redirect(URL("data_uploader", "importer", vars={'id': data_set_id}))
    return locals()

def taxon_select():
    data_set_id = request.get_vars.data_set_id
    study_data_id = request.get_vars.id
    response.flash = 'Now search and select the taxon used in the study, if you make a mistake hit the "Cancel" button to restart'
    [setattr(f, 'readable', False)
     for f in db.taxon
     if f.name not in ('db.taxon.tax_class,db.taxon.tax_order,'
                       'db.taxon.tax_family,db.taxon.tax_genus,'
                       'db.taxon.tax_species,db.taxon')]
    links = [lambda row: A('Select', _class="btn btn-primary", _href=URL("vecdyn", "taxon_insert", \
                                                             vars={'taxonID': row.taxonID, \
                                                                   'data_set_id': data_set_id, \
                                                                   'tax_species': row.tax_species, \
                                                                   'study_data_id': study_data_id}))]
    db.taxon.taxonID.readable = False
    grid = SQLFORM.grid(db.taxon,links=links, deletable=False, editable=False, details=False,  create=False, csv=False, maxtextlength=50)
    return locals()

def taxon_insert():
    data_set_id = request.get_vars.data_set_id
    study_data_id = request.get_vars.study_data_id
    tax_species = request.get_vars.tax_species
    taxonID = request.get_vars.taxonID
    taxon_st = tax_species
    taxon_st_id = taxonID
    row = db(db.study_data.id == study_data_id).select().first()
    row.update_record(taxon_st=taxon_st, taxon_st_id=taxonID)
    redirect(URL("vecdyn", "view_data_sets", vars={'data_set_id': data_set_id}))
    return locals()


def location_select():
    data_set_id = request.get_vars.data_set_id
    db.gaul_admin_layers.ADM_CODE.readable = False
    db.gaul_admin_layers.centroid_latitude.readable = False
    db.gaul_admin_layers.centroid_longitude.readable = False
    tax_species = request.get_vars.tax_species
    taxonID = request.get_vars.taxonID
    links = [lambda row: A('Select', _class="btn btn-primary",_href=URL("vecdyn", "submit_study_data",
                                                                         vars={'ADM_CODE': row.ADM_CODE, \
                                                                               'taxonID': taxonID, \
                                                                               'tax_species': tax_species, \
                                                                               'data_set_id': data_set_id}))]
    db.study_data.data_set_id.default = request.get_vars.data_set_id
    response.flash = 'Now select a geographical location which best describes the study location'
    grid = SQLFORM.grid(db.gaul_admin_layers, orderby=db.gaul_admin_layers.ADM0_NAME|db.gaul_admin_layers.ADM1_NAME|db.gaul_admin_layers.ADM2_NAME, links=links, deletable=False, editable=False, details=False, create=False, csv=False)
    return locals()

def submit_study_data():
    response.flash = 'Now enter the study metadata'
    db.study_data.location_ID.default = request.get_vars.ADM_CODE
    db.study_data.taxon.default = request.get_vars.tax_species
    db.study_data.taxon_id.default = request.get_vars.taxonID
    db.study_data.data_set_id.default = request.get_vars.data_set_id
    db.study_data.taxon.readable = False
    db.study_data.taxon.writable = False
    db.study_data.taxon_id.readable = False
    db.study_data.taxon_id.writable = False
    db.study_data.data_set_id.readable = False
    db.study_data.data_set_id.writable = False
    db.study_data.location_ID.writable = False
    db.study_data.location_ID.readable = False
    form = SQLFORM(db.study_data)
    if form.process().accepted:
        session.flash = 'Thank you, now submit your sample-data. If you want to submit this later click on the end button'
        session.id = form.vars.id
        redirect(URL('upload_sample_data',vars={'id':session.id}))
    return locals()

def view_my_collection():
    reg_id = request.get_vars.id
    reg = db.data_set(reg_id)
    form = SQLFORM(db.data_set,reg, readonly=True, showid=False)
    form2 = FORM(INPUT(_type='submit',_value='Please confirm these are the details you wish to edit'),_class="btn btn-primary")
    if form2.process().accepted:
        session.flash = 'Thank you, now submit your meta-data'
        redirect(URL('edit_my_collection', vars={'id':reg.id}))
    return locals()

def edit_my_collection():
    reg_id = request.get_vars.id
    form = SQLFORM(db.data_set,reg_id, showid=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submitted your changes'
        redirect(URL('my_collections'))
    return locals()

#lambda row: A('Submit Sample Data', _href=URL("vecdyn", "upload_sample_data", vars={'id':row.id}))


def upload_sample_data():
    response.flash = 'Upload sample data or click finish to upload it later'
    session.id  = request.get_vars.id
    form = FORM(INPUT(_type='file', _name='csvfile', requires=IS_UPLOAD_FILENAME(extension='csv')),
                INPUT(_type='hidden', _value='sample_data', _name='table'), INPUT(_type='submit',_value='Upload',_class="btn btn-primary"))
    if form.process().accepted:
        db[form.vars.table].import_from_csv_file(request.vars.csvfile.file)
        query = db.sample_data.study_data_id == ""
        db(query).update(study_data_id=session.id)
        session.flash = 'Data uploaded! Please confirm everything uploaded correctly and click finish to go back to main menu'
        redirect(URL("vecdyn", "view_sample_data", vars={'id':session.id}))
    return dict(form=form)


def view_sample_data():
    study_data_id = request.get_vars.id
    db.sample_data.id.readable = False
    db.sample_data.study_data_id.readable = False
    form = SQLFORM.grid(db.sample_data.study_data_id  == study_data_id, selectable = lambda ids:del_emp(ids), paginate=1000, searchable=False, deletable=False, editable=True, details=False, create=False,csv=False)
    #form.element(_type='submit')['_value'] = T("Delete")
    if form.elements('th'):
        form.elements('th')[0].append(SPAN('Select all', BR(), INPUT(_type='checkbox',
                                                              _onclick="jQuery('input:checkbox').not(this).prop('checked', this.checked);"
                                                              )))
    if db(db.sample_data.id).count() == 0:
        session.flash = 'You have not yet registered any sample data to this dataset'
    else:
        session.flash = 'Sample data'
    form2 = FORM(INPUT(_type='submit',_value='Add sample data',_class="btn btn-primary"))
    if form2.process().accepted:
        session.id = study_data_id
        redirect(URL('upload_sample_data', vars={'id': session.id}))
    o = form.element(_type='submit', _value='%s' % T('Submit'))
    if not form.create_form and not form.update_form and not form.view_form:
        if o is not None:
            o['_value'] = T("Delete selected")
    return locals()


def del_emp(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.sample_data.id == row).delete()
		pass
	pass
	return


####The next set of functions is for managers, the difference is here is that managers can access all datasets, common filters are switched to false,
@auth.requires_membership('VectorbiteAdmin')
def manage_collections():
    query = db.data_set.id
    [setattr(f, 'readable', False)
    for f in db.data_set
        if f.name not in ('db.data_set.title,db.data_set.collection_auth,'
                          'db.data_set.pub_date,db.data_set.is_public')]
    #db.data_set.title.represent = lambda title,row:\
    #    A(title,_href=URL('view_my_collection',vars={'id':row.id}))
    links = [lambda row: A('Add new data set to Collection',_href=URL("vecdyn", "taxon_select",vars={'id':row.id})),\
              lambda row: A('View Associated Datasets',_href=URL("vecdyn", "view_data_sets",vars={'id':row.id}))]
    form = SQLFORM.grid(db.data_set, ignore_common_filters=True, links = links, searchable=False, deletable=False,\
                        editable=True, details=False, create=False,csv=False)
    if db(db.data_set.id).count() == 0:
        response.flash = 'You have not yet registered any data collection information'
    else:
        response.flash = 'data collections'
    return locals()

