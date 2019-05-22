# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index')),
]


if request.controller == 'vectraits':
    # VT-specific navbar
    response.menu.append(('VecTraits', False, URL('vectraits', 'index')))
    if auth.is_logged_in():
        response.menu.append(
            (T('Database'), False, None, [
                ('Submit', False, URL('vectraits', 'index')),   # TODO: change to submit link
                ('Explore', False, URL('vectraits', 'view_vectraits')),
                ('Validate', False, URL('vectraits', 'validate_vectraits')),
                # ('Download Template', False, URL('vectraits', 'vectraits_template')), # TODO: Uncomment when live
            ])
        )
    response.menu.append(('About VecTraits', False, URL('vectraits', 'about')))
elif request.controller in ('vecdyn', 'vecdyn_data_uploader', 'vecdyn_query_1', 'vecdyn_query_2'):
    # VD-specific navbar
    response.menu.append(('VecDyn', False, URL('vecdyn', 'index')))
    if auth.is_logged_in():
        response.menu.append(
            (T('Database'), False, None, [
                ('Submit', False, URL('default', 'submit_vecdyn_data')),  # TODO: move to vecdyn controller
                ('Explore', False, URL('vecdyn_query_1', 'vecdyn_taxon_location_query')),
            ])
        )
    response.menu.append(('About VecDyn', False, URL('vecdyn', 'about')))
else:
    # Default/all else navbar
    response.menu.extend([
        (T('Databases'), False, None, [
            ('VecDyn', False, URL('vecdyn', 'index')),
            ('VecTraits', False, URL('vectraits', 'index')),
        ]),
        (T('About Us'), False, URL('default', 'about_us')),
        (T('Contact Us'), False, None, [
            ('Report problem', False, URL('default', 'report_problem')),
            ('General enquiries', False, URL('default', 'contact_us'))]),
    ])


if auth.has_membership('VectorbiteAdmin'):
    # Admin navbar
    response.menu.append((T('Admin'), False, None, [
        ('Manage VecDyn Datasets', False, URL('vecdyn', 'dataset_registrations')),
        ('Manage VecTraits Datasets', False, URL('vectraits', 'index')),    # TODO: Change to management interface when created
        ('Task Manager', False, URL('default', 'tasks')),
        ('Group Membership', False, URL('default', 'group_membership'))]))

# TODO: Work out whether the below is still needed
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
