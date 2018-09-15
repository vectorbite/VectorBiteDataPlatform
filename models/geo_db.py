

db.define_table('country',
                Field('Country_or_Area', 'string', comment='UN Standard country or area codes for statistical'),
                Field('M49_code', 'string'),
                Field('ISO_alpha3_code', 'string'),
                format='%(Country_or_Area)s')


#if db(db.country.id>0).count() == 0:
 #   db.country.truncate()



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




