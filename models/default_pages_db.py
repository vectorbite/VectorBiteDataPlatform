# -*- coding: utf-8 -*-
#db2 contains admin, community databases and task manager


import datetime

from gluon.tools import prettydate

week = datetime.timedelta(days=7)

db.define_table('data_source_tracker',
                Field('title', requires=IS_NOT_EMPTY()),
                Field('provider', requires=IS_NOT_EMPTY()),
                Field('species',  requires=IS_NOT_EMPTY()),
                Field('description','text'),
                Field('Web', requires=IS_URL))


# assigns a status to a task -
STATUSES = ('assigned','accepted','rejected','reassigned','completed')

TASK_TYPE = ('VecDyn data submission', 'VecTraits data submission', 'Investigate issue/fix bug', 'Enquiry', 'Data Set Sources')

DATARIGHTS = ('Open', 'Embargo')

db.define_table('task',
                Field('title', requires=IS_NOT_EMPTY(), comment='*'),
                Field('task_type', requires=IS_IN_SET(TASK_TYPE), comment='*Select data submission type i.e. VecDyn or VecTraits'),
                Field('collection_author', comment='*Name of collection author'),
                Field('digital_object_identifier', type='string', comment='DOI'),
                Field('publication_doi', type='string', comment = 'Digital Object Identifier'),
                Field('url', requires=IS_EMPTY_OR(IS_URL()), comment = 'web link to dataset'),
                Field('contact_affiliation', type='string'),
                Field('description', type='text', required=True, comment='*Brief description of data set'),
                Field('contact_name', type='string', required=True, comment='*'),
                Field('orcid', type='string'),
                Field('email', requires=IS_EMAIL(), comment='*'),
                Field('dataset_license', type='string'),
                Field('data_rights', requires=IS_IN_SET(DATARIGHTS), default=DATARIGHTS[0]),
                Field('embargo_release_date', type ='date', requires=IS_EMPTY_OR(IS_DATE()), comment = 'Embargo release date'),
                Field('file', 'upload', required=False, comment='*'),
                Field('assigned_to','reference auth_user'), #### needs to be set to something like Field('assigned_to', requires=IS_IN_DB(db.auth_membership.group_id==3))),
                Field('status',requires=IS_IN_SET(STATUSES), default=STATUSES[0]),
                Field('deadline', 'datetime', default=request.now + week * 4),
                auth.signature)

db.define_table('post',
                Field('task', 'reference task'),
                Field('body', 'text'),
                auth.signature)







db.task.file.requires=IS_UPLOAD_FILENAME(extension='csv')


db.task.created_on.represent = lambda v,row: prettydate(v)
db.task.deadline.represent = lambda v,row: SPAN(prettydate(v),_class='overdue' if v and v < datetime.datetime.today() else None)


def fullname(user_id):
    if user_id is None:
        return "Unknown"
    return "%(first_name)s %(last_name)s (id:%(id)s)" % db.auth_user(user_id)

def show_status(status,row=None):
    return SPAN(status,_class=status)

db.task.status.represent = show_status

def send_email(to,subject,message,sender):
    if not isinstance(to,list): to = [to]
    mail.settings.sender = sender
    mail.send(to=to, subject=subject, message=message or '(no message)')


###Add extra tables to auth

#ORG_TYPE = ('Academic', 'Governmental', 'NGO','Private Sector')

#auth = Auth(db)
#auth.settings.extra_fields['auth_user']= [
#  Field('Organisation'),
#  Field('Organisation_type', requires=IS_IN_SET(ORG_TYPE))]
#auth.define_tables(username=True)


DOC_TYPE = ('VecDyn Documentation', 'VecTraits data submission')

db.define_table('documentation',
                Field('title', type='string', requires=IS_NOT_EMPTY()),
                Field('doc_type', requires=IS_IN_SET(DOC_TYPE)),
                Field('file', 'upload', required=False),
                Field('body', type='text', requires=IS_NOT_EMPTY()),
                auth.signature)

db.define_table('index_page_updates',
                Field('title', type='string', requires=IS_NOT_EMPTY()),
                Field('file', 'upload', required=False),
                Field('body', type='text', requires=IS_NOT_EMPTY()),
                auth.signature)


##Contact form example
db.define_table('contact',
   Field('your_name',requires=IS_NOT_EMPTY()),
   Field('email',requires=IS_EMAIL()),
   Field('message','text'))
