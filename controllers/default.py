

def about_us():
    return locals()

#def error(message="not authorized"):
#    session.flash = message
#    redirect(URL('tasks'))

##create a view all tasks too, and a see my tasks/assigned to me tasks

me = auth.user_id

#@auth.requires_membership('VectorbiteManagers')
def tasks():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = (db.task.assigned_to==me)|(db.task.created_by==me)    # replaced with query below
    #query = (db.task)
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=lambda row: (row.created_by==me),maxtextlength=200,
                        fields=[db.task.title,
                                db.task.task_type,
                                db.task.description,
                                db.task.email,
                                db.task.file,
                                db.task.created_on,
                                db.task.deadline,
                                db.task.created_by,
                                db.task.status,
                                db.task.assigned_to])
    return locals()

def vecdyn_submissions():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = (db.task.assigned_to==me)|(db.task.created_by==me) & (db.task.task_type == 'VecDyn data submission')   # replaced with query below
    #query = (db.task)
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=lambda row: (row.created_by==me),maxtextlength=200,
                        fields=[db.task.title,
                                db.task.task_type,
                                db.task.description,
                                db.task.email,
                                db.task.file,
                                db.task.created_on,
                                db.task.deadline,
                                db.task.created_by,
                                db.task.status,
                                db.task.assigned_to])
    return locals()

def vectrait_submissions():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = (db.task.assigned_to==me)|(db.task.created_by==me) & (db.task.task_type == 'VecTraits data submission')   # replaced with query below
    #query = (db.task)
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=lambda row: (row.created_by==me),maxtextlength=200,
                        fields=[db.task.title,
                                db.task.task_type,
                                db.task.description,
                                db.task.email,
                                db.task.file,
                                db.task.created_on,
                                db.task.deadline,
                                db.task.created_by,
                                db.task.status,
                                db.task.assigned_to])
    return locals()

def issues():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = (db.task.assigned_to==me)|(db.task.created_by==me) & (db.task.task_type == 'Investigate issue/fix bug')   # replaced with query below
    #query = (db.task)
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=lambda row: (row.created_by==me),maxtextlength=200,
                        fields=[db.task.title,
                                db.task.task_type,
                                db.task.description,
                                db.task.email,
                                db.task.file,
                                db.task.created_on,
                                db.task.deadline,
                                db.task.created_by,
                                db.task.status,
                                db.task.assigned_to])
    return locals()

def general_enquiries():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = (db.task.assigned_to==me)|(db.task.created_by==me) & (db.task.task_type == 'Enquiry')   # replaced with query below
    #query = (db.task)
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=lambda row: (row.created_by==me),maxtextlength=200,
                        fields=[db.task.title,
                                db.task.task_type,
                                db.task.description,
                                db.task.email,
                                db.task.file,
                                db.task.created_on,
                                db.task.deadline,
                                db.task.created_by,
                                db.task.status,
                                db.task.assigned_to])
    return locals()

def data_set_sources():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = (db.task.assigned_to==me)|(db.task.created_by==me) & (db.task.task_type == 'Data Set Sources')   # replaced with query below
    #query = (db.task)
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=lambda row: (row.created_by==me),maxtextlength=200,
                        fields=[db.task.title,
                                db.task.task_type,
                                db.task.description,
                                db.task.email,
                                db.task.file,
                                db.task.created_on,
                                db.task.deadline,
                                db.task.created_by,
                                db.task.status,
                                db.task.assigned_to])
    return locals()





#@auth.requires_membership('VectorbiteAdmin')
def create_task():
    #db.task.status.readable = False
    #db.task.status.writable = False
    form = SQLFORM(db.task).process()
    if form.accepted:
        #send_email(to=db.auth_user(form.vars.assigned_to).email,
        #           sender=auth.user.email,
        #           subject="New Task Assigned: %s" % form.vars.title,
         #          message=form.vars.description)
        redirect(URL('tasks'))
    return locals()

#@auth.requires_membership('VectorbiteManagers')
def view_task():
    task_form = ()
    task_id = request.args(0,cast=int)
    task = db.task(task_id) or error()
    if not task.created_by==me and not task.assigned_to==me: error()
    if (task.task_type == 'VecDyn data submission') | (task.task_type == 'VecTraits data submission'):
        db.task.id.readable = False
        db.task.file.readable = False
        db.task.file.writable = False
        task_form = SQLFORM(db.task, task_id)
    elif (task.task_type == 'Investigate issue/fix bug') | (task.task_type == 'Enquiry'):
        db.task.id.readable = False
        db.task.collection_author.readable = False
        db.task.file.readable = False
        db.task.file.writable = False
        db.task.title.readable = False
        db.task.title.readable = False
        db.task.title.readable = False
        db.task.title.readable = False
        task_form = SQLFORM(db.task, task_id)
    elif (task.task_type == 'VecDyn Data Set Source') | (task.task_type == 'VecTraits Data Set Source'):
        db.task.id.readable = False
        db.task.collection_author.readable = False
        db.task.file.readable = False
        db.task.file.writable = False
        db.task.title.readable = False
        db.task.title.readable = False
        db.task.title.readable = False
        db.task.title.readable = False
        task_form = SQLFORM(db.task, task_id)
    db.post.task.default = task.id
    db.post.task.writable = False
    db.post.task.readable = False
    task_form = SQLFORM(db.task, task_id)
    form = SQLFORM(db.post).process()
    if form.accepted:
        user_id = task.created_by if task.assigned_to==me else task.assigned_to
        #send_email(to=db.auth_user(user_id).email,
         #          sender=auth.user.email,
          ##         subject="New Commend About: %s" % task.title,
            #       message=form.vars.body)
    posts = db(db.post).select(orderby=db.post.created_by)
    return locals()

#@auth.requires_membership('VectorbiteManagers')
def edit_task():
    publication_info_id = request.get_vars.publication_info_id
    data_set_type = db.task.task_type
    db.task.file.readable = False
    db.task.file.writable = False
    task_id = request.args(0,cast=int)
    task = db.task(task_id) or error()
    #if not task.created_by==me and not task.assigned_to==me: error()
    #if task.created_by==me:
    #    task.assigned_to.writable = True
    #else:
    #    task.assigned_to.writable = False
    #    task.status.requires=IS_IN_SET(('accepted','rejected','completed'))
    form = SQLFORM(db.task,task,
                   showid=False,
                   deletable=True).process() ### change true for (task.created_by==me) so only users who created a task can delete it
    if form.accepted:
    #    email_to = db.auth_user(
    #        form.vars.assigned_to if task.created_by==me else task.created_b
     #       ).email
     #   send_email(to=email_to,sender=auth.user.email,
     #              subject="Task Changed (%(status)s): %(title)s" % form.vars,
     #              message=form.vars.description)
        redirect(URL('tasks'))
    return locals()


def submit_data():
    db.task.task_type.requires = IS_IN_SET(('VecDyn data submission', 'VecTraits data submission'))
    db.task.status.readable = False
    db.task.status.writable = False
    db.task.assigned_to.writable = False
    db.task.assigned_to.readable = False
    db.task.deadline.writable = False
    db.task.deadline.readable = False
    db.task.file.requires=IS_UPLOAD_FILENAME(extension='csv')
    form = SQLFORM(db.task, labels={'task_type':'Data set category'}).process()
    if form.accepted:
        session.flash = 'Thanks, your data set has been submitted for review, we will get back to you soon!'
        #send_email(to=db.auth_user(form.vars.assigned_to).email,
        #           sender=auth.user.email,
        #           subject="New data set submitted: %s" % form.vars.title,
        #           message=form.vars.description)
        redirect(URL('index'))
    #else:
     #   response.flash = 'please fill out the form in full and attach a csv file'
    return locals()



def new_data_source():
    db.task.task_type.default = 'Data Set Sources'
    db.task.task_type.writable = False
    db.task.task_type.readable = False
    db.task.assigned_to.writable = False
    db.task.assigned_to.readable = False
    db.task.deadline.writable = False
    db.task.deadline.readable = False
    db.task.status.readable = False
    db.task.status.writable = False
    db.task.contact_affiliation.writable = False
    db.task.contact_affiliation.readable = False
    db.task.dataset_license.writable = False
    db.task.dataset_license.readable = False
    db.task.file.writable = False
    db.task.file.readable = False
    form = SQLFORM(db.task, labels={'task_type':'Data set category'}).process()
    if form.accepted:
        session.flash = 'Thanks, source added'
        redirect(URL('default', 'data_set_sources'))
     #   response.flash = 'please fill out the form in full and attach a csv file'
    return locals()



def contact_us():
    db.task.task_type.default = 'Enquiry'
    db.task.task_type.writable = False
    db.task.task_type.readable = False
    db.task.status.readable = False
    db.task.status.writable = False
    db.task.assigned_to.writable = False
    db.task.assigned_to.readable = False
    db.task.deadline.writable = False
    db.task.deadline.readable = False
    db.task.collection_author.writable = False
    db.task.collection_author.readable = False
    db.task.digital_object_identifier.writable = False
    db.task.digital_object_identifier.readable = False
    db.task.publication_doi.writable = False
    db.task.publication_doi.readable = False
    db.task.contact_affiliation.writable = False
    db.task.contact_affiliation.readable = False
    db.task.dataset_license.writable = False
    db.task.dataset_license.readable = False
    db.task.url.writable = False
    db.task.url.readable = False
    db.task.file.writable = False
    db.task.file.readable = False
    form = SQLFORM(db.task).process()
    if form.accepted:
        session.flash = 'Thanks for your comment, we will get back to you soon!'
        #send_email(to=db.auth_user(form.vars.assigned_to).email,
        #           sender=auth.user.email,
        #           subject="New data set submitted: %s" % form.vars.title,
        #           message=form.vars.description)
        redirect(URL('index'))
    else:
        session.flash = 'please complete the form'
    return locals()

'''def contact_us():
    form = SQLFORM(db.contact)
    if form.process().accepted:
        mail.send(to='vectorbiteonlineplatform@gmail.com',
                  subject='contact request from %(your_name)s %(email)s'  % form.vars,
                  message = form.vars.message)
        session.flash = 'Thank you, your message was sent'
        redirect(URL('index'))
    return dict(form=form)'''



def report_problem():
    db.task.task_type.default = 'Investigate issue/fix bug'
    db.task.task_type.writable = False
    db.task.task_type.readable = False
    db.task.status.readable = False
    db.task.status.writable = False
    db.task.assigned_to.writable = False
    db.task.assigned_to.readable = False
    db.task.deadline.writable = False
    db.task.deadline.readable = False
    db.task.collection_author.writable = False
    db.task.collection_author.readable = False
    db.task.digital_object_identifier.writable = False
    db.task.digital_object_identifier.readable = False
    db.task.publication_doi.writable = False
    db.task.publication_doi.readable = False
    db.task.contact_affiliation.writable = False
    db.task.contact_affiliation.readable = False
    db.task.dataset_license.writable = False
    db.task.dataset_license.readable = False
    db.task.url.writable = False
    db.task.url.readable = False
    db.task.file.writable = False
    db.task.file.readable = False
    form = SQLFORM(db.task).process()
    if form.accepted:
        session.flash = 'Thanks for your comment, we will get back to you soon!'
        #send_email(to=db.auth_user(form.vars.assigned_to).email,
        #           sender=auth.user.email,
        #           subject="New data set submitted: %s" % form.vars.title,
        #           message=form.vars.description)
        redirect(URL('index'))
    else:
        session.flash = 'please complete the form'
    return locals()

#Admin and community functions

#@auth.requires_membership('VectorbiteManagers')
def manage_index_page_updates():
    grid = SQLFORM.grid(db.index_page_updates,  searchable=False, deletable=True,\
                        editable=True, details=False, create=False,csv=False)
    return dict(grid=grid)


def index():
    #if auth.has_membership('VectorBiTE Managers'): redirect(URL('tasks'))
    rows = db(db.index_page_updates).select(orderby=~db.index_page_updates.created_on)
    return locals()


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
