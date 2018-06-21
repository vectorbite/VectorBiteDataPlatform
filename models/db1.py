# -*- coding: utf-8 -*-
#db2 contains admin, community databases and task manager

####upload db - Manuals, data collection sheets etc.

db.define_table('database_docs',
                Field('title', requires=IS_NOT_EMPTY()),
                Field('file', 'upload', required=True),
                       auth.signature)


import datetime
week = datetime.timedelta(days=7)

db.define_table('data_source_tracker',
                Field('title', requires=IS_NOT_EMPTY()),
                Field('provider', requires=IS_NOT_EMPTY()),
                Field('species',  requires=IS_NOT_EMPTY()),
                Field('description','text'),
                Field('Web', requires=IS_URL))


# assigns a status to a task -

#STATUSES = ('assigned','accepted','rejected','reassigned','completed')

TASK_TYPE = ('VecDyn data submission', 'VecTraits data submission', 'Investigate issue/fix bug', 'Enquiry', 'Other')

db.define_table('task',
                Field('title', requires=IS_NOT_EMPTY(), comment='*'),
                Field('task_type', requires=IS_IN_SET(TASK_TYPE), comment='*Select data submission type i.e. VecDyn or VecTraits'),
                Field('collection_author', comment='*Name of collection author'),
                Field('digital_object_identifier', type='string', comment='DOI'),
                Field('publication_date', type='date', required=False),
                Field('description', type='text', required=True, comment='*Brief description of data set'),
                Field('contact_name', type='string', required=True, comment='*'),
                Field('email', requires=IS_EMAIL(), comment='*'),
                Field('file', 'upload', required=False, comment='*'),
                # Field('assigned_to','reference auth_user'), #### needs to be set to something like Field('assigned_to', requires=IS_IN_DB(db.auth_membership.group_id==3))),
                # Field('status',requires=IS_IN_SET(STATUSES)),
                # default=STATUSES[0]),
                # Field('deadline','date',default=request.now+week),
                auth.signature)





#db.define_table('task',
 #               Field('title', requires=IS_NOT_EMPTY()),
  #              Field('task_type', requires=IS_IN_SET(TASK_TYPE)),
   #             Field('collection_authority', comment='Name of collection authority'),
    #            Field('digital_object_identifier', type='string', comment='DOI'),
     #           Field('publication_date', type='date'),
      #          Field('description', type='text', required=True, comment='Brief description of data series'),
       #         Field('contact_name', type='string'),
        #        Field('email', requires=IS_EMAIL()),
         #       Field('ORCID', type='string',
          #            comment='A digital identifier which provides researchers with a unique ID, see www.orcid.org'),
           #     Field('keywords', type='string',
             #         comment='Keywords for web searches, seperate each keyword with a comma'),
           #     Field('file', 'upload', required=False),
                # Field('assigned_to','reference auth_user'), #### needs to be set to something like Field('assigned_to', requires=IS_IN_DB(db.auth_membership.group_id==3))),
                # Field('status',requires=IS_IN_SET(STATUSES)),
                # default=STATUSES[0]),
                # Field('deadline','date',default=request.now+week),
            #    auth.signature)

db.task.file.requires=IS_UPLOAD_FILENAME(extension='csv')
#else db.task.file.requires=IS_NULL

#auth.enable_record_versioning(db)

#db.task.created_on.represent = lambda v,row: prettydate(v)
#db.task.deadline.represent = lambda v,row: SPAN(prettydate(v),_class='overdue' if v and v<datetime.date.today() else None)


def fullname(user_id):
    if user_id is None:
        return "Unknown"
    return "%(first_name)s %(last_name)s (id:%(id)s)" % db.auth_user(user_id)

#def show_status(status,row=None):
#    return SPAN(status,_class=status)

#db.task.status.represent = show_status


#def send_email_realtime(to, subject, message, sender):
#    if not isinstance(to,list): to = [to]
#    # if auth.user: to = [email for email in to if not to==auth.user.email]
#    mail.settings.sender = sender
#    return mail.send(to=to, subject=subject, message=message or '(no message)')


#def send_email(to, subject, message, sender):
#    if EMAIL_POLICY == 'realtime':
#        return send_email_realtime(to, subject, message, sender)
#    else:
#        return send_email_deferred(to, subject, message, sender)




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

db.define_table('feedback_post',
                Field('title', type='string', requires=IS_NOT_EMPTY()),
                Field('file', 'upload', required=False),
                Field('body', type='text', requires=IS_NOT_EMPTY()),
                auth.signature)

db.define_table('post_comment',
                Field('feedback_post','reference feedback_post'),
                Field('file', 'upload', required=False),
                Field('body', 'text', requires=IS_NOT_EMPTY()),
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
