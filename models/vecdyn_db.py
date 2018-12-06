# -*- coding: utf-8 -*-


# VecDyn

###add ondelete='CASCADE' to these tables, so


db.define_table('data_set_upload',
                Field('csvfile','upload',uploadfield=False, requires = IS_UPLOAD_FILENAME(extension='csv')))


db.define_table('collection_author',
    Field('name', 'string', notnull=True, unique=True),
    Field('description', 'text'),
                format='%(name)s')

DATARIGHTS = ('Open', 'Embargo', 'Closed')

DATATYPE = ('Abundance', 'Presence/Absence')

db.define_table('publication_info',
                Field('title', unique=True, type='string', required=True, comment ='Short title identifying the data collection'),
                Field('collection_author', db.collection_author,
                      requires=IS_IN_DB(db, 'collection_author.id', 'collection_author.name')),
                Field('dataset_doi', type='string', comment = 'Digital Object Identifier for the dataset'),
                Field('publication_doi', type='string', comment = 'If linked to a publication, enter the Digital Object Identifier of the publication'),
                Field('description', type='text',  required=True, comment='Brief description of the dataset'),
                Field('url', requires=IS_EMPTY_OR(IS_URL()), comment = 'Web link to dataset or collection author website'),
                Field('contact_name', type='string', comment = 'Lead author or best person to contact with any enquiries about the dataset'),
                Field('contact_affiliation', type='string', comment = 'Name of main organization is the contact above affiliated with'),
                Field('email', requires=IS_EMAIL()),
                Field('orcid', type='string', comment = 'Enter for name of main contact, ORCID is a digital identifier which provides researchers with a unique ID, see www.orcid.org'),
                Field('dataset_license', type='string', comment = 'e.g. Creative Commons license CC0 “No Rights Reserved”'),
                Field('data_rights', requires=IS_IN_SET(DATARIGHTS), default=DATARIGHTS[2]),
                Field('embargo_release_date', type ='date', requires=IS_EMPTY_OR(IS_DATE()), comment = 'If dataset is under embargo for a period of time please add its release date'),
                Field('submit', type ='boolean',default=False),
                Field('data_set_type', requires=IS_IN_SET(DATATYPE), default=DATATYPE[0]),
                auth.signature)#,
                #format='%(id)s')

###could write a query to automatically update embargo date once it reaches data >= today
today = datetime.date.today()
embargo_status_updates = db((db.publication_info.data_rights == 'Embargo') & (db.publication_info.embargo_release_date <= today)).select()
for row in embargo_status_updates:
    row.update_record(data_rights='Open', embargo_release_date=None)

def show_data_rights(data_rights,row=None):
    return SPAN(data_rights,_class=data_rights)

db.publication_info.data_rights.represent = show_data_rights


#if db(db.study_meta_data.id>0).count() == 0:
 #   db.study_meta_data.truncate()

db.define_table('study_meta_data',
                Field('title'), #0
                Field('taxon'), #1
                Field('location_description', type = 'string', required=True,  comment='Study location description'),
                Field('study_collection_area', type = 'string', comment='The spatial extent (area or volume) of the sample'), #3
                Field('geo_datum', type='string', comment='Indicate Geodetic datum e.g. wgs 84'),
                Field('gps_obfuscation_info', type='string', comment='Indicate Geodetic datum e.g. wgs 84'),#4
                Field('species_id_method', type = 'string', comment='Species Identification Method'), #5
                Field('study_design', type = 'string', comment='Study design methodology'), #6
                Field('sampling_strategy', type = 'string', comment='Indicate the strategy used to select the sample'), #7
                Field('sampling_method', type = 'string', required=True, comment='Sampling apparatus (e.g.  trap type, observation method)'), #8
                Field('sampling_protocol', type = 'string', comment='How entities were sampled'), #9
                Field('measurement_unit', type = 'string', required=True, comment='Unit of measurement'), #10
                Field('value_transform', type = 'string', comment='Note if the original values have been transformed'), #11
                Field('taxonID', default=None), #12
                Field('ADM_CODE', default=None), #13
                Field('publication_info_id', 'reference publication_info')) #14

db.study_meta_data.publication_info_id.requires = IS_IN_DB(db, db.publication_info.id)#, '%(title)s')

if db(db.study_meta_data.id>0).count() == 0:
    db.study_meta_data.truncate()


db.define_table('time_series_data',
                Field('sample_start_date', type = 'date', requires=IS_DATE(), comment='date of sample was set, leave blank if not applicable to the study'),
                Field('sample_start_time', type = 'time', required=False, comment='time of sample was set, leave blank if not applicable to the study'),
                Field('sample_end_date', type = 'date', requires=IS_DATE(), comment='Date of sample collection'),
                Field('sample_end_time', type = 'time', required=False, comment='time of sample collection'),
                Field('value'),#type = 'integer', comment='The numerical amount or result from the sample collection'),
                Field('sample_sex', type = 'string', comment='sex of sample if applicable'),
                Field('sample_stage', type = 'string', comment='life stage of sample if applicable'),
                Field('sample_location', type = 'string', comment='Additional sample information'),
                Field('sample_collection_area', type='string', comment='The spatial extent (area or volume) of the sample'),
                Field('sample_lat_dd', type = 'string', comment='Latitude of sample area as a decimal degree'),
                Field('sample_long_dd', type = 'string', comment='Longitude of sample area as a decimal degree'),
                Field('sample_environment', type = 'string', comment='General description about the sample location'),
                Field('additional_location_info', type = 'string', comment='Additional sample information'),
                Field('additional_sample_info', type = 'string', comment='Additional sample information'),
                Field('sample_name', type = 'string', comment ='A human readable sample name'),
                Field('study_meta_data_id'))


if db(db.time_series_data.id>0).count() == 0:
    db.time_series_data.truncate()


#THIS IS FOR SELECT_OR_ADD
class SelectOrAdd(object):
    def __init__(self, controller=None, function=None, form_title=None, button_text=None, dialog_width=450):
        if form_title == None:
            self.form_title = T('Add New')
        else:
            self.form_title = T(form_title)
        if button_text == None:
            self.button_text = T('Add')
        else:
            self.button_text = T(button_text)
        self.dialog_width = dialog_width

        self.controller = controller
        self.function = function

    def widget(self, field, value):
        #generate the standard widget for this field
        from gluon.sqlhtml import OptionsWidget
        select_widget = OptionsWidget.widget(field, value)

        #get the widget's id (need to know later on so can tell receiving controller what to update)
        my_select_id = select_widget.attributes.get('_id', None)
        add_args = [my_select_id]
        #create a div that will load the specified controller via ajax
        form_loader_div = DIV(LOAD(c=self.controller, f=self.function, args=add_args, ajax=True), _id=my_select_id + "_dialog-form", _title=self.form_title)
        #generate the "add" button that will appear next the options widget and open our dialog
        activator_button = A(T(self.button_text), _class='button button-primary', _id=my_select_id + "_option_add_trigger")
        #create javascript for creating and opening the dialog
        js = 'jQuery( "#%s_dialog-form" ).dialog({autoOpen: false, show: "blind", hide: "explode", width: %s});' % (my_select_id, self.dialog_width)
        js += 'jQuery( "#%s_option_add_trigger" ).click(function() { jQuery( "#%s_dialog-form" ).dialog( "open" );return false;}); ' % (my_select_id, my_select_id)  # decorate our activator button for good measure
        js += 'jQuery(function() { jQuery( "#%s_option_add_trigger" ).button({text: true, icons: { primary: "ui-icon-circle-plus"} }); });' % (my_select_id)
        jq_script = SCRIPT(js, _type="text/javascript")

        wrapper = DIV(_id=my_select_id + "_adder_wrapper")
        wrapper.components.extend([select_widget, form_loader_div, activator_button, jq_script])
        return wrapper


add_option = SelectOrAdd(form_title=T("Add a new something"),
                                              controller="vecdyn",
                                              function="add_collection_author",
                                              button_text=T("Add New"),
                                              dialog_width=600)


db.publication_info.collection_author.widget = add_option.widget

