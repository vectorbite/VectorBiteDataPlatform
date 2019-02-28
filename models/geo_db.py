






db.define_table('gaul_admin_layers',
                Field('geo_id', type = 'id'),
                Field('adm0_name'),
                Field('adm1_name'),
                Field('adm2_name', default=None),
                Field('centroid_latitude', 'double'),
                Field('centroid_longitude', 'double'),
                #lazy_tables = True,
                format='%(adm0_name)s')
#if db(db.gaul_admin_layers.ADM_CODE>0).count() == 0:
 #   db.gaul_admin_layers.truncate()


#db.gaul_admin_layers.drop()



