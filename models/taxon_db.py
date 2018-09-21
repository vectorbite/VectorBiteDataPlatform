


####still need to restructure data set so only one specific line i.e. order, kingdom can be selected. Also need to included specificEpithet & infraspecificEpithet in search


db.define_table('taxon',
                Field('taxonID'),
                Field('tax_scientificName'),
                Field('tax_kingdom'),
                Field('tax_phylum'),
                Field('tax_class'),
                Field('tax_order'),
                Field('tax_superfamily'),
                Field('tax_family'),
                Field('tax_genus'),
                Field('tax_subgenus'),
                Field('tax_specificEpithet'),
                Field('tax_infraspecificEpithet'),
                Field('tax_species'),
                #lazy_tables = True,
                primarykey=['taxonID'],
                format='%(tax_species)s')


#if db(db.taxon.taxonID>0).count() == 0:
 #   db.taxon.truncate()

#if db(db.taxon_genus.genus_id>0).count() == 0:
 #   db.taxon_genus.truncate()

