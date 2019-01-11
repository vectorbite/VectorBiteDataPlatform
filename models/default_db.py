# -*- coding: utf-8 -*-

import datetime

from gluon.tools import prettydate

week = datetime.timedelta(days=7)

''' Text updates for index page not currently implemented, however, we can use a database table + SQLform to control updates rather the 
editing html directly from a view'''
db.define_table('index_page_updates',
                Field('title', type='string', requires=IS_NOT_EMPTY()),
                Field('file', 'upload', required=False),
                Field('body', type='text', requires=IS_NOT_EMPTY()),
                auth.signature)

'''database table for collection author, this is used as a lookup in the submit vecdyn data task table and 
the the vecdyn publication info table, both tables and functions use the SelectOrAdd function so user can add a collection 
author when submitting or setting up a new vecdy dataset'''

db.define_table('collection_author',
    Field('name', 'string', notnull=True, unique=True),
    Field('description', 'text'),
                format='%(name)s')

# assigns a status to a task -
STATUSES = ('assigned','accepted','rejected','reassigned','completed')

#assign a task type to a task
TASK_TYPE = ('vecdyn data submission', 'vectraits data submission', 'investigate issue/fix bug', 'enquiry', 'data set sources')

DATARIGHTS = ('open', 'embargo')

'''the following db table 'task' is set up to deal with data submissions, messages via the website, and also to 
to keep track of potential data sets we can incorporate into the dbs. '''

db.define_table('task',
                Field('title', requires=IS_NOT_EMPTY(), comment='* Short title identifying the data collection'),
                Field('task_type', requires=IS_IN_SET(TASK_TYPE), comment='*Select data submission type i.e. VecDyn or VecTraits'),
                Field('collection_author', db.collection_author,
                      requires=IS_IN_DB(db, 'collection_author.id', 'collection_author.name')),
                Field('digital_object_identifier', type='string', comment='Digital Object Identifier for the dataset'),
                Field('publication_doi', type='string', comment = 'If linked to a publication, enter the Digital Object Identifier of the publication'),
                Field('url', requires=IS_EMPTY_OR(IS_URL()), comment = 'Web link to dataset or collection author website'),
                Field('description', type='text', required=True, comment='* Brief description of data set'),
                Field('contact_name', type='string', required=True, comment='* Lead author or best person to contact with any enquiries about the dataset'),
                Field('contact_affiliation', type='string', comment = 'Name of main organisation the contact is affiliated with'),
                Field('orcid', type='string', comment = 'Enter for name of main contact, ORCID is a digital identifier which provides researchers with a unique ID, see www.orcid.org'),
                Field('email', requires=IS_EMAIL(), comment='* Email of the main/best contact'),
                Field('dataset_license', type='string', comment = 'e.g. Creative Commons license CC0 “No Rights Reserved”'),
                Field('data_rights', requires=IS_IN_SET(DATARIGHTS), default=DATARIGHTS[0], comment = 'Indicate if the dataset is open at the date of submission or if under embargo'),
                Field('embargo_release_date', type ='date', requires=IS_EMPTY_OR(IS_DATE()), comment = 'If dataset is under embargo for a period of time please add its release date'),
                Field('file', 'upload', required=False, comment='* File has to be in .csv format'),
                Field('assigned_to', 'reference auth_user'),
                Field('status',requires=IS_IN_SET(STATUSES), default=STATUSES[0]),
                Field('deadline', 'datetime', default=request.now + week * 4),
                auth.signature)

db.task.file.requires=IS_UPLOAD_FILENAME(extension='csv')

'''this query selects user ids from a members of VectorbiteAdmin'''
query = db((db.auth_user.id==db.auth_membership.user_id) & (db.auth_group.id==db.auth_membership.group_id) & (db.auth_group.role == 'VectorbiteAdmin'))
db.task.assigned_to.requires = IS_IN_DB(query, 'auth_user.id', '%(first_name)s' ' %(last_name)s')

db.task.created_on.represent = lambda v,row: prettydate(v)
db.task.deadline.represent = lambda v,row: SPAN(prettydate(v),_class='overdue' if v and v < datetime.datetime.today() else None)

def fullname(user_id):
    if user_id is None:
        return "Unknown"
    return "%(first_name)s %(last_name)s (id:%(id)s)" % db.auth_user(user_id)

def show_status(status,row=None):
    return SPAN(status,_class=status)

db.task.status.represent = show_status

'''function to send email, used in task manager, not currently implemented'''
def send_email(to,subject,message,sender):
    if not isinstance(to,list): to = [to]
    mail.settings.sender = sender
    mail.send(to=to, subject=subject, message=message or '(no message)')


'''Assigns the select or add widget to db.task.collection_author table'''

add_option_2 = SelectOrAdd(form_title=T("Add a new something"),
                                              controller="default",
                                              function="add_collection_author",
                                              button_text=T("Add New"),
                                              dialog_width=600)

db.task.collection_author.widget = add_option_2.widget


