# -*- coding: utf-8 -*-

me = auth.user_id
import logging

logger = logging.getLogger("web2py.app.vbdp")
logger.setLevel(logging.DEBUG)


# ----------------------------------------------------------------------------------------------------------------------
# The following code is for USER upload and download of data
# Ignore_common_filters are applied so only the users who have created a dataset can access them
# ----------------------------------------------------------------------------------------------------------------------

def index():
    # dsets = db(db.publication_info).count()
    # obs =  db(db.time_series_data).count()
    # taxa = db(db.study_meta_data.taxon).select(distinct=db.study_meta_data.taxon, cache=(cache.ram, 3600), cacheable=True)
    # taxa = len(taxa)
    # countries = db(db.study_meta_data.geo_id == db.gaul_admin_layers.id).select(
    #     distinct=db.gaul_admin_layers.adm0_name, cache=(cache.ram, 36000), cacheable=True)
    # countries = len(countries)
    # regions = db(db.study_meta_data.geo_id == db.gaul_admin_layers.id).select(
    #     distinct=db.gaul_admin_layers.adm1_name, cache=(cache.ram, 36000), cacheable=True)
    # regions = len(regions)
    # counties = db(db.study_meta_data.geo_id == db.gaul_admin_layers.id).select(
    #     distinct=db.gaul_admin_layers.adm2_name, cache=(cache.ram, 36000), cacheable=True)
    # counties = len(counties)
    dsets = 0
    obs = 0
    taxa = 0
    countries = 0
    regions = 0
    counties = 0
    coords = 0
    # trap_locs = {}
    # trap_locs = db(db.time_series_data).select(db.time_series_data.sample_lat_dd, db.time_series_data.sample_long_dd)
    #coords = []
    # for i in db(db.time_series_data).select(db.time_series_data.sample_lat_dd, db.time_series_data.sample_long_dd,
    #                                         distinct=True):
    #     coords.append(i)
    # coords = len(coords)
    return dict(dsets=dsets,obs=obs,taxa=taxa,countries=countries,regions=regions,counties=counties,coords=coords)



def about():
    # rows = db(db.index_page_updates).select(orderby=~db.index_page_updates.created_on)
    return locals()

# imports data sets submitted by users - only meta data and sample data (time series)
def queue_task():
    scheduler.queue_task('vecdyn_importer', prevent_drift=False, repeats=0, period=5)

# updates all vecdyn data base tables
def queue_task_2():
        scheduler.queue_task('vecdyn_bulk_importer', prevent_drift=False, repeats=0, period=5)

# updates all vecdyn data base tables
def queue_task_3():
        scheduler.queue_task('vecdyn_taxon_standardiser', prevent_drift=False, repeats=0, period=4)


# The following function imports a vecdyn csv
@auth.requires_membership('VectorbiteAdmin')
def vecdyn_csv_uploader():
    publication_info_id = request.get_vars.publication_info_id
    db.data_set_upload.publication_info_id.default = publication_info_id
    db.data_set_upload.status.default = 'pending'
    db.data_set_upload.publication_info_id.readable = False
    db.data_set_upload.status.readable = False
    response.flash = 'Now upload a time series data set, make sure this is in csv format'
    # Get the publicaton infor id from the previous page
    form = SQLFORM(db.data_set_upload, comments=False, fields=['csvfile'],
                   labels={'csvfile': 'Click to search and select a file:'})
    if form.process().accepted:
        response.flash = 'Thanks data submitted for upload, you will recieve an email once data has been uploaded into the db'
        redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    return locals()


# The following function imports a vecdyn csv
@auth.requires_membership('VectorbiteAdmin')
def vecdyn_csv_bulk_uploader():
    db.data_set_bulk_upload.status.default = 'pending'
    db.data_set_bulk_upload.readable = False
    response.flash = 'Now upload your data set, make sure this is in csv format'
    # Get the publicaton infor id from the previous page
    form = SQLFORM(db.data_set_bulk_upload, comments=False, fields=['csvfile'],
                   labels={'csvfile': 'Click to search and select a file:'})
    if form.process().accepted:
        response.flash = 'Data uploaded'
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def submit_vecdyn_data():
    """function set up to Submit vecdyn  data through the website"""
    db.task.task_type.default = 'vecdyn data submission'
    db.task.task_type.readable = False
    db.task.task_type.writable = False
    db.task.status.readable = False
    db.task.status.writable = False
    db.task.assigned_to.writable = False
    db.task.assigned_to.readable = False
    db.task.deadline.writable = False
    db.task.deadline.readable = False
    db.task.file.requires = IS_UPLOAD_FILENAME(extension='csv')
    add_option_2 = SelectOrAdd(form_title="Add new collection author",
                               controller="default",
                               function="add_collection_author",
                               button_text="Add New")
    # assign widget to field
    db.task.collection_author.widget = add_option.widget
    form = SQLFORM(db.task, labels={'task_type': 'Data set category'}).process()

    # Here we would like to know if the DB is written to, and also whether people are having problems with the form
    # (Hence logging on errors)
    if form.accepted:
        logger.info("VD dataset submitted: task ID {} - {}".format(form.vars["id"], form.vars["title"]))
        redirect(URL('index'))
    elif form.errors:
        logger.debug("VD data submission errors: {}".format(len(form.errors)))
        logger.debug("in the following fields: {}".format(form.errors.keys()))

        # response.flash = CENTER(B('Problems with the form in the following fields: {}'
        #                           .format(form.errors.keys())), _style='color: red')
    else:
        response.flash = 'please fill out the form in full and attach a csv file'

    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.js'))
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.theme.css'))
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def dataset_registration():
    task_id = request.get_vars.task_id
    if task_id is not None:
        myrecord = db(db.task.id == task_id).select().first()
        db.publication_info.title.default = myrecord.title
        # collection_author = myrecord.collection_author
        # collection_author = db(db.collection_author.name == collection_author).select().first()
        db.publication_info.collection_author.default = myrecord.collection_author
        db.publication_info.dataset_citation.default = myrecord.dataset_citation    # TODO: dataset doi missing
        db.publication_info.publication_citation.default = myrecord.publication_citation
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
                          'db.publication_info.dataset_citation,'
                          'db.publication_info.title,'
                          'db.publication_info.collection_author,'
                          'db.publication_info.created_by')]
    # db.publication_info.data_rights.represent = lambda data_rights, row: A(data_rights, _href=URL('edit_data_rights', args=row.id))
    links = [lambda row: A('Enter Dataset Control Panel', _href=URL("vecdyn", "view_data", vars={'publication_info_id': row.id}), _class="btn btn-primary")]
    form = SQLFORM.grid(db.publication_info, links=links, searchable=True, advanced_search=False, deletable=False,
                        editable=False, details=False, create=False, csv=False, maxtextlength=200,
                        fields=[
                            db.publication_info.title,
                            db.publication_info.collection_author,
                            db.publication_info.dataset_citation,
                            db.publication_info.data_rights],
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
    db.publication_info.dataset_citation.writable = False
    db.publication_info.dataset_citation.readable = False
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
    db.publication_info.publication_citation.writable = False
    db.publication_info.publication_citation.readable = False
    form = SQLFORM(db.publication_info, publication_info_id, showid=False)
    if form.process().accepted:
        session.flash = 'Thanks you have successfully submitted your changes'
        redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    return locals()



@auth.requires_membership('VectorbiteAdmin')
def view_data():
    # Query for publication info pages, found at the top of the view data pages
    publication_info_id = request.get_vars.publication_info_id
    publication_info_query = db(db.publication_info.id == publication_info_id).select().first()

    observations = db(db.time_series_data.publication_info_id == publication_info_id).count()

    taxon_entries = db(db.study_meta_data.publication_info_id == publication_info_id).count(
        distinct=db.study_meta_data.taxon)
    regions = db(db.study_meta_data.publication_info_id == publication_info_id).count(
        distinct=db.study_meta_data.location_description)

    unstan_tax = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxon_id == None)).count(distinct=db.study_meta_data.taxon)

    unstan_geo = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.geo_id == None)).count(distinct=db.study_meta_data.location_description)

    coords = []
    # for i in db(db.time_series_data.publication_info_id == publication_info_id).select(db.time_series_data.sample_lat_dd, db.time_series_data.sample_long_dd, distinct=True, cache=(cache.ram, 36000), cacheable=True):
    #     coords.append(i)
    # coords = len(coords)
    # Following queries count to see how many unstandardised entries are in the collection, unstandardised dates are
    # recognised by the absence of either a no taxon_id (None) or no geo_id (None) supplies user with a message
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
    query_2 = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.canonical_name != None) & (db.study_meta_data.geo_id == db.gaul_admin_layers.geo_id))
    form = SQLFORM.grid(query_2, field_id=db.study_meta_data.id,
                        fields=[db.study_meta_data.canonical_name,
                                db.gaul_admin_layers.adm2_name,
                                db.gaul_admin_layers.adm1_name,
                                db.gaul_admin_layers.adm0_name,
                                db.study_meta_data.study_design,
                                db.study_meta_data.sampling_method,
                                db.study_meta_data.measurement_unit,
                                db.study_meta_data.value_transform],
                        headers={'study_meta_data.canonical_name': 'Standardised taxon',
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
    return dict(form=form,  coords=coords, regions=regions,unstan_tax=unstan_tax,unstan_geo=unstan_geo,taxon_entries=taxon_entries,publication_info_query=publication_info_query,publication_info_id=publication_info_id, observations=observations)


@auth.requires_membership('VectorbiteAdmin')
def view_unstandardised_data():
        # User message code

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
        # query_2 = ((db.study_meta_data.taxon_id == None) | (db.study_meta_data.geo_id == None) &
        #          (db.study_meta_data.publication_info_id == publication_info_id))
        my_select = db((db.study_meta_data.publication_info_id == publication_info_id) & ((db.study_meta_data.taxon_id == None) | (db.study_meta_data.geo_id == None)))
        form = SQLFORM.grid(my_select, field_id=db.study_meta_data.id,
                            fields=[db.study_meta_data.taxon,
                                    db.study_meta_data.canonical_name,
                                    db.study_meta_data.location_description,
                                    db.study_meta_data.geo_id],
                            headers={'study_meta_data.taxon': 'Original Taxon',
                                     'study_meta_data.canonical_name': 'Replacement Taxon Name',
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
    # db.study_meta_data.title.writable = False
    # db.study_meta_data.title.readable = False
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
    if taxon_entries > 0:
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
    rows = db((db.study_meta_data.publication_info_id == publication_info_id) & (db.study_meta_data.taxon_id == db.gbif_taxon.taxon_id)).select(distinct=db.study_meta_data.taxon_id)
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
                                           'genus_or_above': row.genus_or_above,
                                           'taxonomic_rank': row.taxonomic_rank,
                                           'study_meta_data_id': study_meta_data_id}))]
    db.gbif_taxon.taxon_id.readable = False
    grid = SQLFORM.grid(db.gbif_taxon,links=links, searchable=True, advanced_search=False, deletable=False, editable=False, details=False,  create=False, csv=False, maxtextlength=50)
    search_input = grid.element('#w2p_keywords')
    if search_input:
        search_input['_value'] = taxon
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
    genus_or_above = request.get_vars.genus_or_above
    taxonomic_rank = request.get_vars.taxonomic_rank
    meta_edit = request.get_vars.meta_edit
    form = FORM(INPUT(_type='submit', _value='Confirm', _class="btn btn-primary"))
    if form.process().accepted:
            redirect(URL("vecdyn", "taxon_insert", vars={'publication_info_id': publication_info_id,
                                                         'study_meta_data_id': study_meta_data_id,
                                                         'taxon_id': taxon_id,
                                                         'canonical_name': canonical_name,
                                                         'genus_or_above': genus_or_above,
                                                         'taxonomic_rank': taxonomic_rank,
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
    genus_or_above = request.get_vars.genus_or_above
    taxonomic_rank = request.get_vars.taxonomic_rank
    for row in db(db.study_meta_data.publication_info_id == publication_info_id).iterselect():
        if taxon == row.taxon:
            row.update_record(taxon_id=taxon_id)
            row.update_record(canonical_name=canonical_name)
            row.update_record(genus_or_above=genus_or_above)
            row.update_record(taxonomic_rank=taxonomic_rank)
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
    # if first_row.geo_id < 1:
    #     pass
    # else:
    #     response.flash = 'All data attached to this data set has been standardised'
    #     redirect(URL("vecdyn", "view_data", vars={'publication_info_id': publication_info_id}))
    return locals()


@auth.requires_membership('VectorbiteAdmin')
def re_standardise_geo_data():
    # Page variable used in redirection to various standardization pages
    page = 're_standardise_geo_data'
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.id
    rows = db((db.study_meta_data.publication_info_id == publication_info_id) & ( db.study_meta_data.geo_id == db.gaul_admin_layers.geo_id)).select(distinct=db.study_meta_data.location_description)
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
    publication_info_id = request.get_vars.publication_info_id
    study_meta_data_id = request.get_vars.study_meta_data_id
    form = SQLFORM.grid(db.time_series_data.study_meta_data_id  == study_meta_data_id, paginate=50, searchable=True, advanced_search=False,
                        deletable=False, editable=False, details=False, create=False,csv=False)
    if db(db.time_series_data.id).count() == 0:
        response.flash = 'You have not added any time series data to this dataset'
    else:
        response.flash = 'Time series data'
    return locals()



import datetime

from gluon.tools import prettydate
# from datetime import datetime

week = datetime.timedelta(days=7)


# VecDyn query
# @auth.requires_login()
@auth.requires_membership('VectorbiteAdmin')
def vecdyn_taxon_location_query():
    """
    Controller to serve a searchable grid view of the vector dynamics
    datasets with a download function. We want to be able to download
    individual records, selected sets of records and all records
    covered by a query.

    The individual row / selected sets is handled by a download controller
    that grabs ids from the request variables and send back the data as
    a csv.

    The complete set of rows in a grid query is accessible to the export
    buttons within the grid code, so the download all option uses that
    mechanism but expands the rows to the datasets for each row before
    returning. Currently, this won't let you Download All for more than
    50 MainID records.
    """
    today = datetime.date.today()

    # control which fields available
    [setattr(f, 'readable', False) for f in db.publication_info
        if f.name not in ('db.publication_info.title, db.publication_info.collection_author')]
    [setattr(f, 'readable', False) for f in db.collection_author
     if f.name not in ('db.collection_author.name')]
    # MainID is not made unreadable, so that it can be accessed by the export controller
    [setattr(f, 'readable', False) for f in db.study_meta_data
        if f.name not in ('db.study_meta_data.canonical_name,db.study_meta_data.genus_or_above,'
                          'db.study_meta_data.taxonomic_rank'
                          'db.study_meta_data.location_description')]
    [setattr(f, 'readable', False) for f in db.gaul_admin_layers
     if f.name not in ('db.gaul_admin_layers.adm2_name, db.gaul_admin_layers.adm1_name, db.gaul_admin_layers.adm0_name')]

    # Add selectability checkboxes
    select = [('Download selected',
               lambda ids: redirect(URL('vecdyn', 'vec_dyn_download_1', vars=dict(ids=ids))),
               'btn btn-default')]

    # turn the study_meta_data.id into a download link
    db.study_meta_data.represent = lambda value, row: A(value, _href=URL("vecdyn", "vec_dyn_download_1",
                                                        vars={'ids': row.study_meta_data.id}))
    # get the grid
    # week = datetime.timedelta(days=7)
    # Field('deadline', 'datetime', default=request.now + week),
    # db.publication_info.collection_author.represent = lambda collection_author, row: \
    #    A(collection_author, _href=URL('edit_task', args=row.publication_info.collection_author))
    db.collection_author.name.represent = lambda name, row: \
        A(name, _href=URL('vecdyn', 'vecdyn_author_query', vars={'collection_author': row.collection_author.name}))
    grid = SQLFORM.grid((db.study_meta_data.publication_info_id == db.publication_info.id)
                        & (db.publication_info.collection_author == db.collection_author.id)
                        & (db.study_meta_data.taxon_id != 'notfound') # not found added by scheduler function
                        & (db.study_meta_data.canonical_name != None) #
                        & (db.publication_info.data_rights == 'open')
                        & (db.gaul_admin_layers.geo_id == db.study_meta_data.geo_id),
                        field_id=db.study_meta_data.id,
                        fields=[db.study_meta_data.canonical_name,
                                db.study_meta_data.genus_or_above,
                                db.study_meta_data.taxonomic_rank,
                                db.study_meta_data.location_description,
                                db.gaul_admin_layers.adm0_name,
                                db.gaul_admin_layers.adm1_name,
                                db.gaul_admin_layers.adm2_name,
                                db.publication_info.title,
                                db.collection_author.name,
                                ],

                        headers={'publication_info.title': 'Title',
                                 'collection_author.name': 'Collector',
                                 'study_meta_data.canonical_name': 'Taxon',
                                 'study_meta_data.genus_or_above': 'Genus_or_above',
                                 'study_meta_data.taxonomic_rank': 'taxonomic_rank',
                                 'gaul_admin_layers.adm2_name': 'Administrative Division 2',
                                 'gaul_admin_layers.adm1_name': 'Administrative Division 1',
                                 'gaul_admin_layers.adm0_name': 'Country Name',
                                 'study_meta_data.id': 'Dataset ID'},
                        maxtextlength=200,
                        paginate=10,
                        selectable=select,
                        deletable=False, editable=False, details=False, create=False)
    if grid.elements('th'):
        grid.elements('th')[0].append(SPAN('Select all', BR(), INPUT(_type='checkbox',
                                                                     _onclick="jQuery('input:checkbox').not(this).prop('checked', this.checked);"
                                                                     )))
    # The final bit of untidiness is the location of the buttons.
    # - The export 'menu' (a single button here) is at the bottom of the page.
    #   This button doesn't submit a form, just calls the page again with _export_type
    #   set, so we can simply move it.
    # - The Download selected button is more tricky: selectable turns the grid
    #   table into a form, which the download selected button needs to be inside.
    #   I've simply hidden it and added a fake button in the right location that
    #   uses JS to press the real submit. Having a fake submit and using JS to submit
    #   the form directly wasn't getting the request right, so this is easier!

    # The script we're setting up for is this:

    # <script type="text/javascript">
    #     $(document).ready(function() {
    #        $("#fake_exp_sel").click(function() {
    #            $("#exp_sel").click();
    #        });
    #     });
    # </script>

    # Create some buttons to add (one is just a link, masquerading
    # as a button, the other presses the hidden submit on the real form).
    # This code shouldn't run if no records are found by a search, since then
    # the export menu and the selectable form don't exist.
    exp_menu = grid.element('.w2p_export_menu')
    if exp_menu is not None:

        exp_menu = grid.element('.w2p_export_menu')
        fake_exp_sel = INPUT(_value='Download selected', _type='submit',
                             _class="btn btn-primary", _id='fake_exp_sel',
                             _style='padding:6px 12px;line-height:20px')

        # add the buttons after the end of the web2py console form
        console = grid.element('.web2py_console')
        #console[1].insert(1, CAT(exp_all, fake_exp_sel))
        console[1].insert(1, CAT(fake_exp_sel))

        # add an ID to the selection form, to allow JS to link the
        # new button to form submission
        sel_form = grid.element('.web2py_table form')
        sel_form['_id'] = 'select_form'

        # Delete the original export menu
        export_menu_idx = [x.attributes['_class'] for x in grid].index('w2p_export_menu')
        del grid[export_menu_idx]

        # hide the real export selected button and add an ID
        exp_sel = grid.element('.web2py_table .btn')
        exp_sel['_style'] = 'display:none;'
        exp_sel['_id'] = 'exp_sel'

    return dict(grid=grid)


def _get_data_csv_1(ids):
    """
    Internal function that gets the required fields for downloading datasets
    for a given set of MainID ids and returns the data formatted as csv.

    This compilation is needed by both the dataset download controller
    and the Exporter class, so define here once and call from each.
    """

    rows = db((db.study_meta_data.id.belongs(ids)) &
              (db.gaul_admin_layers.geo_id == db.study_meta_data.geo_id) &
              (db.publication_info.id == db.study_meta_data.publication_info_id) &
              (db.time_series_data.study_meta_data_id == db.study_meta_data.id)).select(
                    db.publication_info.title,
                    db.study_meta_data.canonical_name,
                    db.study_meta_data.genus_or_above,
                    db.study_meta_data.taxonomic_rank,
                    db.study_meta_data.taxon_id,
                    db.time_series_data.sample_start_date,
                    db.time_series_data.sample_start_time,
                    db.time_series_data.sample_end_date,
                    db.time_series_data.sample_end_time,
                    db.time_series_data.sample_value,
                    db.study_meta_data.measurement_unit,
                    db.study_meta_data.value_transform,
                    db.time_series_data.sample_sex,
                    db.time_series_data.sample_stage,
                    db.time_series_data.sample_location,
                    db.time_series_data.sample_collection_area,
                    db.time_series_data.sample_lat_dd,
                    db.time_series_data.sample_long_dd,
                    db.time_series_data.sample_environment,
                    db.time_series_data.additional_location_info,
                    db.time_series_data.additional_sample_info,
                    db.time_series_data.sample_name,
                    db.study_meta_data.species_id_method,
                    db.study_meta_data.study_design,
                    db.study_meta_data.sampling_strategy,
                    db.study_meta_data.sampling_method,
                    db.study_meta_data.sampling_protocol,
                    db.study_meta_data.measurement_unit,
                    db.study_meta_data.value_transform,
                    db.study_meta_data.location_description,
                    db.gaul_admin_layers.adm2_name,
                    db.gaul_admin_layers.adm1_name,
                    db.gaul_admin_layers.adm0_name,
                    db.gaul_admin_layers.geo_id,
                    db.study_meta_data.geo_datum,
                    db.study_meta_data.gps_obfuscation_info,
                    db.publication_info.description,
                    db.publication_info.collection_author,
                    db.publication_info.dataset_citation,
                    db.publication_info.publication_citation,
                    db.publication_info.description,
                    db.publication_info.url,
                    db.publication_info.contact_name,
                    db.publication_info.contact_affiliation,
                    db.publication_info.email,
                    db.publication_info.orcid,
                    db.publication_info.dataset_license)
    return rows.as_csv()


def vec_dyn_download_1():
    """
    Function to return the data of records matching the ids
    """

    # Get the ids. If there are multiple ids, then we get a list,
    # and we need an iterable for belongs, so all we have to trap
    # is a single ID which comes in as a string
    ids = request.vars['ids']
    if ids != None:
        if isinstance(ids, str):
            ids = [ids]
        data = _get_data_csv_1(ids)

        # and now poke the text object out to the browser
        response.headers['Content-Type'] = 'text/csv'
        attachment = 'attachment;filename=vec_dyn_download_1_{}.csv'.format(datetime.date.today().isoformat())
        response.headers['Content-Disposition'] = attachment

        raise HTTP(200, data,
                   **{'Content-Type': 'text/csv',
                      'Content-Disposition': attachment + ';'})

    else:
        redirect(URL("vecdyn", "vecdyn_taxon_location_query"))


import datetime

from gluon.tools import prettydate
# from datetime import datetime

week = datetime.timedelta(days=7)


# VecDyn query
# @auth.requires_login()
@auth.requires_membership('VectorbiteAdmin')
def vecdyn_author_query():
    """
    Controller to serve a searchable grid view of the vector dynamics
    datasets with a download function. We want to be able to download
    individual records, selected sets of records and all records
    covered by a query.

    The individual row / selected sets is handled by a download controller
    that grabs ids from the request variables and send back the data as
    a csv.

    The complete set of rows in a grid query is accessible to the export
    buttons within the grid code, so the download all option uses that
    mechanism but expands the rows to the datasets for each row before
    returning. Currently, this won't let you Download All for more than
    50 MainID records.
    """
    today = datetime.date.today()

    # control which fields available
    [setattr(f, 'readable', False) for f in db.publication_info
        if f.name not in ('db.publication_info.title, db.publication_info.collection_author,'
                          'db.publication_info.data_set_type,'
                          'db.publication_info.dataset_citation, db.publication_info.description')]
    [setattr(f, 'readable', False) for f in db.collection_author
     if f.name not in ('db.collection_author.id, db.collection_author.name')]

    # Add selectability checkboxes
    select = [('Download selected',
               lambda ids: redirect(URL('vecdyn', 'vec_dyn_download_2', vars=dict(ids=ids))),
               'btn btn-default')]

    # turn the study_meta_data.id into a download link
    db.publication_info.represent = lambda value, row: A(value, _href=URL("vecdyn", "vec_dyn_download_2",
                                                         vars={'ids': row.publication_info.id}))
    # get the grid
    # week = datetime.timedelta(days=7)
    # Field('deadline', 'datetime', default=request.now + week),
    #    A(name, _href=URL('edit_task', vars={'collection_author': row.collection_author.name}))
    collection_author = request.get_vars.collection_author
    if collection_author != None:
        collection_author = db(db.collection_author.name == collection_author).select().first()
        query = ((db.publication_info.collection_author == collection_author.id)
                 & (db.publication_info.data_rights == 'open'))
    else:
        query = ((db.publication_info.collection_author == db.collection_author.id)
                 & (db.publication_info.data_rights == 'open'))
    grid = SQLFORM.grid(query,
                        field_id=db.publication_info.id,
                        fields=[db.publication_info.title,
                                db.publication_info.collection_author,
                                db.publication_info.description,
                                db.publication_info.data_set_type],
                        headers={'publication_info.title': 'Title',
                                 'publication_info.collection_author': 'Collector',
                                 'publication_info.description': 'Description',
                                 'publication_info.data_set_type': 'Dataset Type'},
                        maxtextlength=200,
                        paginate=5,
                        selectable=select,
                        deletable=False, editable=False, details=False, create=False)
    # if grid.elements('th'):
    #     grid.elements('th')[0].append(SPAN('Selet all', BR(), INPUT(_type='checkbox',
    #                                                                  _onclick="jQuery('input:checkbox').not(this).prop('checked', this.checked);"
    #                                                                  )))
    # The final bit of untidiness is the location of the buttons.
    # - The export 'menu' (a single button here) is at the bottom of the page.
    #   This button doesn't submit a form, just calls the page again with _export_type
    #   set, so we can simply move it.
    # - The Download selected button is more tricky: selectable turns the grid
    #   table into a form, which the download selected button needs to be inside.
    #   I've simply hidden it and added a fake button in the right location that
    #   uses JS to press the real submit. Having a fake submit and using JS to submit
    #   the form directly wasn't getting the request right, so this is easier!

    # The script we're setting up for is this:

    # <script type="text/javascript">
    #     $(document).ready(function() {
    #        $("#fake_exp_sel").click(function() {
    #            $("#exp_sel").click();
    #        });
    #     });
    # </script>

    # Create some buttons to add (one is just a link, masquerading
    # as a button, the other presses the hidden submit on the real form).
    # This code shouldn't run if no records are found by a search, since then
    # the export menu and the selectable form don't exist.
    exp_menu = grid.element('.w2p_export_menu')
    if exp_menu is not None:

        fake_exp_sel = INPUT(_value='Download selected', _type='submit',
                             _class="btn btn-primary", _id='fake_exp_sel',
                             _style='padding:6px 12px;line-height:20px')

        # add the buttons after the end of the web2py console form
        console = grid.element('.web2py_console')
        console[1].insert(1, CAT(fake_exp_sel))

        # add an ID to the selection form, to allow JS to link the
        # new button to form submission
        sel_form = grid.element('.web2py_table form')
        sel_form['_id'] = 'select_form'

        # Delete the original export menu
        export_menu_idx = [x.attributes['_class'] for x in grid].index('w2p_export_menu')
        del grid[export_menu_idx]

        # hide the real export selected button and add an ID
        exp_sel = grid.element('.web2py_table .btn')
        exp_sel['_style'] = 'display:none;'
        exp_sel['_id'] = 'exp_sel'

    return dict(grid=grid)


def _get_data_csv_2(ids):
    """
    Internal function that gets the required fields for downloading datasets
    for a given set of MainID ids and returns the data formatted as csv.

    This compilation is needed by both the dataset download controller
    and the Exporter class, so define here once and call from each.
    """

    rows = db((db.publication_info.id.belongs(ids)) &
              (db.publication_info.collection_author == db.collection_author.id) &
              (db.study_meta_data.publication_info_id == db.publication_info.id) &
              (db.gaul_admin_layers.geo_id == db.study_meta_data.geo_id) &
              (db.time_series_data.study_meta_data_id == db.study_meta_data.id)).select(
                    db.publication_info.title,
                    db.study_meta_data.canonical_name,
                    db.study_meta_data.genus_or_above,
                    db.study_meta_data.taxonomic_rank,
                    db.study_meta_data.taxon_id,
                    db.time_series_data.sample_start_date,
                    db.time_series_data.sample_start_time,
                    db.time_series_data.sample_end_date,
                    db.time_series_data.sample_end_time,
                    db.time_series_data.sample_value,
                    db.study_meta_data.measurement_unit,
                    db.study_meta_data.value_transform,
                    db.time_series_data.sample_sex,
                    db.time_series_data.sample_stage,
                    db.time_series_data.sample_location,
                    db.time_series_data.sample_collection_area,
                    db.time_series_data.sample_lat_dd,
                    db.time_series_data.sample_long_dd,
                    db.time_series_data.sample_environment,
                    db.time_series_data.additional_location_info,
                    db.time_series_data.additional_sample_info,
                    db.time_series_data.sample_name,
                    db.study_meta_data.species_id_method,
                    db.study_meta_data.study_design,
                    db.study_meta_data.sampling_strategy,
                    db.study_meta_data.sampling_method,
                    db.study_meta_data.sampling_protocol,
                    db.study_meta_data.measurement_unit,
                    db.study_meta_data.value_transform,
                    db.study_meta_data.location_description,
                    db.gaul_admin_layers.adm2_name,
                    db.gaul_admin_layers.adm1_name,
                    db.gaul_admin_layers.adm0_name,
                    db.study_meta_data.geo_datum,
                    db.study_meta_data.gps_obfuscation_info,
                    db.publication_info.description,
                    db.collection_author.name,
                    db.publication_info.dataset_citation,
                    db.publication_info.publication_citation,
                    db.publication_info.description,
                    db.publication_info.url,
                    db.publication_info.contact_name,
                    db.publication_info.contact_affiliation,
                    db.publication_info.email,
                    db.publication_info.orcid,
                    db.publication_info.dataset_license)
    return rows.as_csv()


def vec_dyn_download_2():
    """
    Function to return the data of records matching the ids
    """

    # Get the ids. If there are multiple ids, then we get a list,
    # and we need an iterable for belongs, so all we have to trap
    # is a single ID which comes in as a string
    ids = request.vars['ids']
    if ids != None:
        if isinstance(ids, str):
            ids = [ids]
        data = _get_data_csv_2(ids)

        # and now poke the text object out to the browser
        response.headers['Content-Type'] = 'text/csv'
        attachment = 'attachment;filename=vec_dyn_download_2_{}.csv'.format(datetime.date.today().isoformat())
        response.headers['Content-Disposition'] = attachment

        raise HTTP(200, data,
                   **{'Content-Type': 'text/csv',
                      'Content-Disposition': attachment + ';'})

    else:
        redirect(URL("vecdyn_query_2", "vecdyn_author_query"))




