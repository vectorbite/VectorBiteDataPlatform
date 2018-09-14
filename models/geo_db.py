

db.define_table('country',
                Field('Country_or_Area', 'string', comment='UN Standard country or area codes for statistical'),
                Field('M49_code', 'string'),
                Field('ISO_alpha3_code', 'string'),
                format='%(Country_or_Area)s')


#if db(db.country.id>0).count() == 0:
 #   db.country.truncate()



db.define_table('gaul_admin_layers',
                Field('ADM_CODE', type = 'string'),
                Field('ADM0_NAME', 'string'),
                Field('ADM1_NAME', 'string'),
                Field('ADM2_NAME', 'string'),
                Field('centroid_latitude', 'double'),
                Field('centroid_longitude', 'double'),
                #lazy_tables = True,
                primarykey=['ADM_CODE'])
#if db(db.gaul_admin_layers.ADM_CODE>0).count() == 0:
 #   db.gaul_admin_layers.truncate()


