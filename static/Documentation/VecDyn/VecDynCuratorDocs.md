# Global **Vec**tor Population **Dyn**amics Database (VecDyn) Curator Documentation

[TOC]

Welcome to VectorBiTE’s VecDyn Database curator guidelines. This document provides details and instructions on cleaning, preparing and uploading data to the database.

## What is VecDyn?

VecDyn is a global database for spatially and temporally explicit presence-absence and abundance data. We accept and distribute data for animal and plant disease vectors. 

Data Storage and Data Collection Specifications
------------------------------

The following section gives an overview of the database structure and describes all the fields in the VecDyn database and provides details on the rational for their requirement.  

### VecDyn Database structure (backend)

The following image shows the database schema which describes how the data is stored in the database.



![erdplus-diagram (3).png](Images/erdplus-diagram%20%283%29.png)



The database backend consists of three main data collection tables,and two data tables which have been adapted from *third*-*party* sources,  these are used to standardise taxonomic and geographic information.

The **Publication Information Table** table captures publication information like who compiled and submitted the dataset,  and also digital identifiers such as a DOI or ORCID . This table also stores information on data rights and provides links to the original source of the dataset. 

The **Study Meta Data Table** captures information which describes the time series data e.g. where a study took place, what organism was studied and how the sample was collected. The data captured in these fields should help the statistician decide on the quality of the experiment and subsequently the data e.g. how was the organism sampled and can the data be used to make generalised predictions about a wider population. Data in this table captures information that tends to be repeated in population abundance datasets, therefore storing this information once saves storage space improving the scalability of the database. 

The **Time Series Data Table** captures all the information required to produce a Time-Series. Each row should represent a separate observation, at a particular point in time and provide a value for the entity being sampled. This table also captures detailed information like the coordinates of an observation site and particular information about that at a particular site i.e. changes in the environmental or climatic conditions. 

The **Taxonomic Information Table**  is a database table which is used to standardise all  taxonomic information uploaded into the database. It has been adapted from [The Catalogue of Life database](http://www.catalogueoflife.org), which is the most comprehensive and authoritative global index of species currently available. This enables  front-end search (querying) facilities to use internationally recognised naming conventions thus improving the usability of the web app.   

The **Geographic Database Table** is used to standardise geographic information entered into the database. [The Global Administrative Unit Layers (GAUL) 2014 dataset](http://www.fao.org/geonetwork/srv/en/metadata.show?id=12691) is a spatial database that systematises global administrative regions with a unified coding system at country, first (e.g. departments) and second administrative levels (e.g. districts). Each Administrative unit is assigned a unique ID and is connected to a spatial polygon. 

### Data Collection Template

 The latest [vecdyn data collection template](https://github.com/vectorbite/VectorBiteDataPlatform/blob/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv) is available here


| Field Name               | Required Y/N | Data format                       | Details                                                      | Additional Notes                                             |        Db table         |
| ------------------------ | ------------ | --------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | :---------------------: |
| title                    | Yes          | string                            | Short title identifying the data set                         | E.g. “Mosquito Surveillance in Iowa”                         | Publication Information |
| collection_author        | Yes          | string                            | Name of collection author                                    | E.g.family name, given names; OR ‘Iowa State'                | Publication Information |
| dataset_DOI              | No           | string                            | Digital Object Identifier (DOI) of the the dataset           | If the data set was already published                        | Publication Information |
| publication_DOI          | No           | string                            | Second Digital Object Identifier (DOI) if connected to a published article | If the data set was already published as an article          | Publication Information |
| description              | Yes          | string                            | A short description of the study / data set                  | E.g. ‘Long term, fixed trapped, municipal surveillance of west Nile vector population in Colorado from 2000-2010” | Publication Information |
| contact_name             | Yes          | string                            | Name, person, authority, etc…. that may be contacted with inquiries about the data |                                                              | Publication Information |
| contact_affiliation      | Yes          | string                            | Author/contact affiliation                                   |                                                              | Publication Information |
| email                    | No           | string                            | Contact email of the person who supplied or uploaded the dataset |                                                              | Publication Information |
| ORCID                    | No           | string                            | ORCID code                                                   | A digital identifier which provides                          | Publication Information |
| data_rights              | Yes          | string                            | information provided on copyright of dataset i.e. open access, closed, embargo | Open access, closed (who is access available to) or embargo (must provide embargo release date) | Publication information |
| taxon                    | Yes          | string                            | Classification of sample collected                           |                                                              |     Study Meta Data     |
| location_description     | Yes          | string                            | Description of study location                                | Town, county, state                                          |     Study Meta Data     |
| study_collection_area    | Yes          | string                            | The spatial extent (area or volume) of the study             |                                                              |     Study Meta Data     |
| geo_datum                | No           | string                            | Geodetic datum                                               | E.g.. WGS 84                                                 |     Study Meta Data     |
| species_id_method        | No           | string                            | Species identification method                                | A description of the methods species identification          |     study_meta_data     |
| study_design             | No           | string                            | Study design methodology                                     | Indicate if observational study i.e. prospective , retrospective, or experimental etc |     study_meta_data     |
| sampling_strategy        | No           | string                            | Sampling_strategy, indicate the strategy used to select the sample | E.g. simple random sampling, stratified, convenience sampling, cluster, sampling, census etc |     study_meta_data     |
| sampling_method          | No           | string                            | Sampling apparatus e.g..trap type, observation method        | E.g. “CDC light trap w/ CO2”, “Prokopack backpack aspirator”, “Quadrat count” |     study_meta_data     |
| sampling_protocol        | No           | string                            | How entities were sampled                                    |                                                              |     study_meta_data     |
| measurement_unit         | Yes          | string                            | Indicate what was measured                                   | ‘Count’, ‘Count (millions)’, ‘Harvest’, ‘Index of abundance’, ‘Index of territories’, ‘Leaf area’, ‘Mean Count’, ‘Not Specified’, ‘Percent cover’ and ‘Sample’ |     study_meta_data     |
| value_transform          | No           | string                            | Note if the original values have been transformed – list details of the reference value of any data transformation | E.g .Base Year, Log, Proportion                              |     study_meta_data     |
| sample_start_date        | No           | ISO 8601 date format (YYYY-MM-DD) | Date of the sample was set.                                  | E.g. between when a trap was set and when the sample was collected E |    time_series_data     |
| sample_start_time        | No           | ISO 8601 time format (hh:mm:ss)   | Time of the sample was set                                   | Only required when the collector wants to sample populations within specific time frames |    time_series_data     |
| sample_end_date          | Yes          | ISO 8601 date format (YYYY-MM-DD) | The date the sample was collected.                           | If collection occurs monthly use the first day of each month i.e. 2001-01-01, 2001-02-01 |    time_series_data     |
| sample_end_time          | No           | ISO 8601 time format (hh:mm:ss)   | Time of the sample collection                                |                                                              |    time_series_data     |
| trap_duration            | No           | string                            | The amount of time the sample was set                        | e.g. 1 day, 1 hour                                           |    time_series_data     |
| value                    | Yes          | Integer                           | The numerical amount or result from the sample collection    |                                                              |    time_series_data     |
| sample_sex               | No           | string                            | Information on the sex of the organism sampled               |                                                              |    time_series_data     |
| sample_stage             | No           | string                            | Information on the life stage of the organism sampled        | E.g adult, egg, larva, pupa                                  |    time_series_data     |
| sample_location          | No           | string                            |                                                              |                                                              |    time_series_data     |
| sample_collection_area   | No           | string                            | Area of sample location                                      |                                                              |    time_series_data     |
| sample_latitude_DD       | No           | float                             | Latitude of sample area as a decimal degree Specific location of the sample | Ranges [-90,+90] for latitude (north-south measurement)      |    time_series_data     |
| sample_longitude_DD      | No           | float                             | Longitude of sample area as a decimal degree                 | Ranges [-180,180] for longitude (east-west measurement)      |    time_series_data     |
| additional_location_info | No           | string                            | Additional geo information                                   |                                                              |    time_series_data     |
| additional_sample_info   | No           | string                            | Additional sample information                                | Should be used when more information is required to understand the experiment, for example experimental variables |    time_series_data     |
| sample_name              | No           | string                            | A human readable sample name                                 | May exist solely for the benefit of the depositor in organizing their data, use their own internal naming conventions etc. Naming convention is not restricted, but any encoded metadata should be revealed in the other data fields. For example, you may name a sample named ‘Aphid1_StickyTrap_Jan4,’ but you will still have “Sticky Trap” listed in a Collection Method field, and “Jan 4, 2017” in the date field |    time_series_data     |



**Taxonomic Information Table**

The original [The Catalogue of Life database](http://www.catalogueoflife.org) field names had to be renamed for issues concerning Python keywords, the main programming language that was used to build the Web app and control the database. 

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

**Geographic Database Table**

[The Global Administrative Unit Layers (GAUL) 2014 dataset](http://www.fao.org/geonetwork/srv/en/metadata.show?id=12691) has been restructured in order to provide one unique observation for each individual geographic entry  or row within the data table e.g. a specific country or specific region. Each specific geographic entity has as individual conde assigned to it and shape file. 

| Field name  in original dataset | Field name in VecDyn Db | Description                                                  |
| ------------------------------- | ----------------------- | ------------------------------------------------------------ |
| ------------------------------  | ADM_CODE                | unique code assigned to each administrative unit / shape file |
| ADM0_NAME                       | ADM0_NAME               | country name                                                 |
| ADM1_NAME                       | ADM1_NAME               | first administrative subdivision e.g. Florida                |
| ADM2_NAME                       | ADM2_NAME               | first administrative subdivision e.g. Manatee County         |
| ------------------------------  | centroid_latitude       | latitude of centroid representing centre of administrative unit |
| ------------------------------  | centroid_longitude      | longitude centroid taking representing centre of administrative unit |



### Preparing data for upload

*To prepare a dataset for the VecDyn database, follow the subsequent
guidelines*

1.  Download the latest template by right clicking on the following [link](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv) and selecting ‘save.as’.   A completed [example data set can be found here](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv). This will help you to understand how to compile data in the VecDyn template format. You can also access an example [R Markdown recipe](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd) that provides an example of converting an existing data set into a VecDyn formatted dataset.
2.  You can refer to the [VecDyn Data Collection Specifications](#vecdyn-data-collection-specifications) to guide you through the data collection and compilation process.
3.  Note that the data upload facility (*temporary*) is only set up to process one dataset at a time, one data set compromises of one species and one main umbrella geographical location.

*Notice that all files are in plain text e.g. ‘.csv’ format, and not in Excel format or similar. This facilitates text parsing by scripts, prevents data loss/corruption, and allows for detailed comparisons of changes via version control systems.*


### Adding data to the database

For testing purposes (*temporary*) first download the [example data set](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv) to try out the process.

Log on and go to the and go to the [VectorBiTE web app](http://www.vectorbyte.org) and go to ‘My collections’. This will
only work if you have been granted access rights.

*Note that the data upload facility (temporary) is only set up to process one dataset at a time, one data set compromises of one species and one main umbrella geographical location.*

Click on **‘Add New Collection’**

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep1.png" width="75%" style="display: block; margin: auto;" />

The first table captures general information about the data provider and the data series. A data collection may provide centralised information about one or many related datasets.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep2.png" width="75%" style="display: block; margin: auto;" />

Once the collection information has been registered, you now be able to submit data sets to that collection. Click on ‘Add new data set to collection’

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep3.png" width="75%" style="display: block; margin: auto;" />

Next select a taxon, it is best to search using the first box first. When you have found the taxon you are after. Hit the ‘select’ button on the aligning row.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep4.png" width="75%" style="display: block; margin: auto;" />

Next select a geographical location, this either needs to be country or an ADM1 (e.g. State) or ADM2 (county) administrative subdivision. Again, hit the ‘select’ button on the row of your choice.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep5.png" width="75%" style="display: block; margin: auto;" />

Next submit all the study data (metadata) and click on submit once you have completed the page.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep6.png" width="75%" style="display: block; margin: auto;" />

Next you need to upload the complete csv. This will only upload fields related to the time series (sample data)

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep7.png" width="75%" style="display: block; margin: auto;" />

Once completed, you’ll be taken the final page where you can can verify if all the sample data is correct. If it is, click on ‘finish’ button.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep9.png" width="75%" style="display: block; margin: auto;" />

However, if there is a problem you can delete or edit each entry. To delete all the entries hit ‘select’ all and scroll down to the bottom of the page and click ‘delete selected’  
<img
src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep8.png"
width="75%" style="display: block; margin: auto;" />

Note that you can also edit every part of your data after it has been submitted with the exception of taxon names and place names.

Templates, Examples & Tutorials
-------------------------------

[VecDyn Template](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv).

[Build a VecDyn Template dataframe in R Markdown](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd).

[Example data set](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv)

[R markdown recipe: Clean a data set, transform it into the VecDyn format and produce a time
series](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd)

Issues, troubleshooting & suggestions
-------------------------------------

Any suggestions or todos with regards to the database (e.g. new columns, schema modifications etc.) can be logged as [Issues on GitHub](https://github.com/vectorbite/VectorBiteDataPlatform/issues).
Issues allow for discussions among multiple users, file attachments, colour-coded labels etc.

### Known issues

The FAO’s GUAL data set has been restructured for VecDyn. A new column was created which represents an individual ID for each admin unit. This creates a few minor issues, since some region codes are not unique and therefore, an additional ‘b’ has been added to the end of each ADM\_CODE’ which has been used in VecDyn as a ‘Primary key’. 



| ADM_CODE   | ADM2_NAME                         | ADM1_NAME | ADM0_NAME                   |
| ---------- | --------------------------------- | --------- | --------------------------- |
| 48472      | Administrative unit not available | Rukwa     | United Republic of Tanzania |
| 48472**b** | Administrative unit not available | Mwanza    | United Republic of Tanzania |
| 22917      | Ifelodun                          | Kwara     | Nigeria                     |
| 23036      | Surulere                          | Oyo       | Nigeria                     |
| 22917**b** | Ifelodun                          | Osun      | Nigeria                     |
| 23036b     | Surulere                          | Lagos     | Nigeria                     |
| 22602      | Osisioma Ngwa                     | Abia      | Nigeria                     |
| 22602**b** | Ukwa West                         | Abia      | Nigeria                     |
| 15426      | Gnral. Antonio Elizalde           | Guayas    | Ecuador                     |
| 15426**b** | Milagro                           | Guayas    | Ecuador                     |




Miscellaneous
-------------

The `GPDD` directory also contains the documentation of the [**G**lobal **P**opulation **D**ynamics **D**atabase](http://www3.imperial.ac.uk/cpb/databases/gpdd), a pre-existing database of population dynamics, hosted in Silwood Park, Imperial College London since 1999. 
