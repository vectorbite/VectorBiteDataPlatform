def vecdyn_taxon_standardiser(): # some randomisation needs to go into this
    tax_match = db((db.study_meta_data.taxon_id == None) & (db.study_meta_data.taxon == db.gbif_taxon.canonical_name)).\
        select(db.study_meta_data.id, db.gbif_taxon.taxon_id, db.gbif_taxon.canonical_name, db.gbif_taxon.genus_or_above,
               db.gbif_taxon.taxonomic_rank, limitby=(0, 200))
    for row in tax_match:
                        id = row.study_meta_data.id
                        taxon_id = row.gbif_taxon.taxon_id
                        canonical_name = row.gbif_taxon.canonical_name
                        genus_or_above = row.gbif_taxon.genus_or_above
                        taxonomic_rank = row.gbif_taxon.taxonomic_rank
                        db(db.study_meta_data.id == id).update(taxon_id=taxon_id, canonical_name=canonical_name,
                                                               genus_or_above=genus_or_above, taxonomic_rank=taxonomic_rank)

