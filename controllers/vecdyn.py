# -*- coding: utf-8 -*-

me = auth.user_id

'''def index():
    if auth.user:
        redirect(URL('tasks'))
    else:
        redirect(URL('user/login'))
    return dict(message=T('Welcome!'))'''


'''def error(message="not authorized"):
    session.flash = message
    redirect(URL('tasks'))
'''

me = auth.user.id

### The following code is for USER upload and download of data, ignore_common_filters are applied so only the users who have created a dataset can access the,

def collection_registration():
    db.publication_info.data_rights.writable = False
    db.publication_info.data_rights.readable = False
    db.publication_info.embargo_release_date.writable = False
    db.publication_info.embargo_release_date.readable = False
    db.publication_info.submitted.writable = False
    db.publication_info.submitted.readable = False
    form = SQLFORM(db.publication_info)
    if form.process().accepted:
        session.flash = 'Thank you, your data set has been registered, now upload a data set'
        redirect(URL('my_collections'))
    return locals()
#lambda row: A('Add new data set to collection',_href=URL("vecdyn", "taxon_select",vars={'id':row.id})),\


def my_collections():
    query = db.publication_info.created_by==me
    [setattr(f, 'readable', False)
    for f in db.publication_info
        if f.name not in ('db.publication_info.title,db.publication_info.collection_authority, db.publication_info.data_rights')]
    #db.publication_info.data_rights.represent = lambda data_rights, row: A(data_rights, _href=URL('edit_data_rights', args=row.id))
    links = [lambda row: A('Add/upload data',_href=URL("data_uploader", "importer",vars={'id':row.id}),_class="btn btn-primary"), \
             lambda row: A('View data', _href=URL("vecdyn", "view_data", vars={'publication_info_id': row.id}),_class="btn btn-primary"),
             lambda row: A('Edit data set rights', _href=URL("vecdyn", "edit_data_rights", vars={'publication_info_id': row.id}),
                           _class="btn btn-primary"),
             lambda row: A('View/edit data publication info', _href=URL("vecdyn", "edit_collection", vars={'publication_info_id': row.id}),
                           _class="btn btn-primary")]
    form = SQLFORM.grid(db.publication_info, ignore_common_filters=False, links = links, searchable=False, deletable=False,\
                        editable=False, details=False, create=False,csv=False, maxtextlength=200,
                        fields=[
                            #db.publication_info.data_rights,
                            db.publication_info.title,
                            db.publication_info.collection_authority,
                            db.publication_info.data_rights,
                        ],
                        #buttons_placement='left',
                        #links_placement='left'
                        )
    if db(db.publication_info.id).count() == 0:
        response.flash = 'You have not yet registered any data sets'
    else:
        response.flash = 'data set registrations'
    return locals()

def edit_collection():
    db.publication_info.submitted.writable = False
    db.publication_info.submitted.readable = False
    db.publication_info.data_rights.writable = False
    db.publication_info.data_rights.readable = False
    db.publication_info.embargo_release_date.writable = False
    db.publication_info.embargo_release_date.readable = False
    publication_info_id = request.get_vars.publication_info_id
    form = SQLFORM(db.publication_info,publication_info_id, showid=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submitted your changes'
        redirect(URL('my_collections'))
    return locals()




def edit_data_rights():
    #db.data_rights.publication_info_id.writable = False
    #db.data_rights.publication_info_id.readable = False
    db.publication_info.title.writable = False
    db.publication_info.title.readable = False
    db.publication_info.collection_authority.writable = False
    db.publication_info.collection_authority.readable = False
    db.publication_info.DOI.writable = False
    db.publication_info.DOI.readable = False
    #db.publication_info.publication_date.writable = False
    #db.publication_info.publication_date.readable = False
    db.publication_info.description.writable = False
    db.publication_info.description.readable = False
    db.publication_info.url.writable = False
    db.publication_info.url.readable = False
    db.publication_info.contact_name.writable = False
    db.publication_info.contact_name.readable = False
    db.publication_info.contact_affiliation.writable = False
    db.publication_info.contact_affiliation.readable = False
    db.publication_info.contact_email.writable = False
    db.publication_info.contact_email.readable = False
    db.publication_info.ORCID.writable = False
    db.publication_info.ORCID.readable = False
    db.publication_info.submitted.writable = False
    db.publication_info.submitted.readable = False
    publication_info_id = request.get_vars.publication_info_id
    form = SQLFORM(db.publication_info, publication_info_id, showid=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submitted your changes'
        redirect(URL('my_collections'))
    return locals()


#lambda row: A('Submit Sample Data', _href=URL("vecdyn", "upload_time_series_data", vars={'id':row.id}))



def view_data():
    response.flash = 'Study meta-data!'
    #####user message code
    publication_info_id = request.get_vars.publication_info_id
    count = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxonID == None)).count()
    a = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.ADM_CODE == None)).select(
        groupby=db.study_meta_data.location_description)
    count2 = len(a)
    count2 = int(count2)
    count = int(count)
    message = ()
    if (count >=1) & (count2 >=1):
        message="You have %s taxonomic entries and %s geographic entries to standardise, click on the standardise button above and follow the insructions" % (count, count2)
    elif (count >=1) & (count2 <1):
        message="You have %s taxonomic entries to standardise, click on the standardise button above and follow the insructions" % count
    elif (count <1) & (count2 >=1):
        message="You have %s geographic entries to standardise" % count2
    elif (count <1) & (count2 <1):
        message = "All taxonomic and geographic data has been standardised for this data set!"
    query = db(db.study_meta_data.publication_info_id == publication_info_id).count()
    if query == 0:
            session.flash = "You have not yet submitted any study data to this collection, click on 'Add time series data to add a data set' !"
    elif (count >= 1) | (count2 >= 1):
            session.flash = 'You still need to standardise entries before they become available in data tables!'
    else:
            session.flash = 'This is a list of all the standardised  time series data linked to this data set!'
    ####code for grid
    links = [lambda row: A('View time series data',_class="btn btn-primary",_href=URL("vecdyn", "view_time_series_data", vars={'id':row.study_meta_data.id})),
                           lambda row: A('View/edit meta data',
                                         _href=URL("vecdyn", "edit_meta_data", vars={'study_meta_data_id':row.study_meta_data.id,
                                                                                     'publication_info_id':publication_info_id}),
                                         _class="btn btn-primary")]
    query = ((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.ADM_CODE == db.gaul_admin_layers.ADM_CODE) & (
                db.taxon.taxonID == db.study_meta_data.taxonID))
    form = SQLFORM.grid(query, field_id=db.study_meta_data.id,
                        fields=[db.taxon.tax_species,
                                db.gaul_admin_layers.ADM2_NAME,
                                db.gaul_admin_layers.ADM1_NAME,
                                db.gaul_admin_layers.ADM0_NAME,
                                db.study_meta_data.study_design,
                                db.study_meta_data.sampling_method,
                                db.study_meta_data.measurement_unit,
                                db.study_meta_data.value_transform],
                        headers={'taxon.tax_species': 'Taxon',
                                 'gaul_admin_layers.ADM2_NAME': 'District',
                                 'gaul_admin_layers.ADM1_NAME': 'Province',
                                 'gaul_admin_layers.ADM0_NAME': 'Country',
                                 'study_meta_data.study_design': 'Study Design',
                                 'study_meta_data.sampling_method': 'Sampling Method',
                                 'study_meta_data.measurement_unit': 'Measurement Unit',
                                 'study_meta_data.value_transform': 'Value Transformation'},
                        links=links,
                        maxtextlength=200,
                        searchable=False, deletable=False,
                        editable=False, details=False, create=False, csv=False)
    return locals()


def edit_meta_data():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    db.study_meta_data.taxonID.writable = False
    db.study_meta_data.ADM_CODE.writable = False
    db.study_meta_data.publication_info_id.writable = False
    db.study_meta_data.taxonID.readable = False
    db.study_meta_data.ADM_CODE.readable = False
    db.study_meta_data.publication_info_id.readable = False
    form = SQLFORM(db.study_meta_data,publication_info_id, showid=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submitted your changes'
        redirect(URL('view_data'))
    return locals()



##write a function if name is in db do something, if not standardise data
def standardise_taxon():
    session.flash = 'You have uploaded taxonomic data that is not recognised in our database, you need to standardise this manually. Click on the link next to each taxon name to search for equivalent taxon names.  !'
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.id
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select(orderby=db.study_meta_data.taxonID)
    count = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxonID == None)).count()
    first_row = rows.first()
    if first_row.taxonID == None:
        pass
    else:
        session.flash = 'Now standardise geo data'
        redirect(URL("vecdyn", "standardise_geo_data", vars={'publication_info_id': publication_info_id}))
    links = [lambda row: A('Standardise taxon', _href=URL("vecdyn", "taxon_select", vars={'study_meta_data_id': row.id, \
                                                                                          'taxon': row.taxon, \
                                                                                          'publication_info_id': publication_info_id}),_class="btn btn-primary")]
    [setattr(f, 'readable', False)
     for f in db.study_meta_data
     if f.name not in ('study_meta_data.taxon')]
    form = SQLFORM.grid((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxonID == None),
                        ignore_common_filters=True, links=links, maxtextlength=200, searchable=False,
                        headers={'study_meta_data.taxon': 'Original Taxon Name',
                                 'study_meta_data.taxonID': 'Replacement'},
                        deletable=False, editable=False,
                        details=False, create=False, csv=False
                        )
    return locals()

def taxon_select():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    taxon = request.get_vars.taxon
    response.flash = 'Now search and select the taxon used in the study, if you make a mistake hit the "Cancel" button to restart'
    [setattr(f, 'readable', False)
     for f in db.taxon
     if f.name not in ('db.taxon.tax_class,db.taxon.tax_order,'
                       'db.taxon.tax_family,db.taxon.tax_genus,'
                       'db.taxon.tax_species,db.taxon')]
    links = [lambda row: A('Select',_class="btn btn-primary", _href=URL("vecdyn", "taxon_confirm", \
                                                             vars={'taxonID': row.taxonID, \
                                                                   'publication_info_id': publication_info_id, \
                                                                   'taxon': taxon, \
                                                                   'tax_species': row.tax_species, \
                                                                   'study_meta_data_id': study_meta_data_id}))]
    db.taxon.taxonID.readable = False
    grid = SQLFORM.grid(db.taxon,links=links, deletable=False, editable=False, details=False,  create=False, csv=False, maxtextlength=50)
    search_input = grid.element('#w2p_keywords')
    if search_input:
        search_input['_value'] = taxon
    #grid.search.default = request.get_vars.get_vars.taxon
    return locals()

def taxon_confirm():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    tax_species = request.get_vars.tax_species
    taxon = request.get_vars.taxon
    taxonID = request.get_vars.taxonID
    form = FORM(INPUT(_type='submit', _value='Confirm', _class="btn btn-primary"))
    if form.process().accepted:
        redirect(URL("vecdyn", "taxon_insert", vars={'publication_info_id': publication_info_id,
                                                     'study_meta_data_id': study_meta_data_id,
                                                     'tax_species': tax_species,
                                                     'taxonID': taxonID,
                                                     'taxon': taxon,
                                                     'publication_info_id': publication_info_id}))
    return locals()

## Searches through all the entries for a taxon  and adds the tax standardized taxon name to each row
def taxon_insert():
    taxon = request.get_vars.taxon
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    tax_species = request.get_vars.tax_species
    taxonID = request.get_vars.taxonID
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
    for row in rows:
        if taxon == row.taxon:
            row.update_record(taxonID=taxonID)
        else: continue
    redirect(URL("vecdyn", "standardise_taxon", vars={'publication_info_id': publication_info_id}))
    return locals()




def standardise_geo_data():
    session.flash = 'Please standardise geo data. Click on the link next to each geo description name to search for equivalent geo names!'
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.id
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select(orderby=db.study_meta_data.ADM_CODE)
    a = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.ADM_CODE == None)).select(groupby=db.study_meta_data.location_description)
    count = len(a)
    first_row = rows.first()
    if first_row.ADM_CODE == None:
        pass
    else:
        session.flash = 'All data attached to this data set has been standardised standardise'
        redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    links = [lambda row: A('Standardise geo information',_class="btn btn-primary",_href=URL("vecdyn", "location_select", vars={'study_meta_data_id': row.id, \
                                                                                                       'location_description': row.location_description,
                                                                                                            'publication_info_id': publication_info_id}))]
    [setattr(f, 'readable', False)
    for f in db.study_meta_data
    if f.name not in ('db.study_meta_data.location_description')]
    form = SQLFORM.grid((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.ADM_CODE == None),
                        groupby=db.study_meta_data.location_description,
                        ignore_common_filters=True, links=links, maxtextlength=200, searchable=False,
                        deletable=False, editable=False,
                        details=False, create=False, csv=False)
    return locals()

def location_select():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    location_description = request.get_vars.location_description
    db.gaul_admin_layers.ADM_CODE.readable = False
    db.gaul_admin_layers.centroid_latitude.readable = False
    db.gaul_admin_layers.centroid_longitude.readable = False
    links = [lambda row: A('Select', _class="btn btn-primary",_href=URL("vecdyn", "geo_confirm",
                                                                         vars={'ADM_CODE': row.ADM_CODE, \
                                                                               'study_meta_data_id': study_meta_data_id, \
                                                                               'ADM0_NAME': row.ADM0_NAME, \
                                                                               'ADM1_NAME': row.ADM1_NAME, \
                                                                               'ADM2_NAME': row.ADM2_NAME, \
                                                                               'location_description': location_description, \
                                                                               'publication_info_id': publication_info_id}))]
    response.flash = 'Now select a geographical location which best describes the study location'
    grid = SQLFORM.grid(db.gaul_admin_layers, orderby=db.gaul_admin_layers.ADM0_NAME|db.gaul_admin_layers.ADM1_NAME|db.gaul_admin_layers.ADM2_NAME, links=links, deletable=False, editable=False, details=False, create=False, csv=False)
    search_input = grid.element('#w2p_keywords')
    if search_input:
        search_input['_value'] = location_description
    return locals()


def geo_confirm():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    ADM_CODE = request.get_vars.ADM_CODE
    ADM0_NAME = request.get_vars.ADM0_NAME
    ADM1_NAME = request.get_vars.ADM1_NAME
    ADM2_NAME = request.get_vars.ADM2_NAME
    location_description = request.get_vars.location_description
    form = FORM(INPUT(_type='submit', _value='Confirm', _class="btn btn-primary"))
    if form.process().accepted:
        redirect(URL("vecdyn", "geo_st_insert",
                     vars={'ADM_CODE': ADM_CODE, \
                           'study_meta_data_id': study_meta_data_id, \
                           'location_description': location_description, \
                           'publication_info_id': publication_info_id}))
    return locals()



def geo_st_insert():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    ADM_CODE = request.get_vars.ADM_CODE
    location_description = request.get_vars.location_description
    ADM_CODE = ADM_CODE
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
    for row in rows:
        if location_description == row.location_description:
            row.update_record(ADM_CODE=ADM_CODE)
        #else:
        #    continue
    redirect(URL("vecdyn", "standardise_geo_data", vars={'publication_info_id': publication_info_id}))
    return locals()


def upload_time_series_data():
    response.flash = 'Upload sample data or click finish to upload it later'
    session.id  = request.get_vars.id
    form = FORM(INPUT(_type='file', _name='csvfile', requires=IS_UPLOAD_FILENAME(extension='csv')),
                INPUT(_type='hidden', _value='time_series_data', _name='table'), INPUT(_type='submit',_value='Upload',_class="btn btn-primary"))
    if form.process().accepted:
        db[form.vars.table].import_from_csv_file(request.vars.csvfile.file)
        query = db.time_series_data.study_meta_data_id == ""
        db(query).update(study_meta_data_id=session.id)
        session.flash = 'Data uploaded! Please confirm everything uploaded correctly and click finish to go back to main menu'
        redirect(URL("vecdyn", "view_time_series_data", vars={'id':session.id}))
    return dict(form=form)


def view_time_series_data():
    study_meta_data_id = request.get_vars.id
    db.time_series_data.id.readable = False
    db.time_series_data.study_meta_data_id.readable = False
    form = SQLFORM.grid(db.time_series_data.study_meta_data_id  == study_meta_data_id, selectable = lambda ids:del_emp(ids), paginate=1000, searchable=False, deletable=False, editable=True, details=False, create=False,csv=False)
    #form.element(_type='submit')['_value'] = T("Delete")
    if form.elements('th'):
        form.elements('th')[0].append(SPAN('Select all', BR(), INPUT(_type='checkbox',
                                                              _onclick="jQuery('input:checkbox').not(this).prop('checked', this.checked);"
                                                              )))
    if db(db.time_series_data.id).count() == 0:
        session.flash = 'You have not yet registered any sample data to this dataset'
    else:
        session.flash = 'Sample data'
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
			db(db.time_series_data.id == row).delete()
		pass
	pass
	return


####The next set of functions is for managers, the difference is here is that managers can access all datasets, common filters are switched to false,
@auth.requires_membership('VectorbiteAdmin')
def manage_collections():
    query = db.publication_info.id
    [setattr(f, 'readable', False)
    for f in db.publication_info
        if f.name not in ('db.publication_info.title, db.publication_info.collection_auth,'
                          'db.publication_info.pub_date, db.publication_info.is_public')]
    #db.publication_info.title.represent = lambda title,row:\
    #    A(title,_href=URL('view_my_collection',vars={'id':row.id}))
    links = [lambda row: A('Add new data set to Collection',_href=URL("vecdyn", "taxon_select",vars={'id':row.id})),\
              lambda row: A('View Associated Datasets',_href=URL("vecdyn", "view_publication_infos",vars={'id':row.id}))]
    form = SQLFORM.grid(db.publication_info, ignore_common_filters=True, links = links, searchable=False, deletable=False,\
                        editable=True, details=False, create=False,csv=False)
    if db(db.publication_info.id).count() == 0:
        response.flash = 'You have not yet registered any data collection information'
    else:
        response.flash = 'data collections'
    return locals()

