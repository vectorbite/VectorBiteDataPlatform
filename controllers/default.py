# The default controller

'''Index page text  not yet implented in the correspodning view'''
@auth.requires_login()
def index():
    rows = db(db.index_page_updates).select(orderby=~db.index_page_updates.created_on)
    return locals()

'''used to indicated if specific databases havebeen set up by a specific user, 
can used to delete dor edit database entries'''
me = auth.user_id

'''the following functions create the task manager tables in default/tasks'''

'''creates a table which displays all tasks '''
@auth.requires_membership('VectorbiteAdmin')
def tasks():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = (db.task.assigned_to==me)|(db.task.created_by==me)    # replaced with query below
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=True,
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

'''creates a vecdyn submission table from from tasks, recieves data submitted through the website '''
@auth.requires_membership('VectorbiteAdmin')
def vecdyn_submissions():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = db(db.task.task_type == 'vecdyn data submission')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=True,
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

'''creates a vectraits submission table from tasks db table,  recieves data submitted through the website '''
@auth.requires_membership('VectorbiteAdmin')
def vectrait_submissions():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = db(db.task.task_type == 'vectraits data submission')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=True,
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


'''creates an issue tracker from the tasks db table, recieves messages submitted through the website '''
@auth.requires_membership('VectorbiteAdmin')
def issues():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = db(db.task.task_type == 'investigate issue/fix bug')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=True,
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


'''creates a general enquiry tracker from the tasks db table, recieves messages submitted through the website '''
@auth.requires_membership('VectorbiteAdmin')
def general_enquiries():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = db(db.task.task_type == 'enquiry')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=True,
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


'''creates a general enquiry tracker from the tasks db table, recieves messages submitted through the website '''
@auth.requires_membership('VectorbiteAdmin')
def data_set_sources():
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title,row:\
        A(title,_href=URL('edit_task',args=row.id))
    query = db(db.task.task_type == 'data set sources')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False,details=False,editable=False,csv=False,
                        deletable=True,
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


'''view/edit task, depending on task type. loads specif fields depedning on task type'''
@auth.requires_membership('VectorbiteAdmin')
def edit_task():
    task_id = request.args(0,cast=int)
    task = db.task(task_id) or error()
    add_option_2 = SelectOrAdd(form_title="Add new collection author",
                               controller="default",
                               function="add_collection_author",
                               button_text="Add New")
    # assign widget to field
    db.task.collection_author.widget = add_option.widget
    if (task.task_type == 'investigate issue/fix bug') | (task.task_type == 'enquiry'):
        db.task.task_type.writable = False
        db.task.task_type.readable = False
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
        db.task.orcid.writable = False
        db.task.orcid.readable = False
        db.task.embargo_release_date.writable = False
        db.task.embargo_release_date.readable = False
        db.task.data_rights.writable = False
        db.task.data_rights.readable = False
    else:
        pass
    form = SQLFORM(db.task,task,
                   showid=False,
                   deletable=True).process() ### change true for (task.created_by==me) so only users who created a task can delete it
    if form.accepted:
        redirect(URL('tasks'))
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.js'))
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.theme.css'))
    return locals()


'''the following functions are pass various tasks from the website to the task manager'''

'''function set up to Submit vecdyn  data through the website'''
@auth.requires_membership('VectorbiteAdmin')
def submit_vecdyn_data():
    db.task.task_type.default = 'vecdyn data submission'
    db.task.task_type.readable = False
    db.task.task_type.writable = False
    db.task.status.readable = False
    db.task.status.writable = False
    db.task.assigned_to.writable = False
    db.task.assigned_to.readable = False
    db.task.deadline.writable = False
    db.task.deadline.readable = False
    db.task.file.requires=IS_UPLOAD_FILENAME(extension='csv')
    add_option_2 = SelectOrAdd(form_title="Add new collection author",
                             controller="default",
                             function="add_collection_author",
                             button_text="Add New")
    # assign widget to field
    db.task.collection_author.widget = add_option.widget
    form = SQLFORM(db.task, labels={'task_type':'Data set category'}).process()
    if form.accepted:
        redirect(URL('index'))
    else:
        response.flash = 'please fill out the form in full and attach a csv file'
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.js'))
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.theme.css'))
    return locals()


'''add or set up a collection authro to add to the submit vecdyn data function'''
def add_collection_author():
    #this is the controller function that will appear in our dialog
    form = SQLFORM(db.collection_author)
    if form.accepts(request):
        #Successfully added new item
        #do whatever else you may want
        #Then let the user know adding via our widget worked
        response.flash = T("Added")
        target = request.args[0]
        #close the widget's dialog box
        response.js = 'jQuery( "#%s_dialog-form" ).dialog( "close" ); ' %(target)
        #update the options they can select their new category in the main form
        response.js += """jQuery("#%s").append("<option value='%s'>%s</option>");""" \
                % (target, form.vars.id, form.vars.name)
        #and select the one they just added
        response.js += """jQuery("#%s").val("%s");""" % (target, form.vars.id)
        #finally, return a blank form incase for some reason they wanted to add another option
        return form
    elif form.errors:
        # silly user, just send back the form and it'll still be in our dialog box complete with error messages
        return form
    else:
        #hasn't been submitted yet, just give them the fresh blank form
        return form


'''function set up to submit vectrait  data through the website'''
@auth.requires_login()
def submit_vectrait_data():
    db.task.task_type.default = 'vectraits data submission'
    db.task.task_type.readable = False
    db.task.task_type.writable = False
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

'''this function is set up to create a list of potential data sources through the task manager  '''
@auth.requires_login()
def new_data_source():
    db.task.task_type.default = 'data set sources'
    db.task.task_type.writable = False
    db.task.task_type.readable = False
    db.task.collection_author.writable = False
    db.task.collection_author.readable = False
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
    db.task.data_rights.writable = False
    db.task.data_rights.readable = False
    db.task.orcid.writable = False
    db.task.orcid.readable = False
    db.task.file.writable = False
    db.task.file.readable = False
    db.task.embargo_release_date.writable = False
    db.task.embargo_release_date.readable = False
    form = SQLFORM(db.task, labels={'task_type':'Data set category'}).process()
    if form.accepted:
        session.flash = 'Thanks, source added'
        redirect(URL('default', 'data_set_sources'))
     #   response.flash = 'please fill out the form in full and attach a csv file'
    return locals()

'''function allows users to submit messages via task manager '''
@auth.requires_login()
def contact_us():
    db.task.task_type.default = 'enquiry'
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
    db.task.orcid.writable = False
    db.task.orcid.readable = False
    db.task.embargo_release_date.writable = False
    db.task.embargo_release_date.readable = False
    db.task.data_rights.writable = False
    db.task.data_rights.readable = False
    form = SQLFORM(db.task, comments=False).process()
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


'''function allows users to report problems through the website  via task manager '''

@auth.requires_login()
def report_problem():
    db.task.task_type.default = 'investigate issue/fix bug'
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
    db.task.orcid.writable = False
    db.task.orcid.readable = False
    db.task.embargo_release_date.writable = False
    db.task.embargo_release_date.readable = False
    db.task.data_rights.writable = False
    db.task.data_rights.readable = False
    form = SQLFORM(db.task,  comments=False).process()
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

'''additional controls for the management pages'''

'''function to add user to admin membership'''
@auth.requires_membership('VectorbiteAdmin')
def group_membership():
    db.auth_membership.group_id.default = 2
    #db.auth_membership.group_id.readable = True
    db.auth_membership.group_id.writable = False
    #form = SQLFORM(db.auth_membership, showid=False, comments=False)
    form = SQLFORM.grid(db.auth_membership.group_id == 2, searchable=False, deletable=True, \
                        editable=False, details=False, create=True, csv=False)
    #if form.process().accepted:
     #   session.flash = 'Thanks you have successfully submit your changes'
    return locals()

'''function to manage index page messsages, not currently implemented, sould eveutally use Markmin'''
#@auth.requires_membership('VectorbiteManagers')
def manage_index_page_updates():
    grid = SQLFORM.grid(db.index_page_updates,  searchable=False, deletable=True,\
                        editable=True, details=False, create=True,csv=False)
    return dict(grid=grid)



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
