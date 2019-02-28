# -*- coding: utf-8 -*-

me = auth.user_id

# def index():
#     if auth.user:
#         redirect(URL('tasks'))
#     else:
#         redirect(URL('user/login'))
#     return dict(message=T('Welcome!'))


# def error(message="not authorized"):
#     session.flash = message
#     redirect(URL('tasks'))


# ----------------------------------------------------------------------------------------------------------------------
# The following code is for USER upload and download of data
# Ignore_common_filters are applied so only the users who have created a dataset can access them
# ----------------------------------------------------------------------------------------------------------------------


@auth.requires_membership('VectorbiteAdmin')
def dataset_registration():
    task_id = request.get_vars.task_id
    if task_id is not None:
        myrecord = db(db.task.id == task_id).select().first()
        db.publication_info.title.default = myrecord.title
        # collection_author = myrecord.collection_author
        # collection_author = db(db.collection_author.name == collection_author).select().first()
        db.publication_info.collection_author.default = myrecord.collection_author
        db.publication_info.dataset_doi.default = myrecord.digital_object_identifier    # TODO: dataset doi missing
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
    add_option = SelectOrAdd(form_title="Add new collection author",
                             controller="vecdyn",
                             function="add_collection_author",
                             button_text="Add New")
    # assign widget to field
    db.publication_info.collection_author.widget = add_option.widget
    form = SQLFORM(db.publication_info)
    if form.process().accepted:
        session.flash = 'Thank you, your data set has been registered, now upload a data set'
        redirect(URL('dataset_registrations'))
        # you need jQuery for the widget to work; include here or just put it in your master layout.html
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.js'))
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.theme.css'))
    return locals()


def add_collection_author():
    """this is the controller function that will appear in our dialog"""
    form = SQLFORM(db.collection_author)
    if form.accepts(request):
        # Successfully added new item
        # do whatever else you may want
        # Then let the user know adding via our widget worked
        response.flash = T("Added")
        target = request.args[0]
        # close the widget's dialog box
        response.js = 'jQuery( "#%s_dialog-form" ).dialog( "close" ); ' %(target)
        # update the options they can select their new category in the main form
        response.js += """jQuery("#%s").append("<option value='%s'>%s</option>");""" \
                % (target, form.vars.id, form.vars.name)
        # and select the one they just added
        response.js += """jQuery("#%s").val("%s");""" % (target, form.vars.id)
        # finally, return a blank form incase for some reason they wanted to add another option
        return form
    elif form.errors:
        # silly user, just send back the form and it'll still be in our dialog box complete with error messages
        return form
    else:
        # hasn't been submitted yet, just give them the fresh blank form
        return form


@auth.requires_membership('VectorbiteAdmin')
def dataset_registrations():
    # query = db.publication_info.created_by == me
    [setattr(f, 'readable', False)
        for f in db.publication_info
        if f.name not in ('db.publication_info.data_rights,'
                          'db.publication_info.dataset_doi,'
                          'db.publication_info.title,'
                          'db.publication_info.collection_author,'
                          'db.publication_info.created_by')]
    # db.publication_info.data_rights.represent = lambda data_rights, row: A(data_rights, _href=URL('edit_data_rights', args=row.id))
    links = [lambda row: A('Enter Dataset Control Panel', _href=URL("vecdyn", "view_data", vars={'publication_info_id': row.id}), _class="btn btn-primary")]
    form = SQLFORM.grid(db.publication_info, links=links, searchable=True, advanced_search=False, deletable=lambda row: (row.created_by == me),
                        editable=False, details=False, create=False, csv=False, maxtextlength=200,
                        fields=[
                            db.publication_info.title,
                            db.publication_info.collection_author,
                            db.publication_info.dataset_doi,
                            db.publication_info.data_rights,
                            db.publication_info.created_by],
                        # buttons_placement='left',
                        # links_placement='left'
                        )
    if db(db.publication_info.id).count() == 0:
        response.flash = 'You have not yet registered any data sets'
    else:
        response.flash = 'data set registrations'
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def edit_dataset_general_info():
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
    form = SQLFORM(db.publication_info, publication_info_id, showid=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submit your changes'
        redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def edit_data_rights():
    publication_info_id = request.get_vars.publication_info_id
    # db.data_rights.publication_info_id.writable = False
    # db.data_rights.publication_info_id.readable = False
    db.publication_info.title.writable = False
    db.publication_info.title.readable = False
    db.publication_info.collection_author.writable = False
    db.publication_info.collection_author.readable = False
    db.publication_info.dataset_doi.writable = False
    db.publication_info.dataset_doi.readable = False
    # db.publication_info.publication_date.writable = False
    # db.publication_info.publication_date.readable = False
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



@auth.requires_membership('VectorbiteAdmin')
def view_data():
    # Query for publication info pages, found at the top of the view data pages
    publication_info_id = request.get_vars.publication_info_id
    publication_info_query = db(db.publication_info.id == publication_info_id).select()

    # Following queries count to see how many unstandardised entries are in the collection, unstandardised dates are
    # recognised by the absence of either a no taxon_id (None) or no geo_id (None) supplies user with a message
    ds_check = db(db.study_meta_data.publication_info_id == publication_info_id).select(distinct=db.study_meta_data.publication_info_id)
    ds_count = len(ds_check)
    ds_count = int(ds_count)
    b = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxon_id == None)).select(
        distinct=db.study_meta_data.taxon)
    count = len(b)
    count = int(count)
    a = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.geo_id == None)).select(
        distinct=db.study_meta_data.location_description)
    count2 = len(a)
    count2 = int(count2)
    message = ()

    if ds_count < 1:
        message = "You have not uploaded any data yet"
    elif (count >= 1) & (count2 >= 1):
        message = "You have %s taxonomic entries and %s geographic entries to standardise, " \
                "click on the standardise button above and follow the insructions" % (count, count2)
    elif (count >= 1) & (count2 < 1):
        message = "You have %s taxonomic entries to standardise, " \
                "click on the standardise button above and follow the insructions" % count
    elif (count < 1) & (count2 >= 1):
        message = "You have %s geographic entries to standardise" % count2
    elif (count < 1) & (count2 < 1):
        message = "All taxonomic and geographic data has been standardised for this data set!"
    query = db(db.study_meta_data.publication_info_id == publication_info_id).count()

    if query == 0:
            response.flash = "You have not yet submitted any data yet, click on 'Add time series data to add a data set'!"
    elif (count >= 1) | (count2 >= 1):
            response.flash = 'You still need to standardise entries before they will become available in this page, ' \
                             'go the the unstandardised data page and run through the stadardisation process, ' \
                             'once data is visible in this page it is ready to submit!'
    else:
            response.flash = 'This is a list of all the standardised time series data linked to this data set!'

    # Code for grid
    # row.id isnt working in this function since we are joining multiple tables,
    # instead we need to specify the row.study_meta_data.id for the links in the table
    links = [lambda row: A('View/edit meta entry',
                           _href=URL("vecdyn", "edit_meta_data",
                                     vars={'study_meta_data_id': row.study_meta_data.id,
                                           'publication_info_id': publication_info_id}),
                           _class="btn btn-primary"),
             lambda row: A('View time series data entries',
                           _class="btn btn-primary",
                           _href=URL("vecdyn", "view_time_series_data",
                                     vars={'study_meta_data_id': row.study_meta_data.id,
                                           'publication_info_id': publication_info_id})),
             ]

    query = ((db.study_meta_data.publication_info_id == publication_info_id) &
             (db.study_meta_data.geo_id == db.gaul_admin_layers.geo_id) &
             (db.gbif_taxon.taxon_id == db.study_meta_data.taxon_id))

    form = SQLFORM.grid(query, field_id=db.study_meta_data.id,
                        fields=[db.gbif_taxon.canonical_name,
                                db.gaul_admin_layers.adm2_name,
                                db.gaul_admin_layers.adm1_name,
                                db.gaul_admin_layers.adm0_name,
                                db.study_meta_data.study_design,
                                db.study_meta_data.sampling_method,
                                db.study_meta_data.measurement_unit,
                                db.study_meta_data.value_transform],
                        headers={'gbif_taxon.canonical_name': 'Taxon',
                                 'gaul_admin_layers.adm2_name': 'Administrative Division 2',
                                 'gaul_admin_layers.adm1_name': 'Administrative Division 1',
                                 'gaul_admin_layers.adm0_name': 'Country Name',
                                 'study_meta_data.study_design': 'Study Design',
                                 'study_meta_data.sampling_method': 'Sampling Method',
                                 'study_meta_data.measurement_unit': 'Measurement Unit',
                                 'study_meta_data.value_transform': 'Value Transformation'},
                        links=links,
                        maxtextlength=200,
                        searchable=True, advanced_search=False, deletable=False,
                        editable=False, details=False, create=False, csv=False)
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def view_unstandardised_data():
        # User message code
        publication_info_id = request.get_vars.publication_info_id

        # Query for publication info pages, found at the top of the view data pages
        publication_info_id = request.get_vars.publication_info_id
        publication_info_query = db(db.publication_info.id == publication_info_id).select()

        # Checks to see if there are understadnardised data sets in the data collection
        ds_check = db(db.study_meta_data.publication_info_id == publication_info_id).select(
            distinct=db.study_meta_data.publication_info_id)
        ds_count = len(ds_check)
        ds_count = int(ds_count)

        # Following queries count to see how many unstandardiesed data sets are in the collection,
        # supplies user with a message
        b = db((db.study_meta_data.publication_info_id == publication_info_id) & (
                    db.study_meta_data.taxon_id == None)).select(
            distinct=db.study_meta_data.taxon)
        count = len(b)
        count = int(count)
        a = db((db.study_meta_data.publication_info_id == publication_info_id) & (
                    db.study_meta_data.geo_id == None)).select(
            distinct=db.study_meta_data.location_description)
        count2 = len(a)
        count2 = int(count2)
        message = ()

        if ds_count < 1:
            message = "You have not uploaded any data yet"
        elif (count >= 1) & (count2 >= 1):
            message = "You have %s taxonomic entries and %s geographic entries to standardise," \
                      "click on the standardise button above and follow the insructions" % (count, count2)
        elif (count >= 1) & (count2 < 1):
            message = "You have %s taxonomic entries to standardise," \
                      "click on the standardise button above and follow the insructions" % count
        elif (count < 1) & (count2 >= 1):
            message = "You have %s geographic entries to standardise" % count2
        elif (count < 1) & (count2 < 1):
            message = "All taxonomic and geographic data has been standardised for this data set!"

        query = db(db.study_meta_data.publication_info_id == publication_info_id).count()

        if query == 0:
            response.flash = "You have not yet submitted any data yet," \
                             "click on 'Add time series data to add a data set'!"
        elif (count >= 1) | (count2 >= 1):
            response.flash = 'You still need to standardise entries!'
        else:
            response.flash = 'This is a list of all the standardised  time series data linked to this data set!'
        links = [lambda row: A('View time series data entries', _class="btn btn-primary",
                               _href=URL("vecdyn", "view_time_series_data",
                                         vars={'study_meta_data_id': row.id,
                                               'publication_info_id': publication_info_id})),
                 ]
        query = ((db.study_meta_data.taxon_id == None) | (db.study_meta_data.geo_id == None) &
                 (db.study_meta_data.publication_info_id == publication_info_id))
        form = SQLFORM.grid(query, field_id=db.study_meta_data.id,
                            fields=[db.study_meta_data.taxon,
                                    db.study_meta_data.taxon_id,
                                    db.study_meta_data.location_description,
                                    db.study_meta_data.geo_id],
                            headers={'study_meta_data.taxon': 'Original Taxon',
                                     'study_meta_data.taxon_id': 'Replacement Taxon Name',
                                     'study_meta_data.location_description': 'Original Location Description',
                                     'study_meta_data.geo_id': 'Replacement Location ID'},
                            maxtextlength=200, links=links,
                            searchable=True, advanced_search=False, deletable=False,
                            editable=False, details=False, create=False, csv=False)
        return locals()


@auth.requires_membership('VectorbiteAdmin')
def edit_meta_data():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    rows = db((db.study_meta_data.id == study_meta_data_id) & (db.study_meta_data.taxon_id == db.gbif_taxon.taxon_id)
              & (db.study_meta_data.geo_id == db.gaul_admin_layers.geo_id)).select()
    response.flash = 'Edit meta-data entry!'
    db.study_meta_data.title.writable = False
    db.study_meta_data.title.readable = False
    db.study_meta_data.taxon.writable = False
    db.study_meta_data.location_description.writable = False
    db.study_meta_data.taxon_id.writable = False
    db.study_meta_data.geo_id.writable = False
    db.study_meta_data.publication_info_id.writable = False
    db.study_meta_data.taxon_id.readable = False
    db.study_meta_data.geo_id.readable = False
    db.study_meta_data.publication_info_id.readable = False
    form = SQLFORM(db.study_meta_data, study_meta_data_id, showid=False, comments=False
                   )
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submitted your changes'
        redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    return locals()


# Write a function if name is in db do something, if not standardise data
@auth.requires_membership('VectorbiteAdmin')
def standardise_taxon():
    response.flash = 'You have uploaded taxonomic data that is not recognised in our database, ' \
                     'you need to standardise this manually.' \
                     'Click on the link next to each taxon name to search for equivalent taxon names!'
    publication_info_id = request.get_vars.publication_info_id
    # Page variable used in redirection to various standardization pages
    page = 'standardise_taxon'
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select(orderby=db.study_meta_data.taxon_id)
    taxon_entries = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxon_id == None)).select(
        distinct=db.study_meta_data.taxon)
    count = len(taxon_entries)
    geo_entries = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.geo_id == None)).select(
        distinct=db.study_meta_data.location_description)
    geo_entries_count = len(geo_entries)
    geo_entries_count = int(geo_entries_count)
    first_row = rows.first()
    if first_row.taxon_id is None:
        pass
    else:
        response.flash = 'Now standardise geo data'
        redirect(URL("vecdyn", "standardise_geo_data", vars={'publication_info_id': publication_info_id}))
    return locals()


# Write a function if name is in db do something, if not standardise data
@auth.requires_membership('VectorbiteAdmin')
def re_standardise_taxon():
    # Page variable used in redirection to various standardization pages
    page = 're_standardise_taxon'
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.id
    taxon_entries = db(db.study_meta_data.publication_info_id == publication_info_id).select(distinct=db.study_meta_data.taxon_id)
    # form = SQLFORM.grid(query,
    #                     field_id=db.study_meta_data.id,
    #                     groupby=db.study_meta_data.taxon,
    #                     fields=[db.study_meta_data.taxon,
    #                             db.study_meta_data.taxon_id],
    #                     headers={'study_meta_data.taxon': 'Original Taxon Name',
    #                              'study_meta_data.taxon_id': 'Replacement Taxon Name'},
    #                     links=links, maxtextlength=200, searchable=True, advanced_search=False,
    #                     deletable=False, editable=False,
    #                     details=False, create=False, csv=False
    #                     )
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def taxon_select():
    # Page variable used in redirection to various standardization pages
    page = request.get_vars.page
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    taxon = request.get_vars.taxon
    meta_edit = request.get_vars.meta_edit
    response.flash = 'Now search and select the taxon used in the study,' \
                     'if you make a mistake hit the "Cancel" button to restart'
    [setattr(f, 'readable', False)
     for f in db.gbif_taxon
     if f.name not in ('db.gbif_taxon.canonical_name, db.gbif_taxon.genus_or_above,'
                       'db.gbif_taxon.taxonomic_rank')]
    links = [lambda row: A('Select',
                           _class="btn btn-primary",
                           _href=URL("vecdyn", "taxon_confirm",
                                     vars={'taxon_id': row.taxon_id,
                                           'publication_info_id': publication_info_id,
                                           'taxon': taxon,
                                           'page': page,
                                           'meta_edit': meta_edit,
                                           'canonical_name': row.canonical_name,
                                           'study_meta_data_id': study_meta_data_id}))]
    db.gbif_taxon.taxon_id.readable = False
    grid = SQLFORM.grid(db.gbif_taxon,links=links, searchable=True, advanced_search=False, deletable=False, editable=False, details=False,  create=False, csv=False, maxtextlength=50)
    search_input = grid.element('#w2p_keywords')
    if search_input:
        search_input['_value'] = taxon
    # grid.search.default = request.get_vars.get_vars.taxon
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def taxon_confirm():
    # Page variable used in redirection to various standardization pages
    page = request.get_vars.page
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    canonical_name = request.get_vars.canonical_name
    taxon = request.get_vars.taxon
    taxon_id = request.get_vars.taxon_id
    meta_edit = request.get_vars.meta_edit
    form = FORM(INPUT(_type='submit', _value='Confirm', _class="btn btn-primary"))
    if form.process().accepted:
            redirect(URL("vecdyn", "taxon_insert", vars={'publication_info_id': publication_info_id,
                                                         'study_meta_data_id': study_meta_data_id,
                                                         'canonical_name': canonical_name,
                                                         'taxon_id': taxon_id,
                                                         'taxon': taxon,
                                                         'page': page,
                                                         'meta_edit': meta_edit,
                                                         'publication_info_id': publication_info_id}))
    return locals()


@auth.requires_membership('VectorbiteAdmin')
# Searches through all the entries for a taxon  and adds the tax standardized taxon name to each row
def taxon_insert():
    # Page variable used in redirection to various standardization pages
    page = request.get_vars.page
    taxon = request.get_vars.taxon
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    canonical_name = request.get_vars.canonical_name
    taxon_id = request.get_vars.taxon_id
    meta_edit = request.get_vars.meta_edit
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
    for row in rows:
        if taxon == row.taxon:
            row.update_record(taxon_id=taxon_id)
        else:
            continue
    if page == 're_standardise_taxon':
        session.flash = 'Success!'
        redirect(URL("vecdyn", "re_standardise_taxon", vars={'publication_info_id': publication_info_id,
                                                             'study_meta_data_id': study_meta_data_id}))
    else:
        redirect(URL("vecdyn", "standardise_taxon", vars={'publication_info_id': publication_info_id}))
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def standardise_geo_data():
    # Page variable used in redirection to various standardization pages
    page = 'standardise_geo_data'
    response.flash = 'Please standardise geo data. ' \
                     'Click on the link next to each geo description name to search for equivalent geo names!'
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.id
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select(orderby=db.study_meta_data.geo_id)
    geo_entries = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.geo_id == None)).select(distinct=db.study_meta_data.location_description)
    count = len(geo_entries)
    first_row = rows.first()
    if first_row.geo_id is None:
        pass
    else:
        response.flash = 'All data attached to this data set has been standardised standardise'
        redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def re_standardise_geo_data():
    # Page variable used in redirection to various standardization pages
    page = 're_standardise_geo_data'
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.id
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select(distinct=db.study_meta_data.location_description)
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def location_select():
    # Page variable used in redirection to various standardization pages
    page = request.get_vars.page
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    location_description = request.get_vars.location_description
    db.gaul_admin_layers.geo_id.readable = False
    [setattr(f, 'readable', False)
     for f in db.gaul_admin_layers
     if f.name not in ('db.gaul_admin_layers.adm0_name, db.gaul_admin_layers.adm1_name, db.gaul_admin_layers.adm2_name')]
    links = [lambda row: A('Select', _class="btn btn-primary",_href=URL("vecdyn", "geo_confirm",
                                                                         vars={'geo_id': row.geo_id,
                                                                                'page': page,
                                                                               'study_meta_data_id': study_meta_data_id,
                                                                               'adm0_name': row.adm0_name,
                                                                               'adm1_name': row.adm1_name,
                                                                               'adm2_name': row.adm2_name,
                                                                               'location_description': location_description,
                                                                               'publication_info_id': publication_info_id}))]
    response.flash = 'Now select a geographical location which best describes the study location'
    grid = SQLFORM.grid(db.gaul_admin_layers, orderby=db.gaul_admin_layers.adm0_name|db.gaul_admin_layers.adm1_name|db.gaul_admin_layers.adm2_name,
                        headers=
                        {'gaul_admin_layers.adm0_name': 'Country Name',
                        'gaul_admin_layers.adm1_name': 'Administrative Division 1',
                        'gaul_admin_layers.adm2_name': 'Administrative Division 2'},
                        links=links, searchable=True, advanced_search=False,
                        deletable=False, editable=False, details=False, create=False, csv=False)
    search_input = grid.element('#w2p_keywords')
    if search_input:
        search_input['_value'] = location_description
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def geo_confirm():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    # Page variable used in redirection to various standardization pages
    page = request.get_vars.page
    geo_id = request.get_vars.geo_id
    adm0_name = request.get_vars.adm0_name
    adm1_name = request.get_vars.adm1_name
    adm2_name = request.get_vars.adm2_name
    location_description = request.get_vars.location_description
    form = FORM(INPUT(_type='submit', _value='Confirm', _class="btn btn-primary"))
    if form.process().accepted:
        redirect(URL("vecdyn", "geo_st_insert",
                     vars={'geo_id': geo_id,
                           'study_meta_data_id': study_meta_data_id,
                           'page': page,
                           'location_description': location_description,
                           'publication_info_id': publication_info_id}))
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def geo_st_insert():
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    geo_id = request.get_vars.geo_id
    # Page variable used in redirection to various standardization pages
    page = request.get_vars.page
    location_description = request.get_vars.location_description
    rows = db(db.study_meta_data.publication_info_id == publication_info_id).select()
    for row in rows:
        if location_description == row.location_description:
            row.update_record(geo_id=geo_id)
        # else:
        #    continue
    if page == 're_standardise_geo_data':
        session.flash = 'Success!'
        redirect(URL("vecdyn", "re_standardise_geo_data", vars={'publication_info_id': publication_info_id,
                                                       'study_meta_data_id': study_meta_data_id}))
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
    form = SQLFORM.grid(db.time_series_data.study_meta_data_id  == study_meta_data_id, paginate=50, searchable=True, advanced_search=False,
                        deletable=False, editable=False, details=False, create=False,csv=False)
    if db(db.time_series_data.id).count() == 0:
        response.flash = 'You have not added any time series data to this dataset'
    else:
        response.flash = 'Time series data'
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def edit_time_series_entry():
    study_meta_data_id = request.get_vars.study_meta_data_id
    publication_info_id = request.get_vars.publication_info_id
    time_series_entry = request.get_vars.id
    db.time_series_data.study_meta_data_id.writable = False
    db.time_series_data.study_meta_data_id.readable = False
    form = SQLFORM(db.time_series_data, time_series_entry, showid=False, comments=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submitted your changes'
        redirect(URL('vecdyn', 'view_time_series_data', vars={'study_meta_data_id': study_meta_data_id}))
    return locals()



