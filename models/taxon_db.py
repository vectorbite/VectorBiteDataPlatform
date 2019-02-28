


####still need to restructure data set so only one specific line i.e. order, kingdom can be selected. Also need to included specificEpithet & infraspecificEpithet in search



#if db(db.taxon.taxonID>0).count() == 0:
 #   db.taxon.truncate()

#if db(db.taxon_genus.genus_id>0).count() == 0:
 #   db.taxon_genus.truncate()




####still need to restructure data set so only one specific line i.e. order, kingdom can be selected. Also need to included specificEpithet & infraspecificEpithet in search


#if db(db.gbif_taxon.taxon_id>0).count() == 0:
 #   db.taxon.truncate()

#if db(db.taxon_genus.genus_id>0).count() == 0:
 #   db.taxon_genus.truncate()


db.define_table('gbif_taxon',
                Field('taxon_id', type = 'id'),###change in db file
                Field('parent_key'),
                Field('basionym_key'),
                Field('status'),
                Field('taxonomic_rank'), #remember to alter this in theprocessed dataset
                Field('constituent_key'),
                Field('source_taxon_key'),
                Field('kingdom_key'),
                Field('phylum_key'),
                Field('class_key'),
                Field('order_key'),
                Field('family_key'),
                Field('genus_key'),
                Field('species_key'),
                Field('name_id'),
                Field('scientific_name'),
                Field('canonical_name'),
                Field('genus_or_above'),
                Field('specific_epithet'),
                Field('infra_specific_epithet'),
                #lazy_tables = True,
                format='%(canonical_name)s'
                )


#db.gbif_taxon.drop()
#if db(db.gbif_taxon.id>0).count() == 0:
 #   db.gbif_taxon.truncate()
