# The default controller
import logging

logger = logging.getLogger("web2py.app.vbdp")
logger.setLevel(logging.DEBUG)


# Index page text not yet implemented in the corresponding view
# @auth.requires_login()
def index():
    rows = db(db.index_page_updates).select(orderby=~db.index_page_updates.created_on)
    return locals()


def about_us():
    """
    Controller for about page
    """
    return locals()

# Used to indicated if specific databases have been set up by a specific user
# (can used to delete dor edit database entries)
me = auth.user_id

# Meet the team pages, can be edited in admin section using team page updater
def team():
    db.team.active.readable = False
    query = db(db.team.active == True).select(orderby=db.team.page_position|db.team.name)
    query2 = db(db.team.active == False).select(orderby=~db.team.id)
    return locals()

@auth.requires_membership('VectorbiteAdmin')
def team_page_updater():
    grid = SQLFORM.grid(db.team,
                        create=True, details=True, editable=True, csv=False,
                        deletable=False, maxtextlength=200)
    return locals()

# Grant users privileges, found in admin section
@auth.requires_membership('VectorbiteAdmin')
def privilege_manager():
    # arrange by id and groups == None
    # TODO need to fix query in view to render result without table headings
    privileges = db(db.auth_user).select(orderby=~db.auth_user.modified_on)
    return locals()

# Admin & auth 2 step rights can only be granted through the web2py app admin
@auth.requires_membership('VectorbiteAdmin')
def edit_privileges():
    user_id = request.get_vars.user_id
    user = db(db.auth_user.id == user_id).select().first()
    db.auth_membership.user_id.default = user_id
    db.auth_membership.user_id.writable = False
    db.auth_membership.id.readable = False
    db.auth_membership.group_id.requires = requires = IS_IN_SET({'34':'VDViewer', '35':'VTViewer', '36':'VDUploader', '37':'VTUploader', '38':'VDCurator', '39':'VTCurator', '40':'ViewAll'}, zero=None)
    form = SQLFORM(db.auth_membership).process()
    privileges = (db.auth_membership.user_id == user_id)
    grid = SQLFORM.grid(privileges,
                        create=False, details=False, editable=False, csv=False,
                        deletable=True, searchable=False,maxtextlength=200)
    if form.accepted:
        session.flash = 'Thanks, rights added!'
        send_email(to=user.email,
                   sender='VectorByte Admin',
                   subject='Access Rights',
                   message='Your access rights have been modified')
        redirect(URL('default', 'edit_privileges', vars={'user_id':user_id}))
    return locals()

# Links to funding organisations

def funding():
    """
    Controller for about page
    """
    return locals()



# ----------------------------------------------------------------------------------------------------------------------
# The following functions create the task manager tables in default/tasks
# ----------------------------------------------------------------------------------------------------------------------

@auth.requires_membership('VectorbiteAdmin')
def tasks():
    """creates a table which displays all tasks"""
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title, row:\
        A(title, _href=URL('edit_task', args=row.id))
    query = (db.task.assigned_to == me) | (db.task.created_by == me)    # replaced with query below
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False, details=False, editable=False, csv=False,
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


@auth.requires_membership('VectorbiteAdmin')
def vecdyn_submissions():
    """creates a vecdyn submission table from from tasks, recieves data submitted through the website"""
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title, row:\
        A(title, _href=URL('edit_task', args=row.id))
    query = db(db.task.task_type == 'vecdyn data submission')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False, details=False, editable=False, csv=False,
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


@auth.requires_membership('VectorbiteAdmin')
def vectrait_submissions():
    """creates a vectraits submission table from tasks db table,  recieves data submitted through the website"""
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title, row:\
        A(title, _href=URL('edit_task', args=row.id))
    query = db(db.task.task_type == 'vectraits data submission')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False, details=False, editable=False, csv=False,
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


@auth.requires_membership('VectorbiteAdmin')
def issues():
    """creates an issue tracker from the tasks db table, recieves messages submitted through the website"""
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title, row:\
        A(title, _href=URL('edit_task', args=row.id))
    query = db(db.task.task_type == 'investigate issue/fix bug')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False, details=False, editable=False, csv=False,
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


@auth.requires_membership('VectorbiteAdmin')
def general_enquiries():
    """creates a general enquiry tracker from the tasks db table, recieves messages submitted through the website"""
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title, row:\
        A(title, _href=URL('edit_task', args=row.id))
    query = db(db.task.task_type == 'enquiry')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False, details=False, editable=False, csv=False,
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


@auth.requires_membership('VectorbiteAdmin')
def data_set_sources():
    """creates a general enquiry tracker from the tasks db table, receives messages submitted through the website"""
    db.task.created_on.readable = False
    db.task.created_by.readable = False
    db.task.title.represent = lambda title, row:\
        A(title, _href=URL('edit_task', args=row.id))
    query = db(db.task.task_type == 'data set sources')
    grid = SQLFORM.grid(query, orderby=~db.task.modified_on,
                        create=False, details=False, editable=False, csv=False,
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


@auth.requires_membership('VectorbiteAdmin')
def edit_task():
    """view/edit task, depending on task type. loads specif fields depending on task type"""
    task_id = request.args(0, cast=int)
    task = db.task(task_id) or error()  # TODO: Wrap in try/catch to see if this bugs out?
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
        db.task.dataset_citation.writable = False
        db.task.dataset_citation.readable = False
        db.task.publication_citation.writable = False
        db.task.publication_citation.readable = False
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
    form = SQLFORM(db.task, task,
                   showid=False,
                   deletable=True).process()
    if form.accepted:
        redirect(URL('tasks'))
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.js'))
    response.files.append(URL('static', 'jquery-ui-1.12.1/jquery-ui.theme.css'))
    return locals()


# ----------------------------------------------------------------------------------------------------------------------
# The following functions are pass various tasks from the website to the task manager
# ----------------------------------------------------------------------------------------------------------------------


@auth.requires_login()
def submit_vectrait_data():
    """function set up to submit vectrait  data through the website"""
    db.task.task_type.default = 'vectraits data submission'
    db.task.task_type.readable = False
    db.task.task_type.writable = False
    db.task.status.readable = False
    db.task.status.writable = False
    db.task.assigned_to.writable = False
    db.task.assigned_to.readable = False
    db.task.deadline.writable = False
    db.task.deadline.readable = False
    db.task.file.requires = IS_UPLOAD_FILENAME(extension='csv')
    form = SQLFORM(db.task, labels={'task_type': 'Data set category'}).process()
    if form.accepted:
        session.flash = 'Thanks, your data set has been submitted for review, we will get back to you soon!'
        # send_email(to=db.auth_user(form.vars.assigned_to).email,
        #           sender=auth.user.email,
        #           subject="New data set submitted: %s" % form.vars.title,
        #           message=form.vars.description)
        redirect(URL('index'))
    # else:
    #    response.flash = 'please fill out the form in full and attach a csv file'
    return locals()


@auth.requires_login()
def new_data_source():
    """this function is set up to create a list of potential data sources through the task manager"""
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
    form = SQLFORM(db.task, labels={'task_type': 'Data set category'}).process()
    if form.accepted:
        session.flash = 'Thanks, source added'
        logger.info("Data source submitted: task ID {} - {}".format(form.vars["id"], form.vars["title"]))
        redirect(URL('default', 'data_set_sources'))
    # response.flash = 'please fill out the form in full and attach a csv file'
    return locals()


@auth.requires_login()
def contact_us():
    """function allows users to submit messages via task manager"""
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
    db.task.dataset_citation.writable = False
    db.task.dataset_citation.readable = False
    db.task.publication_citation.writable = False
    db.task.publication_citation.readable = False
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
        logger.info("Enquiry submitted: task ID {} - {}".format(form.vars["id"], form.vars["title"]))
        # send_email(to=db.auth_user(form.vars.assigned_to).email,
        #           sender=auth.user.email,
        #           subject="New data set submitted: %s" % form.vars.title,
        #           message=form.vars.description)
        redirect(URL('index'))
    else:
        session.flash = 'please complete the form'
    return locals()


@auth.requires_login()
def report_problem():
    """function allows users to report problems through the website  via task manager"""
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
    db.task.dataset_citation.writable = False
    db.task.dataset_citation.readable = False
    db.task.publication_citation.writable = False
    db.task.publication_citation.readable = False
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

    # Here it is not critical to notify sysadmin through the log when there are form submission errors
    # However it is always good to log times when the db is written to when possible
    if form.accepted:
        session.flash = 'Thanks for your comment, we will get back to you soon!'
        logger.info("Problem submitted: task ID {} - {}".format(form.vars["id"], form.vars["title"]))
        redirect(URL('index'))
    else:
        session.flash = 'please complete the form'
    return locals()


# ----------------------------------------------------------------------------------------------------------------------
# Additional controls for the management pages
# ----------------------------------------------------------------------------------------------------------------------

@auth.requires_membership('VectorbiteAdmin')
def group_membership():
    """function to add user to admin membership"""
    db.auth_membership.group_id.default = 2
    # db.auth_membership.group_id.readable = True
    db.auth_membership.group_id.writable = False
    # form = SQLFORM(db.auth_membership, showid=False, comments=False)
    form = SQLFORM.grid(db.auth_membership.group_id == 2, searchable=False, deletable=True,
                        editable=False, details=False, create=True, csv=False)
    # if form.process().accepted:
    #    session.flash = 'Thanks you have successfully submit your changes'
    return locals()


# @auth.requires_membership('VectorbiteManagers')
def manage_index_page_updates():
    """function to manage index page messsages, not currently implemented, should eveutally use Markmin"""
    grid = SQLFORM.grid(db.index_page_updates,  searchable=False, deletable=True,
                        editable=True, details=False, create=True, csv=False)
    return dict(grid=grid)


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET':
        raise HTTP(403)
    return response.json({'status': 'success', 'email': auth.user.email})


# ---- Smart Grid (example) -----
@auth.requires_membership('admin')  # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html'  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables:  # Membership test should be "if x not in y"
        raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)


# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu()     # add the wiki to the menu
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