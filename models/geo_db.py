

db.define_table('gaul_admin_layers',
                Field('ADM_CODE'),
                Field('ADM0_NAME'),
                Field('ADM1_NAME'),
                Field('ADM2_NAME'),
                Field('centroid_latitude', 'double'),
                Field('centroid_longitude', 'double'),
                #lazy_tables = True,
                primarykey=['ADM_CODE'],
                format='%(ADM2_NAME)s')
#if db(db.gaul_admin_layers.ADM_CODE>0).count() == 0:
 #   db.gaul_admin_layers.truncate()




