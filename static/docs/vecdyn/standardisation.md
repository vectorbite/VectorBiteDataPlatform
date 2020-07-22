# Data Standardization models / Data integrity

# Taxonomic Standardization Database: GBIF Backbone Taxonomy

The original [GBIF Backbone Taxonomy](https://www.gbif.org/en/dataset/d7dddbf4-2cf0-4f39-9b2a-bb099caae36c) field names have been renamed for issues concerning ether Web2py, Python, or Postgres keywords, the main programming language that was used to build the Web app and control the database.


| Original Field Name  | Field Name in VecDyn Db        |
| -------------------- | ------------------------------ |
| taxonID              | taxonomic_ID                   |
| kingdom              | taxonomic_kingdom              |
| phylum               | taxonomic_phylum               |
| class                | taxonomic_class                |
| order                | taxonomic_order                |
| superfamily          | taxonomic_superfamily          |
| genus                | taxonomic_genus                |
| subgenus             | taxonomic_subgenus             |
| specificEpithet      | taxonomic_specificEpithet      |
| infraspecificEpithet | taxonomic_infraspecificEpithet |
| species              | taxonomic_species              |



# Geographic Standardization Database: The Global Administrative Unit Layers (GAUL)

[The Global Administrative Unit Layers (GAUL) 2014 dataset](http://www.fao.org/geonetwork/srv/en/metadata.show?id=12691) has been restructured in order to provide one unique observation for each individual geographic entry  or row within the data table e.g. a specific country or specific region. Each specific geographic entity has as individual conde assigned to it and shape file.

| Field name  in original dataset | Field name in VecDyn Db | Description                                                  |
| ------------------------------- | ----------------------- | ------------------------------------------------------------ |
| ------------------------------  | ADM_CODE                | unique code assigned to each administrative unit / shape file |
| ADM0_NAME                       | ADM0_NAME               | country name                                                 |
| ADM1_NAME                       | ADM1_NAME               | first administrative subdivision e.g. Florida                |
| ADM2_NAME                       | ADM2_NAME               | first administrative subdivision e.g. Manatee County         |
| ------------------------------  | centroid_latitude       | latitude of centroid representing centre of administrative unit |
| ------------------------------  | centroid_longitude      | longitude centroid taking representing centre of administrative unit |


