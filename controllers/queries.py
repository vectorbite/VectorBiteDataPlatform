
#####VecDyn query




@auth.requires_login()
def vec_dyn_query():
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

    # control which fields available
    [setattr(f, 'readable', False) for f in db.taxon
        if f.name not in ('db.taxon.tax_species,db.taxon.tax_genus,'
                          'db.taxon.tax_family,db.taxon.tax_order')]
   # [setattr(f, 'readable', False) for f in db.StudyLocation
   #     if f.name not in ('db.StudyLocation.Country,db.StudyLocation.CountyStateProvince')]
    # MainID is not made unreadable, so that it can be accessed by the export controller
    [setattr(f, 'readable', False) for f in db.study_data
        if f.name not in ('db.study_data.id, db.study_data.location_description')]

    # Add selectability checkboxes
    select = [('Download selected',
               lambda ids : redirect(URL('queries', 'vec_dyn_download', vars=dict(ids=ids))),
               'btn btn-default')]

    # Adding an exporter that grabs all the data from a query,
    # the name _with_hidden_cols is needed to expose the MainID in the
    # rows passed to the exporter class. Note that nothing unreadable
    # can be exposed.
    export = dict(data_with_hidden_cols=(ExporterAll, 'Export All'),
                  csv_with_hidden_cols=False,
                  csv=False, xml=False, html=False, json=False,
                  tsv_with_hidden_cols=False, tsv=False)

    # turn the MainID into a download link
    db.study_data.id.represent = lambda value, row: A(value, _href=URL("queries","vec_dyn_download",
                                                    vars={'ids': row.study_data.id}))

    # get the grid
    grid = SQLFORM.grid((db.taxon.taxonID == db.study_data.taxon_id)&
                        (db.gaul_admin_layers.ADM_CODE == db.study_data.location_ID),
                        exportclasses=export,
                        ignore_common_filters=True,
                        field_id=db.study_data.id,
                        fields= [db.study_data.id,
                                 db.taxon.tax_species, db.taxon.tax_genus,
                                 db.taxon.tax_family, db.taxon.tax_order,
                                 db.taxon.tax_class, db.taxon.tax_phylum,
                                 db.gaul_admin_layers.ADM0_NAME, db.gaul_admin_layers.ADM1_NAME,
                                 db.study_data.location_description],
                        headers={'taxon.tax_species' : 'Taxon Name',
                                 'taxon.tax_genus' : 'Genus',
                                 'taxon.tax_family' : 'Family',
                                 'taxon.tax_order' : 'Order',
                                 'taxon.tax_class' : 'Class',
                                 'taxon.tax_phylum' : 'Phylum',
                                 'gaul_admin_layers.ADM0_NAME' : 'Country',
                                 'gaul_admin_layers.ADM1_NAME' : 'Region',
                                 'gaul_admin_layers.ADM2_NAME': 'County',
                                 'study_data.id' : 'Dataset ID' },
                        maxtextlength=100,
                        selectable=select,
                        deletable=False, editable=False, details=False, create=False)

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
        exp_all = A("Download all", _class="btn btn-default",
                    _href=exp_menu[1].attributes['_href'],
                    _style='padding:6px 12px;line-height:20px')
        fake_exp_sel = INPUT(_value='Download selected', _type='submit',
                            _class="btn btn-default", _id='fake_exp_sel',
                            _style='padding:6px 12px;line-height:20px')

        # add the buttons after the end of the web2py console form
        console = grid.element('.web2py_console')
        console[1].insert(1, CAT(exp_all, fake_exp_sel))

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

def _get_data_csv(ids):
    """
    Internal function that gets the required fields for downloading datasets
    for a given set of MainID ids and returns the data formatted as csv.

    This compilation is needed by both the dataset download controller
    and the Exporter class, so define here once and call from each.
    """

    rows = db((db.study_data.id.belongs(ids) &
              (db.taxon.taxonID == db.study_data.taxon_id) &
              (db.gaul_admin_layers.ADM_CODE == db.study_data.location_ID) &
              (db.collection_info.id == db.study_data.collection_info_id) &
              (db.sample_data.study_data_id == db.study_data.id)),ignore_common_filters=True).select(
                    db.study_data.title, db.gaul_admin_layers.ADM0_NAME, db.gaul_admin_layers.ADM1_NAME,db.gaul_admin_layers.ADM2_NAME,
                    db.gaul_admin_layers.centroid_latitude, db.gaul_admin_layers.centroid_longitude, db.gaul_admin_layers.ADM_CODE,
                    db.study_data.location_description,db.study_data.location_environment,
                    db.study_data.study_lat_DD, db.study_data.study_long_DD, db.study_data.geo_datum,
                    db.study_data.spatial_accuracy,db.study_data.location_extent,db.study_data.species_id_method,
                    db.study_data.study_design,db.study_data.sampling_strategy,db.study_data.sampling_method,
                    db.study_data.sampling_protocol,db.study_data.measurement_unit,db.study_data.study_collection_area,
                    db.study_data.value_transform,db.taxon.tax_species, db.taxon.tax_genus, db.taxon.tax_family,
                    db.taxon.tax_order, db.taxon.tax_class, db.taxon.tax_phylum,
                    db.study_data.location_description,db.sample_data.sample_start_date, db.sample_data.sample_start_time,
                    db.sample_data.sample_end_date, db.sample_data.sample_end_time, db.sample_data.value,
                    db.sample_data.sample_info, db.sample_data.sample_name,db.sample_data.sample_sex,
                    db.sample_data.sample_lat_DD, db.sample_data.sample_long_DD, db.collection_info.title,
                    db.collection_info.collection_authority,db.collection_info.DOI,db.collection_info.publication_date,
                    db.collection_info.description,db.collection_info.contact_name,db.collection_info.contact_email)
    return rows.as_csv()



def vec_dyn_download():

    """
    Function to return the data of records matching the ids
    """

    # Get the ids. If there are multiple ids, then we get a list,
    # and we need an iterable for belongs, so all we have to trap
    # is a single ID which comes in as a string
    ids = request.vars['ids']
    if isinstance(ids, str):
        ids = [ids]

    data = _get_data_csv(ids)

    # and now poke the text object out to the browser
    response.headers['Content-Type'] = 'text/csv'
    attachment = 'attachment;filename=vec_dyn_download_{}.txt'.format(datetime.date.today().isoformat())
    response.headers['Content-Disposition'] = attachment

    raise HTTP(200, data,
               **{'Content-Type':'text/csv',
                  'Content-Disposition':attachment + ';'})


class ExporterAll(object):

    """
    Used to export all the data associated with rows in the grid
    """

    file_ext = "csv"
    content_type = "text/csv"

    def __init__(self, rows):
        self.rows = rows

    def export(self):

        if self.rows:
            # expand rows to get full data and return that
            request.vars._export_filename = "yourname"
            ids = [rw.study_data.id for rw in self.rows]

            # currently simple check that we aren't trying to export too much
            if len(ids) > 50:
                return 'Download all is currently restricted to searches including fewer than 50 records.'
            else:
                data = _get_data_csv(ids)
                return data
        else:
            return
