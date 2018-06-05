# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------
if auth.is_logged_in():
    response.menu = [
        (T('Home'), False, URL('default', 'index'), []),
        ('Get Data', False, None, [
            ('VecDyn', False, URL('queries', 'vec_dyn_query'))]),
        ('Submit Data', False, None,[
            ('Submit Data Set', False, URL('default', 'submit_data'))]),
         (T('Further Info'), False, None,[
                ('Contact Us', False, URL('default', 'contact_us')),
             (T('About Us'), False, URL('default', 'about_us'))]),

]


if auth.has_membership('VectorbiteAdmin'):
    response.menu.append((T('Manage Data Sets'), False, None,[
                ('VecDyn data collections', False, URL('vecdyn', 'my_collections'))]))




if auth.has_membership('VectorbiteManagers'):
    response.menu.append((T('Managment'), False, None,[
                ('Manage Collections', False, URL('vecdyn', 'manage_collections')),
                ('Register New Data Collection', False, URL('vecdyn', 'user_collection_registration')),
                ('Task Manager', False, URL('default', 'tasks')),
                ('Manage db files & docs', False, URL('default','manage_db_documents')),
                ('Manage index page updates', False, URL('default','manage_index_page_updates'))]))


##### will add an ecological informatics working group area - i.e. links to git hub etc,  - community group


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------
