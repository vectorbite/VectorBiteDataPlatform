





db.define_table('gadm_admin_areas',
                Field('geo_id', type = 'string'),
                Field('gid_0'),
                Field('name_0'),
                Field('gid_1'),
                Field('name_1'),
                Field('varname_1'),
                Field('hasc_1'),
                Field('engtype_1'),
                Field('gid_2'),
                Field('name_2'),
                Field('varname_2'),
                Field('hasc_2'),
                Field('engtype_2'),
                Field('gid_3'),
                Field('name_3'),
                Field('varname_3'),
                Field('hasc_3'),
                Field('engtype_3'),
                Field('gid_4'),
                Field('name_4'),
                Field('varname_4'),
                Field('engtype_4'),
                Field('gid_5'),
                Field('name_5'),
                Field('engtype_5'),
                primarykey=['geo_id'])


#db.gadm_admin_areas.drop()

#db.gadm_admin_areas.truncate()
#db.commit()
#if db(db.gadm_admin_areas.geo_id>0).count() == 0:
 #   db.gadm_admin_areas.truncate()



