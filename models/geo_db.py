






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



# db.define_table('gadm_admin_areas',
#                 Field('geo_id', type = 'string'),
#                 Field('gid_0'),
#                 Field('name_0'),
#                 Field('gid_1'),
#                 Field('name_1'),
#                 Field('varname_1'),
#                 Field('hasc_1'),
#                 Field('engtype_1'),
#                 Field('gid_2'),
#                 Field('name_2'),
#                 Field('varname_2'),
#                 Field('hasc_2'),
#                 Field('engtype_2'),
#                 Field('gid_3'),
#                 Field('name_3'),
#                 Field('varname_3'),
#                 Field('hasc_3'),
#                 Field('engtype_3'),
#                 Field('gid_4'),
#                 Field('name_4'),
#                 Field('varname_4'),
#                 Field('engtype_4'),
#                 Field('gid_5'),
#                 Field('name_5'),
#                 Field('engtype_5'),
#                 primarykey = ['geo_id'])


#db.gadm_admin_areas.drop()

#db.gadm_admin_areas.truncate()
#db.commit()
# if db(db.gadm_admin_areas.geo_id>0).count() == 0:
#     db.gadm_admin_areas.truncate()