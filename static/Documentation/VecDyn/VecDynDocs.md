-   [Global **Vec**tor Population **Dyn**amics Database (VecDyn)
    Documentation](#global-vector-population-dynamics-database-vecdyn-documentation)
-   [Introduction](#introduction)
    -   [What is VecDyn?](#what-is-vecdyn)
    -   [Obtaining data from VecDyn](#obtaining-data-from-vecdyn)
    -   [Submitting data](#submitting-data)
    -   [Adding data to the database (*curators
        only*)](#adding-data-to-the-database-curators-only)
-   [Data Collection Specifications](#data-collection-specifications)
    -   [Collection Information Table (i.e.basic data series
        information)](#collection-information-table-i.e.basic-data-series-information)
    -   [Study Data Table (i.e. metadata, *part of the VecDyn data
        collection
        template))*](#study-data-table-i.e.metadata-part-of-the-vecdyn-data-collection-template)
    -   [Sample Data Table (i.e. time series data, *part of the VecDyn
        data collection
        template*))](#sample-data-table-i.e.time-series-data-part-of-the-vecdyn-data-collection-template)
-   [Data Standardization](#data-standardization)
    -   [Standardizing Taxonomy](#standardizing-taxonomy)
    -   [Standardizing Geo Referencing](#standardizing-geo-referencing)
    -   [Standardizing Environmental
        Descriptions](#standardizing-environmental-descriptions)
    -   [VecDyn Data Base structure
        (backend)](#vecdyn-data-base-structure-backend)
-   [Templates, Examples & Tutorials](#templates-examples-tutorials)
-   [Issues, troubleshooting &
    suggestions](#issues-troubleshooting-suggestions)
    -   [Known issues](#known-issues)
-   [Miscellaneous](#miscellaneous)

Global **Vec**tor Population **Dyn**amics Database (VecDyn) Documentation
=========================================================================

Introduction
============

Welcome to VectorBiTE’s VecDyn database guidelines. This document
provides details and instructions on accessing and submitting data. You
can also access data collection templates and examples which will help
you to prepare data for submission.

What is VecDyn?
---------------

VecDyn is a global database for spatially- and temporally- explicit
population presence-absence abundance, density and dynamics data. We
accept and distribute data for both animal and plant disease vectors.

Obtaining data from VecDyn
--------------------------

To get access to VecDyn’s open data, all you need to do is:

1.  Sign up via the [VectorBiTE Data Platform Web
    App](http://vectorbyte.org) and log in.

2.  To query data, go to the index/home page, click on the ‘Get data’
    button and then ‘VecDyn’ button to open up the population data
    search facility.

3.  To query data, either enter a species or geographical location.
    Please note that the search facility is case sensitive.

4.  To download data, just click on the selection box beside a data set
    title, then click on the ‘Download Selected’ button.

*All data is downloaded in text/csv format.*

*Note that the current search facility is temporary and we’ll soon be
implementing a range of new features to help you search and visualise
data.*

Submitting data
---------------

*To submit data to the VecDyn database, follow the subsequent
guidelines*

1.  Download the latest template here by right clicking on the following
    [link](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv).and
    selecting ‘save.as’.  
    A completed [example data
    set](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv)
    can be found here. This will help you to understand how to compile
    data in the VecDyn template format. You can also access an example
    [R Markdown
    recipe](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd)
    here. This guide takes you through the steps of converting an
    existing data set into a VecDyn formatted dataset. Notice that all
    files are in plain text e.g. ‘.csv’ format, and not in Excel format
    or similar. This facilitates text parsing by scripts, prevents data
    loss/corruption, and allows for detailed comparisons of changes via
    version control systems.

2.  You can refer to the [VecDyn Data Collection
    Specifications](#vecdyn-data-collection-specifications) to guide you
    through the data collection and compilation process.

3.  All data submissions are curated through Zenodo, an open access and
    open data platform. [Follow this
    link](https://zenodo.org/deposit/new?c=vecdyn) to get access to our
    submission page. You’ll need log on to Zenodo to access this page,
    if you do not have one you’ll need to set one up.

4.  To submit your dataset, upload the completed VecDyn Template on
    Zenodo. Under ‘Upload type’ select ‘data set’ and fill in all the
    fields under ‘Basic information’, ‘License’ and ‘Funding’. By
    submitting your data through Zenodo, there is no need to send us the
    basic ‘Data Series Information’ separately since this will be
    covered through the Zenodo submission.

5.  We’ll contact you regarding the outcome of your submission once
    we’ve had a look at it.

Adding data to the database (*curators only*)
---------------------------------------------

For testing purposes (*temporary*) first download the [example data
set](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv)
to try out the process.

Log on and go to the and go to the[VectorBiTE web
app](http://www.vectorbyte.org) and go to ‘My collections’. Note this
will only work if you have been granted access rights.

Click on **‘Add New Collection’**

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep1.png" width="75%" style="display: block; margin: auto;" />

The first table captures general information about the data provider and
the data series. A data series may provide centralised information about
one or many related datasets.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep2.png" width="75%" style="display: block; margin: auto;" />

Once the collection information has been registered, you now be able to
submit data sets to that collection. Click on ‘Add new data set to
collection’

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep3.png" width="75%" style="display: block; margin: auto;" />

Next select a taxon, it is best to search using the first box first.
When you have found the taxon you are after. Hit the ‘select’ button on
the aligning row.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep4.png" width="75%" style="display: block; margin: auto;" />

Next select a geographical location, this either needs to be country or
an ADM1 (e.g. State) or ADM2 (county) administrative subdivision. Again,
hit the ‘select’ button on the row of your choice.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep5.png" width="75%" style="display: block; margin: auto;" />

Next submit all the study data (metadata) and click on submit once you
have completed the page.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep6.png" width="75%" style="display: block; margin: auto;" />

Next you need to upload the complete csv. This will only upload fields
related to the time series (sample data)

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep7.png" width="75%" style="display: block; margin: auto;" />

Once completed, you’ll be taken the final page where you can see all the
sample data relating to the study data. From here you can verify all the
information is correct. If it click on ‘finish’ to be take back the
collections page.

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep9.png" width="75%" style="display: block; margin: auto;" />

However, if these is r problem you can delete or edit each entry. To
delete all the entries hit ‘select’ all and scroll down to the bottom of
the page and click ‘delete selected’  
<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/DataUploadStep8.png" width="75%" style="display: block; margin: auto;" />

Note that you can also edit every part of your data after it has been
submitted except for taxon names and place names.

Data Collection Specifications
==============================

The following section describes all the fields in the VecDyn data base
and provides details on the rational behind their requirement. This
section will also guide through completing the data collection template.
Note that some fields are required and others are optional, although,
ideally all fields should be completed.

Collection Information Table (i.e.basic data series information)
----------------------------------------------------------------

The first table captures general information about the data provider and
the data series. A data series may provide centralised information about
one or many related datasets. The following information should be
supplied separately when a data set is submitted.

<table>
<colgroup>
<col style="width: 17%" />
<col style="width: 7%" />
<col style="width: 48%" />
<col style="width: 26%" />
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
<td>E.g. “Mosquito Surveillance in Iowa”</td>
</tr>
<tr class="even">
<td>collection_authority</td>
<td>Yes</td>
<td>Name of collection authority</td>
<td>E.g. family name, given names; OR ‘Iowa State</td>
</tr>
<tr class="odd">
<td>DOI</td>
<td>Optional</td>
<td>Digital Object Identifier (DOI)</td>
<td>If the data set was already published</td>
</tr>
<tr class="even">
<td>publication_date</td>
<td>Yes</td>
<td>ISO 8601 date format (YYYY-MM-DD)</td>
<td>In case the data set was already published elsewhere, use the date of first publication.</td>
</tr>
<tr class="odd">
<td>description</td>
<td>Yes</td>
<td>A short description of the study / data set</td>
<td>E.g. ‘Long term, fixed trapped, municipal surveillance of west Nile vector population in Colorado from 2000-2010”</td>
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
<td>Name, person, authority, etc…. that may be contacted with inquiries about the data</td>
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

The next table captures metadata for a study. A study should be regarded
as a set of data for one single species, at a given location over a
specific time period. The metadata should be used to capture information
like the general location of a study and particular methods or equipment
used to collect data on the study organism. Note that data entered into
these fields should be repeated for each time series row/observation. In
effect, the metadata helps to describe the time series data.

Study Data Table (i.e. metadata, *part of the VecDyn data collection template))*
--------------------------------------------------------------------------------

<table>
<colgroup>
<col style="width: 17%" />
<col style="width: 7%" />
<col style="width: 47%" />
<col style="width: 26%" />
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
<td>The title should be related to the data series title and the study organism e.g. “Tiger Mosquito Surveillance in Iowa”</td>
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
<td>Use the United Nation’s “Standard Country” names. See here <a href="https://unstats.un.org/unsd/methodology/m49/" class="uri">https://unstats.un.org/unsd/methodology/m49/</a></td>
</tr>
<tr class="even">
<td>location_description</td>
<td>yes</td>
<td>Description of study location</td>
<td>E.g.. town, county, state</td>
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
<td>E.g.. WGS 84</td>
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
<td>E.g. simple random sampling, stratified, convenience sampling, cluster, sampling, census etc.</td>
</tr>
<tr class="even">
<td>sampling_method</td>
<td>Optional</td>
<td>Sampling apparatus e.g..trap type, observation method)</td>
<td>E.g. “CDC light trap w/ CO2”, “Prokopack backpack aspirator”, “Quadrat count”</td>
</tr>
<tr class="odd">
<td>sampling_protocol</td>
<td>Optional</td>
<td>How entities were sampled</td>
<td>E.g. ‘Count’, ‘Count (millions)’, ‘Harvest’, ‘Index of abundance’, ‘Index of territories’, ‘Leaf area’, ‘Mean Count’, ‘Not Specified’, ‘Percent cover’ and ‘Sample’.</td>
</tr>
<tr class="even">
<td>measurement_unit</td>
<td>Optional</td>
<td>Unit of measurement</td>
<td>The entity observed. Entries could include, ‘individuals’, ‘adults’, ‘cells’, ‘egg masses’, and ‘pelts’</td>
</tr>
<tr class="odd">
<td>sample_collection_area</td>
<td>Optional</td>
<td>The spatial extent (area or volume) of the sample</td>
<td>If relevant (E.g.., when collection method is transect or quadrat), in units of area or volume, the spatial coverage of the sampling unit e.g. “100 m^2”, “1 liter”, “1 ha”, “10m^3”</td>
</tr>
<tr class="even">
<td>value_transform</td>
<td>Optional</td>
<td>Note if the original values have been transformed – list details of the reference value of any data transformation</td>
<td>E.g..Base Year, Log, None, Not Specified, Proportion, Unknown, x 1000 lbs</td>
</tr>
</tbody>
</table>

In the following table, the next set of variables captures the
information required to produce a time-Series dataset. Each row should
represent a separate observation, at a particular point in time. Note
that any additional information about a sub sample can be added here too
e.g. point location of sample sites or sex of a species.

Sample Data Table (i.e. time series data, *part of the VecDyn data collection template*))
-----------------------------------------------------------------------------------------

<table>
<colgroup>
<col style="width: 17%" />
<col style="width: 7%" />
<col style="width: 47%" />
<col style="width: 26%" />
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
<td>Only required when the collector wants to sample populations within specific time frames e.g. between when a trap was set and when the sample was collected</td>
</tr>
<tr class="even">
<td>sample_start_time</td>
<td>Optional</td>
<td>Start time: ISO 8601 time format (hh:mm:ss)</td>
<td>Only required when the collector wants to sample populations within specific time frames e.g. time example: 15:53:00</td>
</tr>
<tr class="odd">
<td>sample_end_date</td>
<td>Yes</td>
<td>Collection date:ISO 8601 time format (hh:mm:ss)</td>
<td>The date the sample was collected. If collection occurs monthly use the first day of each month i.e. 2001-01-01, 2001-02-01. Date example: 2008-09-15</td>
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
<td>Specific location of the sample Ranges [-90,+90] for latitude (north-south measurement)</td>
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

To standardise taxonomy, VecDyn includes the [The Catalogue of Life
database](http://www.catalogueoflife.org), which is the most
comprehensive and authoritative global index of species currently
available. Taxonomic data will be standardised by curators upon the
addition of a dataset to the VecDyn database.

<table>
<thead>
<tr class="header">
<th>Field Name</th>
<th>Name in DB</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>taxonID</td>
<td>taxonID</td>
</tr>
<tr class="even">
<td>kingdom</td>
<td>tax_kingdom</td>
</tr>
<tr class="odd">
<td>phylum</td>
<td>tax_phylum</td>
</tr>
<tr class="even">
<td>class</td>
<td>tax_class</td>
</tr>
<tr class="odd">
<td>order</td>
<td>tax_order</td>
</tr>
<tr class="even">
<td>superfamily</td>
<td>tax_superfamily</td>
</tr>
<tr class="odd">
<td>family</td>
<td>tax_family</td>
</tr>
<tr class="even">
<td>genus</td>
<td>tax_genus</td>
</tr>
<tr class="odd">
<td>subgenus</td>
<td>tax_subgenus</td>
</tr>
<tr class="even">
<td>specificEpithet</td>
<td>tax_specificEpithet</td>
</tr>
<tr class="odd">
<td>infraspecificEpithet</td>
<td>tax_infraspecificEpithet</td>
</tr>
<tr class="even">
<td>species</td>
<td>tax_species</td>
</tr>
</tbody>
</table>

Standardizing Geo Referencing
-----------------------------

In order to standardise geographic information, the [the Global
Administrative Unit Layers (GAUL) 2014
databaset](http://www.fao.org/geonetwork/srv/en/metadata.show?id=12691)
has been incorporated into the VecDyn database. The GAUL database
systematises global administrative regions with a unified coding system
at country, first (e.g. departments) and second administrative levels
(e.g. districts). Each Administrative unit is assigned a unique ID and
is connected to a spatial polygon. Therefore data submitted to the
VecDyn database can be represented spatially, as long as a minimal set
of information is provided by the submitter e.g. country, county,
region, state.

<table>
<colgroup>
<col style="width: 59%" />
<col style="width: 40%" />
</colgroup>
<thead>
<tr class="header">
<th>Field Name in db</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>ADM_CODE</td>
<td>unique code assigned to each administrative unit / shape file</td>
</tr>
<tr class="even">
<td>ADM0_NAME</td>
<td>country name</td>
</tr>
<tr class="odd">
<td>ADM1_NAME</td>
<td>first administrative subdivision e.g. Florida</td>
</tr>
<tr class="even">
<td>ADM2_NAME</td>
<td>first administrative subdivision e.g. Manatee County</td>
</tr>
<tr class="odd">
<td>centroid_latitude</td>
<td>latitude of centroid representing centre of administrative unit</td>
</tr>
<tr class="even">
<td>centroid_longitude</td>
<td>longitude centroid taking representing centre of administrative unit</td>
</tr>
</tbody>
</table>

Standardizing Environmental Descriptions
----------------------------------------

Environmental descriptors can be standardized using
[ENVO](http://environmentontology.org/Browse-EnvO). ENVO is an ontology
which represents knowledge about environments,environmental processes,
ecosystems, habitats, and related entities.

VecDyn Data Base structure (backend)
------------------------------------

<img src="https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Images/vecdyn_er_diagram.png" width="75%" style="display: block; margin: auto;" />

Templates, Examples & Tutorials
===============================

[VecDyn
Template](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv).

[Build a VecDyn Template dataframe in R
Markdown](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd).

[Example data
set](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv)

[R markdown recipe: Clean a data set, transform it into the VecDyn
format and produce a time
series](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd)

Issues, troubleshooting & suggestions
=====================================

Any suggestions or todos with regards to the database (e.g. new columns,
schema modifications etc.) can be logged as [Issues on
GitHub](https://github.com/vectorbite/VectorBiteDataPlatform/issues).
Issues allow for discussions among multiple users, file attachments,
colour-coded labels etc.

Known issues
------------

The FAO’s GUAL data set has been restructured for VecDyn. A new column
was created which represents an individual ID for each admin unit. This
creates a few minor issues, since some region codes are not unique and
therefore, an additional ‘b’ has been added to the end of each
ADM\_CODE’ which has been used in VecDyn as a ‘Primary key’

<table>
<thead>
<tr class="header">
<th>ADM_CODE</th>
<th>ADM2_NAME</th>
<th>ADM1_NAME</th>
<th>ADM0_NAME</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>48472</td>
<td>Administrative unit not available</td>
<td>Rukwa</td>
<td>United Republic of Tanzania</td>
</tr>
<tr class="even">
<td>48472<strong>b</strong></td>
<td>Administrative unit not available</td>
<td>Mwanza</td>
<td>United Republic of Tanzania</td>
</tr>
<tr class="odd">
<td>22917</td>
<td>Ifelodun</td>
<td>Kwara</td>
<td>Nigeria</td>
</tr>
<tr class="even">
<td>23036</td>
<td>Surulere</td>
<td>Oyo</td>
<td>Nigeria</td>
</tr>
<tr class="odd">
<td>22917<strong>b</strong></td>
<td>Ifelodun</td>
<td>Osun</td>
<td>Nigeria</td>
</tr>
<tr class="even">
<td>23036b</td>
<td>Surulere</td>
<td>Lagos</td>
<td>Nigeria</td>
</tr>
<tr class="odd">
<td>22602</td>
<td>Osisioma Ngwa</td>
<td>Abia</td>
<td>Nigeria</td>
</tr>
<tr class="even">
<td>22602<strong>b</strong></td>
<td>Ukwa West</td>
<td>Abia Nigeria</td>
</tr>
<tr class="odd">
<td>15426</td>
<td>Gnral. Antonio Elizalde</td>
<td>Guayas</td>
<td>Ecuador</td>
</tr>
<tr class="even">
<td>15426<strong>b</strong></td>
<td>Milagro</td>
<td>Guayas</td>
<td>Ecuador</td>
</tr>
</tbody>
</table>

Miscellaneous
=============

The `GPDD` directory also contains the documentation of the [**G**lobal
**P**opulation **D**ynamics
**D**atabase](http://www3.imperial.ac.uk/cpb/databases/gpdd), a
pre-existing database of population dynamics, hosted in Silwood Park,
Imperial College London since 1999. VecDyn aims to learn from both
GPDD’s success and potential shortcomings as it moves forward.
