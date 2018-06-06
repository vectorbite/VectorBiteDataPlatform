Global **Vec**tor Population **Dyn**amics Database (VecDyn) Documentation
================

-   [Introduction](#introduction)
    -   [What is VecDyn?](#what-is-vecdyn)
    -   [Obtaining data from VecDyn](#obtaining-data-from-vecdyn)
-   [Data Collection Specifications](#data-collection-specifications)
    -   [Basic Data Series Information](#basic-data-series-information)
    -   [Metadata *(part of the VecDyn data collection template)*](#metadata-part-of-the-vecdyn-data-collection-template)
    -   [Time Series Data *(part of the VecDyn data collection template)*](#time-series-data-part-of-the-vecdyn-data-collection-template)
-   [Data Standardization](#data-standardization)
    -   [Standardizing Taxonomy](#standardizing-taxonomy)
    -   [Standardizing Geo Referencing](#standardizing-geo-referencing)
    -   [Standardizing Environmental Descriptions](#standardizing-environmental-descriptions)
-   [Submitting data](#submitting-data)
    -   [Templates, Examples & Tutorials](#templates-examples-tutorials)
-   [Issues, troubleshooting & suggestions](#issues-troubleshooting-suggestions)
-   [Known isses](#known-isses)
-   [Miscellaneous](#miscellaneous)

Introduction
============

Welcome to VectorBiTE's VecDyn database guidelines. This document provides details and instructions on accessing and submitting data. You can also access data collection templates and examples which will help you to prepare data for submission to us.

What is VecDyn?
---------------

VecDyn is a global database for spatially- and temporally- explicit population presence-absence abundance, density and dynamics data.

Obtaining data from VecDyn
--------------------------

To get access to Vecdyn's open data, all you need to do is sign up via the [VectorBiTE Data Platform Web App](http://vectorbyte.org). Querying data is simple, on the top of the page click on **'Get data'**, then **'VecDyn'** to open up the population data search facility. You can either search for data by species or geographical location. Please note that the search facility is **Case Sensitve**. To download data, just click inside a selection box beside each data set title, then click on 'Download Selected'. All data is provided in text/csv format.

Data Collection Specifications
==============================

The following section lists all the fields in the VecDyn data base and provides details on their meaning and why they are required. This section can be used as a guide to help you to fill in the data collection template. Note that some fields are required and others are optional. Ideally, all fields should be completed.

Basic Data Series Information
-----------------------------

The first table captures general information about the data provider and the data series. A data series may provide centralised information about one or many related datasets. The following information should be supplied separately when a data set is submitted.

<table>
<colgroup>
<col width="16%" />
<col width="8%" />
<col width="44%" />
<col width="30%" />
</colgroup>
<thead>
<tr class="header">
<th>Field Name</th>
<th>Required</th>
<th>Details</th>
<th>Additional Notes</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>title</td>
<td>Yes</td>
<td>Short title identifying the data series</td>
<td>e.g. “Mosquito Surveillance in Iowa”</td>
</tr>
<tr class="even">
<td>collection_authority</td>
<td>Yes</td>
<td>Name of collection authority</td>
<td>e.g. family name, given names; OR ‘Iowa State</td>
</tr>
<tr class="odd">
<td>DOI</td>
<td>Optional</td>
<td>Digital Object Identifier (DOI)</td>
<td>if the data set was already published</td>
</tr>
<tr class="even">
<td>publication_date</td>
<td>Yes</td>
<td>ISO 8601 date format (YYYY-MM-DD)</td>
<td>in case the data set was already published elsewhere, use the date of first publication.</td>
</tr>
<tr class="odd">
<td>description</td>
<td>Yes</td>
<td>A short description of the study / data set</td>
<td>e.g. ‘Long term, fixed trapped, municipal surveillance of west Nile vector population in Colorado from 2000-2010”</td>
</tr>
<tr class="even">
<td>URL</td>
<td>Yes</td>
<td>web link to data set</td>
<td></td>
</tr>
<tr class="odd">
<td>contact_name</td>
<td>Yes</td>
<td>Name, person, authority, etc... that may be contacted with inquiries about the data</td>
<td></td>
</tr>
<tr class="even">
<td>contact_affiliation</td>
<td>Optional</td>
<td>Author/contact affiliation</td>
<td></td>
</tr>
<tr class="odd">
<td>email</td>
<td>Optional</td>
<td>Contact email</td>
<td></td>
</tr>
<tr class="even">
<td>ORCID</td>
<td>Optional</td>
<td>ORCID code</td>
<td>A digital identifier which provides</td>
</tr>
<tr class="odd">
<td>keywords</td>
<td>Optional</td>
<td>Keywords for web searches</td>
<td></td>
</tr>
</tbody>
</table>

The next table captures metadata for a study, a study should be regarded as a set of data for one single species, at a given location over a specific time period. The metadata should also be used to capture things like the general location of a study,particular methods or equipment used. Note that data entered into these fields should be repeated for each time series row/observation, In effect, the metadata helps to describe the time series data.

Metadata *(part of the VecDyn data collection template)*
--------------------------------------------------------

<table>
<colgroup>
<col width="16%" />
<col width="8%" />
<col width="44%" />
<col width="30%" />
</colgroup>
<thead>
<tr class="header">
<th>Field Name</th>
<th>Required</th>
<th>Details</th>
<th>Additional Notes</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>data_set_name</td>
<td>yes</td>
<td>Short title identifying the data set</td>
<td>The title should be related to the data series title e.g. “Tiger Mosquito Surveillance in Iowa”</td>
</tr>
<tr class="even">
<td>taxon_name</td>
<td>yes</td>
<td>Classification of sample collected</td>
<td>Use the Catalogue of Life 2017 check-list to obtain the taxon name, only use names which are classed as ‘accepted’. See <a href="http://www.catalogueoflife.org/annual-checklist/2017/" class="uri">http://www.catalogueoflife.org/annual-checklist/2017/</a></td>
</tr>
<tr class="odd">
<td>country</td>
<td>yes</td>
<td>Country where study was conducted</td>
<td>Use the United Nations's &quot;Standard Country&quot; names. See here <a href="https://unstats.un.org/unsd/methodology/m49/" class="uri">https://unstats.un.org/unsd/methodology/m49/</a></td>
</tr>
<tr class="even">
<td>location_description</td>
<td>yes</td>
<td>Description of study location</td>
<td>e.g.. town, county, state</td>
</tr>
<tr class="odd">
<td>location_environment</td>
<td>optional</td>
<td>General description about the location</td>
<td>Where possible, please use the Environment Ontology search feature to characterize the location’s environment (see <a href="http://www.environmentontology.org/Browse-EnvO" class="uri">http://www.environmentontology.org/Browse-EnvO</a>)</td>
</tr>
<tr class="even">
<td>study_lat_DD</td>
<td>optional</td>
<td>Latitude of study area as a decimal degree</td>
<td>General location of the study Ranges[-90,+90] for latitude (north-south measurement)</td>
</tr>
<tr class="odd">
<td>study_long_DD</td>
<td>optional</td>
<td>Longitude of study area as a decimal degree</td>
<td>Ranges [-180,180] for longitude (east-west measurement)</td>
</tr>
<tr class="even">
<td>spatial_accuracy</td>
<td>optional</td>
<td>Spatial accuracy of the given coordinates</td>
<td>Value between 0 - 6 indicating the accuracy of the location given. 0 = Unknown, 1 = &gt;100 km radius, 2 = 10 - &lt;100km, 3 = 1 - &lt;9km, 4 = 0.1 - 1km, 5 = 10 - 100m, 6 = accurate survey (incl. GPS) &lt;= 10m</td>
</tr>
<tr class="odd">
<td>location_extent</td>
<td>optional</td>
<td>Indicating the size of the study site.</td>
<td>A value between 1 - 4. Where available absolute size is recorded in the Area field. 1 = Region &gt;10 km radius, 2 = Local Area 1-10 km radius, 3 = Extended Site 0.1-1 km radius, 4 = Precise Site &lt;0.1 km radius</td>
</tr>
<tr class="even">
<td>geo_datum</td>
<td>optional</td>
<td>Geodetic datum</td>
<td>e.g.. WGS 84</td>
</tr>
<tr class="odd">
<td>species_id_method</td>
<td>Optional</td>
<td>Species Identification Method</td>
<td>A description of the methods species identification.</td>
</tr>
<tr class="even">
<td>study_design</td>
<td>Optional</td>
<td>Study design methodology</td>
<td>Indicate if observational study i.e.prospective , retrospective, or experimental etc</td>
</tr>
<tr class="odd">
<td>sampling_strategy</td>
<td>Optional</td>
<td>Indicate the strategy used to select the sample</td>
<td>E.g.. simple random sampling, stratified, convenience sampling, cluster, sampling, census etc</td>
</tr>
<tr class="even">
<td>sampling_method</td>
<td>Optional</td>
<td>Sampling apparatus e.g..trap type, observation method)</td>
<td>e.g. “CDC light trap w/ CO2”, “Prokopack backpack aspirator”, “Quadrat count”</td>
</tr>
<tr class="odd">
<td>sampling_protocol</td>
<td>Optional</td>
<td>How entities were sampled</td>
<td>e.g. ‘Count’, ‘Count (millions)’, ‘Harvest’, ‘Index of abundance’, ‘Index of territories’, ‘Leaf area’, ‘Mean Count’, ‘Not Specified’, ‘Percent cover’ and ‘Sample’.</td>
</tr>
<tr class="even">
<td>measurement_unit</td>
<td>Optional</td>
<td>Unit of measurement</td>
<td>The entity observed. Entries could include, 'individuals', ‘adults’, ‘cells’, ‘egg masses’, and ‘pelts’</td>
</tr>
<tr class="odd">
<td>sample_collection_area</td>
<td>Optional</td>
<td>The spatial extent (area or volume) of the sample</td>
<td>If relevant (e.g.., when collection method is transect or quadrat), in units of area or volume, the spatial coverage of the sampling unit e.g. “100 m^2”, “1 liter”, “1 ha”, “10m^3”</td>
</tr>
<tr class="even">
<td>value_transform</td>
<td>Optional</td>
<td>Note if the original values have been transformed – list details of the reference value of any data transformation</td>
<td>e.g..Base Year, Log, None, Not Specified, Proportion, Unknown, x 1000 lbs</td>
</tr>
</tbody>
</table>

The next set of variables in the following table captures the information required to produce a time-Series dataset, each row should represent a separate observation, at a particular point in time. Note that any additional information about a sub-sample can be added here too e.g. point location of sample sites or sex of a species.

Time Series Data *(part of the VecDyn data collection template)*
----------------------------------------------------------------

<table>
<colgroup>
<col width="16%" />
<col width="8%" />
<col width="44%" />
<col width="30%" />
</colgroup>
<thead>
<tr class="header">
<th>Field Name</th>
<th>Required</th>
<th>Details</th>
<th>Additional Notes</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>sample_start_date</td>
<td>Optional</td>
<td>Start date: ISO 8601 date format (YYYY-MM-DD)</td>
<td>Only required when the collector wants to sample populations within specific time frames e.g. between when a trap was set and when the sample was collected</td>
</tr>
<tr class="even">
<td>sample_start_time</td>
<td>Optional</td>
<td>Start time: ISO 8601 time format (hh:mm:ss)</td>
<td>Only required when the collector wants to sample populations within specific time frames e.g. time example: 15:53:00</td>
</tr>
<tr class="odd">
<td>sample_end_date</td>
<td>Yes</td>
<td>Collection date:ISO 8601 time format (hh:mm:ss)</td>
<td>The date the sample was collected. If collection occurs monthly use the first day of each month i.e. 2001-01-01, 2001-02-01. Date example: 2008-09-15, Datetime example: 2008-09-15T15:53:00</td>
</tr>
<tr class="even">
<td>sample_end_time</td>
<td>Optional</td>
<td>Time of the sample collection:</td>
<td>ISO 8601 time format (hh:mm:ss)</td>
</tr>
<tr class="odd">
<td>value</td>
<td>Yes</td>
<td>The numerical amount or result from the sample collection</td>
<td>The population data from study</td>
</tr>
<tr class="even">
<td>sample_info</td>
<td>Optional</td>
<td>Additional sample information</td>
<td>Should be used when more information is required to understand the experiment, for example experimental variables, sub-locations, etc.Could report general info regarding sample location. Some users may report wind speeds Examples: “Forest” vs “Field”, “Winter”vs “Summer”, “Inside” vs “Outside”, “200 meters above sea level”</td>
</tr>
<tr class="odd">
<td>sample_lat_DD</td>
<td>Optional</td>
<td>Latitude of sample area as a decimal degree</td>
<td>General location of the sample Ranges[-90,+90] for latitude (north-south measurement)</td>
</tr>
<tr class="even">
<td>sample_long_DD</td>
<td>Optional</td>
<td>Longitude of sample area as a decimal degree</td>
<td>Ranges [-180,180] for longitude (east-west measurement)</td>
</tr>
<tr class="odd">
<td>sample_name</td>
<td>Optional</td>
<td>A human readable sample name</td>
<td>May exist solely for the benefit of the depositor in organizing their data, use their own internal naming conventions etc.Naming convention is not restricted, but any encoded metadata should be revealed in the other data fields. For example, you may name a sample named ‘Aphid1_StickyTrap_Jan4,’ but you will still have “Sticky Trap” listed in a Collection Method field, and “Jan 4, 2017” in the date field.</td>
</tr>
<tr class="even">
<td>sample_sex</td>
<td>Optional</td>
<td>Information on the sex of the organism sampled</td>
<td></td>
</tr>
</tbody>
</table>

Data Standardization
====================

Standardizing Taxonomy
----------------------

To standardise taxonomy, VecDyn includes the [The Catalogue of Life database](http://www.catalogueoflife.org), which is the most comprehensive and authoritative global index of species currently available. Taxonomic data will be adjusted by curators on addition of a dataset to the database.

Standardizing Geo Referencing
-----------------------------

In order to standardise all geographic information, the [the Global Administrative Unit Layers (GAUL) 2014 databaset](http://www.fao.org/geonetwork/srv/en/metadata.show?id=12691) has been incorporated into the VecDyn database. The GAUL database systematises global administrative regions with a unified coding system at country, first (e.g. departments) and second administrative levels (e.g. districts). Each Administrative unit is assigned a unique ID and is connected to a spatial polygon. Therefore data submitted to the VecDyn database can be potentially represented spatially, as long as a minimal set of information is provided by the submitter e.g. country, county, region, state.

Standardizing Environmental Descriptions
----------------------------------------

<http://environmentontology.org/Browse-EnvO> search widget to the app <https://www.bioontology.org/wiki/index.php/NCBO_Widgets> <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3633000/> <https://github.com/ncbo/bioportal_web_ui/tree/master/public/widgets>

Submitting data
===============

*To submit data to the VecDyn database, follow the subsequent guidelines*

1.  Download the latest template here by right clicking on the link and selecting 'save.as' or 'save link' depending on your operating system [VecDyn Template](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv).

A completed [example data set](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring2013/vecdyn_manatee_A.aegypti.csv) here. This will help you to understand how to compile the VecDyn Template.

You can also access an example [R Markdown recipe](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring2013/ManateeCountryMosquitoMonitoring%20-%20Aedes.aegypti.Rmd) here. This guide will takes you through the steps of converting an existing data set into the VecDyn dataset using the vecdyn template. Notice that all files are in plain text e.g. '.csv' format, and not in Excel format or similar. This facilitates text parsing by scripts, prevents data loss/corruption, and allows for detailed comparisons of changes via version control systems.

1.  You can refer to the [VecDyn Data Collection Specifications](#vecdyn-data-collection-specifications) to guide you through the data creation process. See [VecDyn template](#vecdyn-template).

2.  All data submission are curated through Zenodo, an open access and open data platform. [Follow this link](https://zenodo.org/deposit/new?c=vecdyn) to get access to our submission page.

3.  To submit your dataset via Zenodo, upload the completed VecDyn Template. Under 'Upload type' select 'data set' and fill in all the fields under 'Basic information', 'License' and 'Funding' forms. If you submit data through Zenodo there is no need to send us the basic 'Data Series Information' separately since this will be covered through the Zenodo submission.

4.  We'll contact you regarding the outcome of your submission once we've had a look at it.

Templates, Examples & Tutorials
-------------------------------

*In order to download the following files ensure you 'right click' and select the appropriate option do download the file.* [VecDyn Template](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv). [Build a VecDyn Template dataframe in R Markdown](https://github.com/vectorbite/VectorBiteDataPlatform/blob/master/static/Documentation/VecDyn/Template%26Scripts/R%20VecDyn%20template%20Markdown%20Script.Rmd). [Example data set](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring2013/vecdyn_manatee_A.aegypti.csv) [R markdown recipe: Clean a data set, transform it into the VecDyn format and produce a time series](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring2013/ManateeCountryMosquitoMonitoring%20-%20Aedes.aegypti.Rmd)

Issues, troubleshooting & suggestions
=====================================

Any suggestions or todos with regards to the database (e.g. new columns, schema modifications etc.) can be logged as [Issues on GitHub](https://github.com/vectorbite/VectorBiteDataPlatform/issues). Issues allow for discussions among multiple users, file attachments, colour-coded labels etc.

Known isses
===========

The FAO's GUAL data set has been restructured for VecDyn. A new column was created which represents an individual ID for each admin unit. This creates a few minor issues, since some region codes are not unique and therefore, an additional 'b' has been added to the end of each'ADM\_CODE' which has been used in VecDyn as a 'Primary key'

| ADM\_CODE  | ADM2\_NAME                        | ADM1\_NAME   | ADM0\_NAME                  |
|------------|-----------------------------------|--------------|-----------------------------|
| 48472      | Administrative unit not available | Rukwa        | United Republic of Tanzania |
| 48472**b** | Administrative unit not available | Mwanza       | United Republic of Tanzania |
| 22917      | Ifelodun                          | Kwara        | Nigeria                     |
| 23036      | Surulere                          | Oyo          | Nigeria                     |
| 22917**b** | Ifelodun                          | Osun         | Nigeria                     |
| 23036b     | Surulere                          | Lagos        | Nigeria                     |
| 22602      | Osisioma Ngwa                     | Abia         | Nigeria                     |
| 22602**b** | Ukwa West                         | Abia Nigeria |
| 15426      | Gnral. Antonio Elizalde           | Guayas       | Ecuador                     |
| 15426**b** | Milagro                           | Guayas       | Ecuador                     |

Miscellaneous
=============

The `GPDD` directory also contains the documentation of the [**G**lobal **P**opulation **D**ynamics **D**atabase](http://www3.imperial.ac.uk/cpb/databases/gpdd), a pre-existing database of population dynamics, hosted in Silwood Park, Imperial College London since 1999. VecDyn aims to learn from both GPDD's success and potential shortcomings as it moves forward.
