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
                ('Download Template', False, URL('vectraits', 'vectraits_template')),   # TODO: Uncomment when live
            ])
        )
    response.menu.append(('About VecTraits', False, URL('vectraits', 'about')))
    response.menu.append(('Documentation', False, 'https://vectorbitedataplatform.readthedocs.io/en/latest/vectraits/'))


elif request.controller == 'vecdyn':
    # VD-specific navbar
    #response.menu.append(('VecDyn', False, URL('vecdyn', 'index')))
    if auth.is_logged_in():
        response.menu.append(
            (T('Database'), False, None, [
                ('Explore vecdyn datasets', False, URL('vecdyn', 'vecdyn_taxon_location_query')),  # TODO: move to vecdyn controller
                ('Submit vecdyn data', False, URL('vecdyn', 'submit_vecdyn_data')),
            ])
        )
    response.menu.append(('Documentation', False, 'https://vectorbitedataplatform.readthedocs.io/en/latest/vecdyn/'))
else:
    # Default/all else navbar
    response.menu.extend([
        (T('Databases'), False, None, [
            ('VecDyn', False, URL('vecdyn', 'index')),
            ('VecTraits', False, URL('vectraits', 'index')),
        ]),
        (T('Documentation'), False, 'https://vectorbitedataplatform.readthedocs.io/en/latest/'),
        (T('Contact Us'), False, None, [
            ('Report problem', False, URL('default', 'report_problem')),
            ('General enquiries', False, URL('default', 'contact_us'))]),
        (T('Vectorbyte1'), False, None, [
            ('Meet the team', False, URL('default', 'team')),
            ('About', False, URL('default', 'about'))]),
    ])


if auth.has_membership('VDCurator') or auth.has_membership('VectorbiteAdmin'):
    # Admin navbar
    response.menu.append((T('Data management'), False, None, [
        ('Manage VecDyn Datasets', False, URL('vecdyn', 'dataset_registrations')),
        ('Manage VecTraits Datasets', False, URL('vectraits', 'index'))]))    # TODO: Change to management interface when created



if auth.has_membership('VectorbiteAdmin'):
    # Admin navbar 2
    response.menu.append((T('Admin'), False, None, [
        # ('Edit index page', False, URL('default', 'team')),
        # ('Edit vecdyn main page', False, URL('default', 'team')),
        ('Manage privileges', False, URL('default', 'privilege_manager')),
        ('Edit web pages', False, URL('default', 'team_page_updater')),
        ('Task Manager', False, URL('default', 'tasks'))]))
        # ('Edit Funding Pages', False, URL('default', 'funding'))]))
# ,
#         ('Group Membership', False, URL('default', 'group_membership'))
# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------
