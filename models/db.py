# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
from gluon import current

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

import datetime
# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)



db = DAL(configuration.get('db.uri'),
         pool_size=configuration.get('db.pool_size'),
         migrate_enabled=configuration.get('db.migrate'),
         lazy_tables=True,
         #fake_migrate_all=True,
         check_reserved=['postgres', 'postgres_nonreserved'])

db2 = DAL(configuration.get('db2.uri'),
          pool_size=configuration.get('db2.pool_size'),
          migrate_enabled=configuration.get('db2.migrate'),
          lazy_tables=True,
          #fake_migrate_all=True,        # Allow fake migration to rebuild table metadata
          check_reserved=['postgres', 'postgres_nonreserved'])

current.db = db
# Make db2 available for use in vtfuncs
current.db2 = db2



# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))



'''this table is referenced in the user registration'''
db.define_table('country',
                Field('Country_or_Area', 'string', comment='UN Standard country or area codes for statistical'),
                Field('M49_code', 'string'),
                Field('ISO_alpha3_code', 'string'),
                format='%(Country_or_Area)s')


#db.person.import_from_csv_file(open('test.csv', 'r'))
# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------

'''extra fields for the auth fields, note that the country db table above needs to be  populated first '''


auth.settings.extra_fields['auth_user'] = [
    Field('affiliation'),
    Field('job_title'),
    Field('access_request', 'list:string',  multiple=True, widget=SQLFORM.widgets.checkboxes.widget),
    Field('country', 'reference country', required=True)]
auth.define_tables(username=False, signature=True)


db.auth_user.access_request.requires = IS_IN_SET(('VecTraits - download data','VecTraits - submit data','VecDyn - download data','VecDyn - submit data'),  multiple=True)




# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = None
# Let admin know when users sign up and request permissions, this should also create a new task, from the task you one can access the access request and grant access

# TODO this should eventually work when user confirms email rather than submits
auth.settings.register_onaccept.append(lambda form: mail.send(to='vectorbite.db.curators@gmail.com', subject='new database access request',
             message='new user email is %s'%form.vars.email))


#### TODO Users and request new rights by updatign their profiles, should send a message to admina and set a task
auth.settings.profile_onaccept.append(lambda form: mail.send(to='vectorbite.db.curators@gmail.com', subject='user has updated profile',
             message='new user email is %s'%auth.user.email))

#auth.settings.verify_email_onaccept.append(lambda form: mail.send(to='auth.user.email', subject='Email verified!',
 #            message='Your email address has been verified, you will recieve another email once your requested access rights have been granted'))



# Auth message for email verification
auth.messages.email_sent = 'A verification email has been sent, please click on the link to verify your email address. ' \
                           'Once this step is completed the VectorByte Database Admin Team will grant ' \
                           'you access to the database, this may take a little time so please be patient!' \
                           'If you cannot find the verification email in your main inbox check your junk folder.'

auth.messages.profile_updated = 'Profile updated! If you have requested new database access rights you will recieve an email once new rights have been granted'

auth.messages.email_verified = 'Your email address has been verified, you will recieve another email once your requested access rights have been granted.'

#two step authentication for admin
auth.settings.two_factor_authentication_group = "auth2step"


# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configure.get('heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)


'''SELECT OF ADD FUNCTION, USED TO TRACK COLLECTION AUTHOR(INFORMATION ON DATA PROVIDERS)
IN THE VECDYN PUBLICATION INFO TABLE AND SUBMIT VECDYN DATA'''

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



