# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------
if auth.is_logged_in():
    response.menu = [
        (T('Home'), False, URL('default', 'index'), []),
        ('Get Data', False, None, [
            ('VecDyn', False, URL('vecdyn_queries', 'vd_grid_query'))]),
        ('Submit Data', False, None,[
            ('Submit VecDyn Dataset', False, URL('default', 'submit_data'))]),
         (T('Contact Us'), False, None,[
                ('Report problem', False, URL('default', 'report_problem')),
                ('General enquiries', False, URL('default', 'contact_us'))]),
             #(T('About Us'), False, URL('default', 'about_us'))]),

]



#if auth.has_membership('VectorbiteAdmin'):
 #   response.menu.append((T('Manage Data Sets'), False, None,[
  #              ('VecDyn data collections', False, URL('vecdyn', 'data_collections'))]))

if auth.has_membership('VectorbiteAdmin'):
    response.menu.append((T('Management'), False, None,[
                #('Messages', False, URL('default', 'messages')),
                ('Manage VecDyn data sets', False, URL('vecdyn', 'data_collections')),
                ('Task Manager', False, URL('default', 'tasks'))]))


#if auth.has_membership('VectorbiteManagers'):
 #   response.menu.append((T('Management'), False, None,[
                #('Manage Collections', False, URL('vecdyn', 'manage_collections')),
                #('Register New Data Collection', False, URL('vecdyn', 'user_dataset_registration')),
  #              ('Messages', False, URL('default', 'messages')),
   #             ('Task Manager', False, URL('default', 'tasks'))]))
                #('Manage db files & docs', False, URL('default','manage_db_documents')),
                #('Manage index page updates', False, URL('default','manage_index_page_updates'))]))


##### will add an ecological informatics working group area - i.e. links to git hub etc,  - community group


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------
