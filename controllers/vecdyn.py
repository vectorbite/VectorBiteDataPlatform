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

@auth.requires_membership('VectorbiteAdmin')
def dataset_registration():
    task_id = request.get_vars.task_id
    if task_id != None:
        myrecord = db(db.task.id == task_id).select().first()
        db.publication_info.title.default = myrecord.title
        collection_author = myrecord.collection_author
        collection_author = db(db.collection_author.name == collection_author).select().first()
        db.publication_info.collection_author.default = collection_author.id
        db.publication_info.dataset_doi.default = myrecord.digital_object_identifier #need to correct this, dataset doi missing
        db.publication_info.publication_doi.default = myrecord.publication_doi
        db.publication_info.url.default = myrecord.url
        db.publication_info.contact_affiliation.default = myrecord.contact_affiliation
        db.publication_info.dataset_license.default = myrecord.dataset_license
        db.publication_info.description.default = myrecord.description
        db.publication_info.contact_name.default = myrecord.contact_name
        db.publication_info.email.default = myrecord.email
        db.publication_info.orcid.default = myrecord.orcid
    else:
        pass
    db.publication_info.data_rights.writable = False
    db.publication_info.data_rights.readable = False
    db.publication_info.embargo_release_date.writable = False
    db.publication_info.embargo_release_date.readable = False
    db.publication_info.submit.writable = False
    db.publication_info.submit.readable = False
    add_option = SelectOrAdd(form_title="Add new collection author",
                             controller="vecdyn",
                             function="add_collection_author",
                             button_text = "Add New")
    #assign widget to field
    db.publication_info.collection_author.widget = add_option.widget
    form = SQLFORM(db.publication_info)
    if form.process().accepted:
        session.flash = 'Thank you, your data set has been registered, now upload a data set'
        redirect(URL('dataset_registrations'))
        # you need jQuery for the widget to work; include here or just put it in your master layout.html
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.js'))
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.theme.css'))
    return locals()
#lambda row: A('Add new data set to collection',_href=URL("vecdyn", "taxon_select",vars={'id':row.id})),\

def add_collection_author():
    #this is the controller function that will appear in our dialog
    form = SQLFORM(db.collection_author)
    if form.accepts(request):
        #Successfully added new item
        #do whatever else you may want
        #Then let the user know adding via our widget worked
        response.flash = T("Added")
        target = request.args[0]
        #close the widget's dialog box
        response.js = 'jQuery( "#%s_dialog-form" ).dialog( "close" ); ' %(target)
        #update the options they can select their new category in the main form
        response.js += """jQuery("#%s").append("<option value='%s'>%s</option>");""" \
                % (target, form.vars.id, form.vars.name)
        #and select the one they just added
        response.js += """jQuery("#%s").val("%s");""" % (target, form.vars.id)
        #finally, return a blank form incase for some reason they wanted to add another option
        return form
    elif form.errors:
        # silly user, just send back the form and it'll still be in our dialog box complete with error messages
        return form
    else:
        #hasn't been submitted yet, just give them the fresh blank form
        return form


@auth.requires_membership('VectorbiteAdmin')
def dataset_registrations():
    #query = db.publication_info.created_by==me
    [setattr(f, 'readable', False)
    for f in db.publication_info
        if f.name not in ('db.publication_info.data_rights, db.publication_info.dataset_doi, db.publication_info.title,db.publication_info.collection_author, db.publication_info.submit, db.publication_info.created_by')]
    #db.publication_info.data_rights.represent = lambda data_rights, row: A(data_rights, _href=URL('edit_data_rights', args=row.id))
    links = [lambda row: A('Enter Dataset Control Panel', _href=URL("vecdyn", "view_data", vars={'publication_info_id': row.id}),_class="btn btn-primary")]
    form = SQLFORM.grid(db.publication_info, links = links, searchable=False, deletable=lambda row: (row.created_by==me),\
                        editable=False, details=False, create=False,csv=False, maxtextlength=200,
                        fields=[
                            db.publication_info.title,
                            db.publication_info.collection_author,
                            db.publication_info.dataset_doi,
                            db.publication_info.data_rights,
                            db.publication_info.submit,
                            db.publication_info.created_by],
                        #buttons_placement='left',
                        #links_placement='left'
                        )
    if db(db.publication_info.id).count() == 0:
        response.flash = 'You have not yet registered any data sets'
    else:
        response.flash = 'data set registrations'
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def edit_dataset_general_info():
    db.publication_info.submit.writable = False
    db.publication_info.submit.readable = False
    db.publication_info.data_rights.writable = False
    db.publication_info.data_rights.readable = False
    db.publication_info.embargo_release_date.writable = False
    db.publication_info.embargo_release_date.readable = False
    publication_info_id = request.get_vars.publication_info_id
    add_option = SelectOrAdd(form_title="Add new collection author",
                             controller="vecdyn",
                             function="add_collection_author",
                             button_text="Add New")
    # assign widget to field
    db.publication_info.collection_author.widget = add_option.widget
    # you need jQuery for the widget to work; include here or just put it in your master layout.html
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.js'))
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.theme.css'))
    form = SQLFORM(db.publication_info,publication_info_id, showid=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submit your changes'
        redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    return locals()



@auth.requires_membership('VectorbiteAdmin')
def edit_data_rights():
    publication_info_id = request.get_vars.publication_info_id
    #db.data_rights.publication_info_id.writable = False
    #db.data_rights.publication_info_id.readable = False
    db.publication_info.title.writable = False
    db.publication_info.title.readable = False
    db.publication_info.collection_author.writable = False
    db.publication_info.collection_author.readable = False
    db.publication_info.dataset_doi.writable = False
    db.publication_info.dataset_doi.readable = False
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
    db.publication_info.email.writable = False
    db.publication_info.email.readable = False
    db.publication_info.orcid.writable = False
    db.publication_info.orcid.readable = False
    db.publication_info.data_set_type.writable = False
    db.publication_info.data_set_type.readable = False
    db.publication_info.publication_doi.writable = False
    db.publication_info.publication_doi.readable = False
    form = SQLFORM(db.publication_info, publication_info_id, showid=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submitted your changes'
        redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    return locals()


#lambda row: A('Submit Sample Data', _href=URL("vecdyn", "upload_time_series_data", vars={'id':row.id}))


@auth.requires_membership('VectorbiteAdmin')
def view_data():
    #####query for publication info pages, found at the top of the view data pages
    publication_info_id = request.get_vars.publication_info_id
    publication_info_query = db(db.publication_info.id == publication_info_id).select()
    ###checks to see if there are understadnardised data sets in the data collection
    ds_check = db(db.study_meta_data.publication_info_id == publication_info_id).select(groupby=db.study_meta_data.publication_info_id)
    ds_count = len(ds_check)
    ds_count = int(ds_count)
    ###following queries count to see how many unstandardiesed data sets are in the collection, supplies user with a message
    b = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxonID == None)).select(
        groupby=db.study_meta_data.taxon)
    count = len(b)
    count = int(count)
    a = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.ADM_CODE == None)).select(
        groupby=db.study_meta_data.location_description)
    count2 = len(a)
    count2 = int(count2)
    message = ()
    if ds_count < 1:
        message="You have not uploaded any data yet"
    elif (count >=1) & (count2 >=1):
        message="You have %s taxonomic entries and %s geographic entries to standardise, click on the standardise button above and follow the insructions" % (count, count2)
    elif (count >=1) & (count2 <1):
        message="You have %s taxonomic entries to standardise, click on the standardise button above and follow the insructions" % count
    elif (count <1) & (count2 >=1):
        message="You have %s geographic entries to standardise" % count2
    elif (count <1) & (count2 <1):
        message = "All taxonomic and geographic data has been standardised for this data set!"
    query = db(db.study_meta_data.publication_info_id == publication_info_id).count()
    if query == 0:
            response.flash = "You have not yet submitted any data yet, click on 'Add time series data to add a data set' !"
    elif (count >= 1) | (count2 >= 1):
            response.flash = 'You still need to standardise entries before they will become available in this page, once data is visible in this page it is ready to submit!'
    else:
            response.flash = 'This is a list of all the standardised  time series data linked to this data set!'
    ####code for grid
    ####row.id isnt working in this function since we are joining multiple tables, instead we need to specify the row.study_meta_data.id for the links in the table
    links = [lambda row: A('View/edit meta entry',_href=URL("vecdyn", "edit_meta_data", vars={'study_meta_data_id':row.study_meta_data.id,
                                                                                     'publication_info_id':publication_info_id}),_class="btn btn-primary"),
             lambda row: A('View time series data entries',_class="btn btn-primary",_href=URL("vecdyn", "view_time_series_data",vars={'study_meta_data_id':row.study_meta_data.id, 'publication_info_id':publication_info_id})),
                           ]
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


@auth.requires_membership('VectorbiteAdmin')
def view_unstandardised_data():
        #####user message code
        publication_info_id = request.get_vars.publication_info_id
        #####query for publication info pages, found at the top of the view data pages
        publication_info_id = request.get_vars.publication_info_id
        publication_info_query = db(db.publication_info.id == publication_info_id).select()
        ###checks to see if there are understadnardised data sets in the data collection
        ds_check = db(db.study_meta_data.publication_info_id == publication_info_id).select(
            groupby=db.study_meta_data.publication_info_id)
        ds_count = len(ds_check)
        ds_count = int(ds_count)
        ###following queries count to see how many unstandardiesed data sets are in the collection, supplies user with a message
        b = db((db.study_meta_data.publication_info_id == publication_info_id) & (
                    db.study_meta_data.taxonID == None)).select(
            groupby=db.study_meta_data.taxon)
        count = len(b)
        count = int(count)
        a = db((db.study_meta_data.publication_info_id == publication_info_id) & (
                    db.study_meta_data.ADM_CODE == None)).select(
            groupby=db.study_meta_data.location_description)
        count2 = len(a)
        count2 = int(count2)
        message = ()
        if ds_count < 1:
            message = "You have not uploaded any data yet"
        elif (count >= 1) & (count2 >= 1):
            message = "You have %s taxonomic entries and %s geographic entries to standardise, click on the standardise button above and follow the insructions" % (
            count, count2)
        elif (count >= 1) & (count2 < 1):
            message = "You have %s taxonomic entries to standardise, click on the standardise button above and follow the insructions" % count
        elif (count < 1) & (count2 >= 1):
            message = "You have %s geographic entries to standardise" % count2
        elif (count < 1) & (count2 < 1):
            message = "All taxonomic and geographic data has been standardised for this data set!"
        query = db(db.study_meta_data.publication_info_id == publication_info_id).count()
        if query == 0:
            response.flash = "You have not yet submitted any data yet, click on 'Add time series data to add a data set' !"
        elif (count >= 1) | (count2 >= 1):
            response.flash = 'You still need to standardise entries!'
        else:
            response.flash = 'This is a list of all the standardised  time series data linked to this data set!'
        links = [lambda row: A('View/edit meta data entry',
                               _href=URL("vecdyn", "edit_meta_data", vars={'study_meta_data_id': row.id,
                                                                           'publication_info_id': publication_info_id}),
                               _class="btn btn-primary"),
                 lambda row: A('View time series data entries', _class="btn btn-primary",
                               _href=URL("vecdyn", "view_time_series_data",
                                         vars={'study_meta_data_id': row.id,
                                               'publication_info_id': publication_info_id})),
                 ]
        query = ((db.study_meta_data.taxonID==None) | (db.study_meta_data.ADM_CODE==None) & (db.study_meta_data.publication_info_id == publication_info_id))
        form = SQLFORM.grid(query, field_id=db.study_meta_data.id,
                            fields=[db.study_meta_data.taxon,
                                    db.study_meta_data.taxonID,
                                    db.study_meta_data.location_description,
                                    db.study_meta_data.ADM_CODE],
                            headers={'study_meta_data.taxon': 'Original Taxon',
                                     'study_meta_data.taxonID': 'Replacement Taxon Name',
                                     'study_meta_data.location_description': 'Original Location Description',
                                     'study_meta_data.ADM_CODE': 'Replacement Location'},
                            maxtextlength=200,links=links,
                            searchable=False, deletable=False,
                            editable=False, details=False, create=False, csv=False)
        return locals()



@auth.requires_membership('VectorbiteAdmin')
def edit_meta_data():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    meta_edit = "yes"
    rows = db((db.study_meta_data.id == study_meta_data_id) & (db.study_meta_data.taxonID == db.taxon.taxonID)
              & (db.study_meta_data.ADM_CODE == db.gaul_admin_layers.ADM_CODE)).select()
    response.flash = 'Edit meta-data entry!'
    db.study_meta_data.title.writable = False
    db.study_meta_data.title.readable = False
    db.study_meta_data.taxon.writable = False
    db.study_meta_data.taxon.readable = False
    #db.study_meta_data.location_description.writable = False
    db.study_meta_data.taxonID.writable = False
    db.study_meta_data.ADM_CODE.writable = False
    db.study_meta_data.publication_info_id.writable = False
    db.study_meta_data.taxonID.readable = False
    db.study_meta_data.ADM_CODE.readable = False
    db.study_meta_data.publication_info_id.readable = False
    form = SQLFORM(db.study_meta_data,study_meta_data_id, showid=False, comments=False
                   )
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submit your changes'
        redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    return locals()



##write a function if name is in db do something, if not standardise data
@auth.requires_membership('VectorbiteAdmin')
def standardise_taxon():
    response.flash = 'You have uploaded taxonomic data that is not recognised in our database, you need to standardise this manually. Click on the link next to each taxon name to search for equivalent taxon names.  !'
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.id
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select(orderby=db.study_meta_data.taxonID)
    a = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxonID == None)).select(
        groupby=db.study_meta_data.taxon)
    count = len(a)
    taxon_entries = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.ADM_CODE == None)).select(
        groupby=db.study_meta_data.location_description)
    taxon_entries_count = len(taxon_entries)
    taxon_entries_count = int(taxon_entries_count)
    first_row = rows.first()
    if first_row.taxonID == None:
        pass
    else:
        response.flash = 'Now standardise geo data'
        redirect(URL("vecdyn", "standardise_geo_data", vars={'publication_info_id': publication_info_id}))
    links = [lambda row: A('Standardise taxon', _href=URL("vecdyn", "taxon_select", vars={'study_meta_data_id': row.id, \
                                                                                          'taxon': row.taxon, \
                                                                                          'publication_info_id': publication_info_id}),_class="btn btn-primary")]
    [setattr(f, 'readable', False)
     for f in db.study_meta_data
     if f.name not in ('study_meta_data.taxon')]
    form = SQLFORM.grid((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxonID == None),
                        groupby=db.study_meta_data.taxon,
                        links=links, maxtextlength=200, searchable=False,
                        headers={'study_meta_data.taxon': 'Original Taxon Name',
                                 'study_meta_data.taxonID': 'Replacement'},
                        deletable=False, editable=False,
                        details=False, create=False, csv=False
                        )
    return locals()

@auth.requires_membership('VectorbiteAdmin')
def taxon_select():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    taxon = request.get_vars.taxon
    meta_edit = request.get_vars.meta_edit
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
                                                                   'meta_edit': meta_edit, \
                                                                   'tax_species': row.tax_species, \
                                                                   'study_meta_data_id': study_meta_data_id}))]
    db.taxon.taxonID.readable = False
    grid = SQLFORM.grid(db.taxon,links=links, deletable=False, editable=False, details=False,  create=False, csv=False, maxtextlength=50)
    search_input = grid.element('#w2p_keywords')
    if search_input:
        search_input['_value'] = taxon
    #grid.search.default = request.get_vars.get_vars.taxon
    return locals()

@auth.requires_membership('VectorbiteAdmin')
def taxon_confirm():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    tax_species = request.get_vars.tax_species
    taxon = request.get_vars.taxon
    taxonID = request.get_vars.taxonID
    meta_edit = request.get_vars.meta_edit
    form = FORM(INPUT(_type='submit', _value='Confirm', _class="btn btn-primary"))
    if form.process().accepted:
            redirect(URL("vecdyn", "taxon_insert", vars={'publication_info_id': publication_info_id,
                                                         'study_meta_data_id': study_meta_data_id,
                                                         'tax_species': tax_species,
                                                         'taxonID': taxonID,
                                                         'taxon': taxon,
                                                         'meta_edit': meta_edit, \
                                                         'publication_info_id': publication_info_id}))


    return locals()

@auth.requires_membership('VectorbiteAdmin')
## Searches through all the entries for a taxon  and adds the tax standardized taxon name to each row
def taxon_insert():
    taxon = request.get_vars.taxon
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    tax_species = request.get_vars.tax_species
    taxonID = request.get_vars.taxonID
    meta_edit = request.get_vars.meta_edit
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
    for row in rows:
        if taxon == row.taxon:
            row.update_record(taxonID=taxonID)
        else: continue
    if meta_edit == 'yes':
        session.flash = 'Success!'
        redirect(URL("vecdyn", "edit_meta_data", vars={'publication_info_id': publication_info_id,
                                                       'study_meta_data_id': study_meta_data_id,
                                                       'publication_info_id': publication_info_id}))
    else:
        redirect(URL("vecdyn", "standardise_taxon", vars={'publication_info_id': publication_info_id}))
    return locals()

@auth.requires_membership('VectorbiteAdmin')
def standardise_geo_data():
    response.flash = 'Please standardise geo data. Click on the link next to each geo description name to search for equivalent geo names!'
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.id
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select(orderby=db.study_meta_data.ADM_CODE)
    a = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.ADM_CODE == None)).select(groupby=db.study_meta_data.location_description)
    count = len(a)
    first_row = rows.first()
    if first_row.ADM_CODE == None:
        pass
    else:
        response.flash = 'All data attached to this data set has been standardised standardise'
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


@auth.requires_membership('VectorbiteAdmin')
def location_select():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    location_description = request.get_vars.location_description
    meta_edit = request.get_vars.meta_edit
    db.gaul_admin_layers.ADM_CODE.readable = False
    db.gaul_admin_layers.centroid_latitude.readable = False
    db.gaul_admin_layers.centroid_longitude.readable = False
    links = [lambda row: A('Select', _class="btn btn-primary",_href=URL("vecdyn", "geo_confirm",
                                                                         vars={'ADM_CODE': row.ADM_CODE, \
                                                                                'meta_edit': meta_edit, \
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



@auth.requires_membership('VectorbiteAdmin')
def geo_confirm():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    meta_edit = request.get_vars.meta_edit
    ADM_CODE = request.get_vars.ADM_CODE
    ADM0_NAME = request.get_vars.ADM0_NAME
    ADM1_NAME = request.get_vars.ADM1_NAME
    ADM2_NAME = request.get_vars.ADM2_NAME
    meta_edit = request.get_vars.meta_edit
    location_description = request.get_vars.location_description
    form = FORM(INPUT(_type='submit', _value='Confirm', _class="btn btn-primary"))
    if form.process().accepted:
        redirect(URL("vecdyn", "geo_st_insert",
                     vars={'ADM_CODE': ADM_CODE, \
                           'study_meta_data_id': study_meta_data_id, \
                           'meta_edit': meta_edit, \
                           'location_description': location_description, \
                           'publication_info_id': publication_info_id}))
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def geo_st_insert():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    ADM_CODE = request.get_vars.ADM_CODE
    meta_edit = request.get_vars.meta_edit
    location_description = request.get_vars.location_description
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
    for row in rows:
        if location_description == row.location_description:
            row.update_record(ADM_CODE=ADM_CODE)
        #else:
        #    continue
    if meta_edit == 'yes':
        session.flash = 'Success!'
        redirect(URL("vecdyn", "edit_meta_data", vars={'publication_info_id': publication_info_id,
                                                       'study_meta_data_id': study_meta_data_id,
                                                       'meta_edit': meta_edit}))
    else:
        redirect(URL("vecdyn", "standardise_geo_data", vars={'publication_info_id': publication_info_id}))
        response.flash = 'Success!'
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def view_time_series_data():
    study_meta_data_id = request.get_vars.study_meta_data_id
    publication_info_id = request.get_vars.publication_info_id
    db.time_series_data.id.readable = False
    db.time_series_data.study_meta_data_id.readable = False
    links = [
        lambda row: A('Edit time series entry',_class="btn btn-primary", _href=URL("vecdyn", "edit_time_series_entry",
                                                                                    vars={'id': row.id, \
                                                                                          'study_meta_data_id': study_meta_data_id, \
                                                                                          'publication_info_id': publication_info_id}))]
    form = SQLFORM.grid(db.time_series_data.study_meta_data_id  == study_meta_data_id,links=links,selectable = lambda ids:del_emp(ids), paginate=1000, searchable=False, deletable=False, editable=False, details=False, create=False,csv=False)
    if form.elements('th'):
        form.elements('th')[0].append(SPAN('Select all', BR(), INPUT(_type='checkbox',
                                                              _onclick="jQuery('input:checkbox').not(this).prop('checked', this.checked);"
                                                              )))
    if db(db.time_series_data.id).count() == 0:
        response.flash = 'You have not added any time series data to this dataset'
    else:
        response.flash = 'Time series data'
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

@auth.requires_membership('VectorbiteAdmin')
def edit_time_series_entry():
    study_meta_data_id = request.get_vars.study_meta_data_id
    publication_info_id = request.get_vars.publication_info_id
    time_series_entry = request.get_vars.id
    db.time_series_data.study_meta_data_id.writable = False
    db.time_series_data.study_meta_data_id.readable = False
    form = SQLFORM(db.time_series_data, time_series_entry, showid=False, comments=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submit your changes'
        redirect(URL('vecdyn','view_time_series_data', vars={'study_meta_data_id': study_meta_data_id}))
    return locals()




