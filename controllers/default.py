def test():
    return locals()

def about_us():
    return locals()

#def error(message="not authorized"):
#    session.flash = message
#    redirect(URL('tasks'))

##create a view all tasks too, and a see my tasks/assigned to me tasks

me = auth.user_id

#@auth.requires_membership('VectorbiteManagers')
def tasks():
    db.task.created_on.readable = True
    db.task.created_by.readable = True
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('view_task',args=row.id))
    #query = (db.task.assigned_to==me)|(db.task.created_by==me)    # replaced with query below
    query = (db.task)
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,
                        deletable=lambda row: (row.created_by==me),
                        fields=[
            #db.task.status,
            db.task.title,
            db.task.task_type,
            db.task.created_on,
            #db.task.deadline,
            db.task.created_by,
            #db.task.assigned_to,
            ])
    return locals()


#@auth.requires_membership('VectorbiteManagers')
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
    task_id = request.args(0,cast=int)
    task = db.task(task_id) or error()
    #if not task.created_by==me and not task.assigned_to==me: error()
    # form, posts = make_comments(callback)
    return locals()

#@auth.requires_membership('VectorbiteManagers')
def edit_task():
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
        redirect(URL('view_task',args=task.id))
    return locals()


def submit_data():
    #db.task.status.readable = False
    #db.task.status.writable = False
    #db.task.assigned_to.writable = False
    #db.task.assigned_to.readable = False
    #db.task.deadline.writable = False
    #db.task.deadline.readable = False
    db.task.task_type.requires=IS_IN_SET(('VecDyn data submission', 'VecTraits data submission'))
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

#def general_enquiry():
#    db.task.status.readable = False
#    db.task.status.writable = False
#    db.task.assigned_to.writable = False
#    db.task.assigned_to.readable = False
#    db.task.deadline.writable = False
#    db.task.deadline.readable = False
#    db.task.task_type.requires=IS_IN_SET(['Enquiry'])
#    form = SQLFORM(db.task).process()
#    if form.accepted:
#        session.flash = 'Thanks for your comment, we will get back to you soon!'
        #send_email(to=db.auth_user(form.vars.assigned_to).email,
        #           sender=auth.user.email,
        #           subject="New data set submitted: %s" % form.vars.title,
        #           message=form.vars.description)
#        redirect(URL('index'))
#    else:
#        session.flash = 'please complete the form'
#    return locals()

def report_problem():
    #db.task.status.readable = False
    #db.task.status.writable = False
    #db.task.assigned_to.writable = False
    #db.task.assigned_to.readable = False
    #db.task.deadline.writable = False
    #db.task.deadline.readable = False
    db.task.task_type.requires=IS_IN_SET(['Investigate issue/fix bug'])
    db.task.task_type.writable = False
    db.task.task_type.readable = False
    form = SQLFORM(db.task).process()
    if form.accepted:
        session.flash = 'Thanks, we will get back to you as soon as e can!'
    #    send_email(to=db.auth_user(form.vars.assigned_to).email,
     #              sender=auth.user.email,
      #             subject="issue/fix bug: %s" % form.vars.title,
       #            message=form.vars.description)
        redirect(URL('index'))
    #else:
     #   response.flash = 'please fill out the form '
    return locals()

## documentation page - could be a static page or connect to a database

def documentation():
    rows = db(db.database_docs).select(orderby=db.database_docs.id)
    return locals()

def data_download_help():
    rows = db(db.database_docs).select(orderby=db.database_docs.id)
    return locals()

def datasources():
    form = SQLFORM(db.data_source_tracker)
    #if form.accepted:
     #   session.flash = 'Thanks, your comment has been submitted'
      #  redirect(URL('index'))
    return locals()

#Admin and community functions

#@auth.requires_membership('VectorbiteManagers')
def manage_index_page_updates():
    grid = SQLFORM.grid(db.index_page_updates,  searchable=False, deletable=True,\
                        editable=True, details=False, create=False,csv=False)
    return dict(grid=grid)

#@auth.requires_membership('VectorbiteManagers')
def manage_comments():
    grid = SQLFORM.grid(db.feedback_post,searchable=False, deletable=True,\
                        editable=True, details=False, create=False,csv=False)
    return locals()


#@auth.requires_membership('VectorbiteManagers')
def manage_db_documents():
    grid = SQLFORM.grid(db.database_docs,searchable=False, deletable=True,\
                        editable=True, details=False, create=False,csv=False)
    return locals()

def vec_dyn_query():
    form = SQLFORM.grid(db.study_data)
    return locals()



#@auth.requires_login()
def leave_comment():
    form = SQLFORM(db.feedback_post).process()
    if form.accepted:
        session.flash = 'Thanks, your comment has been submitted'
        redirect(URL('view_all_comments'))
    return locals()

#@auth.requires_login()
def view_comment():
    post = db.feedback_post(request.args(0,cast=int))
    db.post_comment.feedback_post.default = post.id
    db.post_comment.feedback_post.readable=False
    db.post_comment.feedback_post.writable=False
    form = SQLFORM(db.post_comment).process()
    comments = db(db.post_comment.feedback_post==post.id).select()
    return locals()

#@auth.requires_login()
def view_all_comments():
    rows = db(db.feedback_post).select(orderby=db.feedback_post.created_on)
    return locals()


def contact_us():
    form = SQLFORM(db.contact)
    if form.process().accepted:
        mail.send(to='vectorbiteonlineplatform@gmail.com',
                  subject='contact request from %(your_name)s %(email)s'  % form.vars,
                  message = form.vars.message)
        session.flash = 'Thank you, your message was sent'
        redirect(URL('index'))
    return dict(form=form)


def messages():
    form = SQLFORM.grid(db.contact)
    return locals()



##VecDyn functions


#def vec_dyn_query_by_id(): add a function that searches or links datasets

def index():
    if  auth.has_membership('VectorBiTE Managers'): redirect(URL('tasks'))
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
