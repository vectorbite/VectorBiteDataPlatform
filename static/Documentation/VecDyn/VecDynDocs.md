Global **Vec**tor Population **Dyn**amics Database (VecDyn)
Documentation
================

# Introduction

Welcome to VectorBiTE’s VecDyn database guidelines. This document
provides details and instructions on accessing and submitting data. You
can also access data collection templates and examples which will help
you to prepare data for submission.

## What is VecDyn?

VecDyn is a global database for spatially- and temporally- explicit
population presence-absence abundance, density and dynamics data. We
accept and distribute data for both animal and plant disease vectors.

## Obtaining data from VecDyn

To get access to Vecdyn’s open data, all you need to do is sign up via
the [VectorBiTE Data Platform Web App](http://vectorbyte.org). Querying
data is simple, on the top of the page click on ‘Get data’, then
‘VecDyn’ buttons to open up the population data search facility. You
can currently search for data by species or geographical location.
Please note that the search facility is case sensitve. To download data,
just click inside a selection box beside a data set title, then click on
the ‘Download Selected’ button. All data is downloaded in text/csv
format. Note that the current search facility is temporary and we’ll
soon be implementing a range of new features to help you search and
visualise data.

## Submitting data

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
    existing data set into a VecDyn dataset using the vecdyn template.
    Notice that all files are in plain text e.g. ‘.csv’ format, and not
    in Excel format or similar. This facilitates text parsing by
    scripts, prevents data loss/corruption, and allows for detailed
    comparisons of changes via version control systems.

2.  You can refer to the [VecDyn Data Collection
    Specifications](#vecdyn-data-collection-specifications) to guide you
    through the data collection and compilation process.

3.  All data submissions are curated through Zenodo, an open access and
    open data platform. [Follow this
    link](https://zenodo.org/deposit/new?c=vecdyn) to get access to our
    submission page.

4.  To submit your dataset, upload the completed VecDyn Template on
    Zenodo. Under ‘Upload type’ select ‘data set’ and fill in all the
    fields under ‘Basic information’, ‘License’ and ‘Funding’. By
    submitting your data through Zenodo, there is no need to send us the
    basic ‘Data Series Information’ separately since this will be
    covered through the Zenodo submission.

5.  We’ll contact you regarding the outcome of your submission once
    we’ve had a look at it.

# Data Collection Specifications

The following section describes all the fields in the VecDyn data base
and provides details on the rational behind their requirement. This
section will also guide through completing the data collection template.
Note that some fields are required and others are optional, although,
ideally all fields should be completed.

## Basic Data Series Information

The first table captures general information about the data provider and
the data series. A data series may provide centralised information about
one or many related datasets. The following information should be
supplied separately when a data set is
submitted.

| Field Name            | Required | Details                                                                            | Additional Notes                                                                                                  |
| --------------------- | -------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| title                 | Yes      | Short title identifying the data series                                            | E.g. “Mosquito Surveillance in Iowa”                                                                              |
| collection\_authority | Yes      | Name of collection authority                                                       | E.g. family name, given names; OR ‘Iowa State                                                                     |
| DOI                   | Optional | Digital Object Identifier (DOI)                                                    | If the data set was already published                                                                             |
| publication\_date     | Yes      | ISO 8601 date format (YYYY-MM-DD)                                                  | In case the data set was already published elsewhere, use the date of first publication.                          |
| description           | Yes      | A short description of the study / data set                                        | E.g. ‘Long term, fixed trapped, municipal surveillance of west Nile vector population in Colorado from 2000-2010” |
| URL                   | Yes      | web link to data set                                                               |                                                                                                                   |
| contact\_name         | Yes      | Name, person, authority, etc…. that may be contacted with inquiries about the data |                                                                                                                   |
| contact\_affiliation  | Optional | Author/contact affiliation                                                         |                                                                                                                   |
| email                 | Optional | Contact email                                                                      |                                                                                                                   |
| ORCID                 | Optional | ORCID code                                                                         | A digital identifier which provides                                                                               |
| keywords              | Optional | Keywords for web searches                                                          |                                                                                                                   |

The next table captures metadata for a study. A study should be regarded
as a set of data for one single species, at a given location over a
specific time period. The metadata should be used to capture information
like the general location of a study and particular methods or equipment
used to collect data on the study organism. Note that data entered into
these fields should be repeated for each time series row/observation. In
effect, the metadata helps to describe the time series
data.

## Metadata *(part of the VecDyn data collection template)*

| Field Name               | Required | Details                                                                                                            | Additional Notes                                                                                                                                                                                                  |
| ------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| data\_set\_name          | yes      | Short title identifying the data set                                                                               | The title should be related to the data series title and the study organism e.g. “Tiger Mosquito Surveillance in Iowa”                                                                                            |
| taxon\_name              | yes      | Classification of sample collected                                                                                 | Use the Catalogue of Life 2017 check-list to obtain the taxon name, only use names which are classed as ‘accepted’. See <http://www.catalogueoflife.org/annual-checklist/2017/>                                   |
| country                  | yes      | Country where study was conducted                                                                                  | Use the United Nations’s “Standard Country” names. See here <https://unstats.un.org/unsd/methodology/m49/>                                                                                                        |
| location\_description    | yes      | Description of study location                                                                                      | E.g.. town, county, state                                                                                                                                                                                         |
| location\_environment    | optional | General description about the location                                                                             | Where possible, please use the Environment Ontology search feature to characterize the location’s environment (see <http://www.environmentontology.org/Browse-EnvO>)                                              |
| study\_lat\_DD           | optional | Latitude of study area as a decimal degree                                                                         | General location of the study Ranges\[-90,+90\] for latitude (north-south measurement)                                                                                                                            |
| study\_long\_DD          | optional | Longitude of study area as a decimal degree                                                                        | Ranges \[-180,180\] for longitude (east-west measurement)                                                                                                                                                         |
| spatial\_accuracy        | optional | Spatial accuracy of the given coordinates                                                                          | Value between 0 - 6 indicating the accuracy of the location given. 0 = Unknown, 1 = \>100 km radius, 2 = 10 - \<100km, 3 = 1 - \<9km, 4 = 0.1 - 1km, 5 = 10 - 100m, 6 = accurate survey (incl. GPS) \<= 10m       |
| location\_extent         | optional | Indicating the size of the study site.                                                                             | A value between 1 - 4. Where available absolute size is recorded in the Area field. 1 = Region \>10 km radius, 2 = Local Area 1-10 km radius, 3 = Extended Site 0.1-1 km radius, 4 = Precise Site \<0.1 km radius |
| geo\_datum               | optional | Geodetic datum                                                                                                     | E.g.. WGS 84                                                                                                                                                                                                      |
| species\_id\_method      | Optional | Species Identification Method                                                                                      | A description of the methods species identification.                                                                                                                                                              |
| study\_design            | Optional | Study design methodology                                                                                           | Indicate if observational study i.e.prospective , retrospective, or experimental etc                                                                                                                              |
| sampling\_strategy       | Optional | Indicate the strategy used to select the sample                                                                    | E.g. simple random sampling, stratified, convenience sampling, cluster, sampling, census etc                                                                                                                      |
| sampling\_method         | Optional | Sampling apparatus e.g..trap type, observation method)                                                             | E.g. “CDC light trap w/ CO2”, “Prokopack backpack aspirator”, “Quadrat count”                                                                                                                                     |
| sampling\_protocol       | Optional | How entities were sampled                                                                                          | E.g. ‘Count’, ‘Count (millions)’, ‘Harvest’, ‘Index of abundance’, ‘Index of territories’, ‘Leaf area’, ‘Mean Count’, ‘Not Specified’, ‘Percent cover’ and ‘Sample’.                                              |
| measurement\_unit        | Optional | Unit of measurement                                                                                                | The entity observed. Entries could include, ‘individuals’, ‘adults’, ‘cells’, ‘egg masses’, and ‘pelts’                                                                                                           |
| sample\_collection\_area | Optional | The spatial extent (area or volume) of the sample                                                                  | If relevant (E.g.., when collection method is transect or quadrat), in units of area or volume, the spatial coverage of the sampling unit e.g. “100 m^2”, “1 liter”, “1 ha”, “10m^3”                              |
| value\_transform         | Optional | Note if the original values have been transformed – list details of the reference value of any data transformation | E.g..Base Year, Log, None, Not Specified, Proportion, Unknown, x 1000 lbs                                                                                                                                         |

In the following table, the next set of variables captures the
information required to produce a time-Series dataset. Each row should
represent a separate observation, at a particular point in time. Note
that any additional information about a sub sample can be added here too
e.g. point location of sample sites or sex of a
species.

## Time Series Data *(part of the VecDyn data collection template)*

| Field Name          | Required | Details                                                   | Additional Notes                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------- | -------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| sample\_start\_date | Optional | Start date: ISO 8601 date format (YYYY-MM-DD)             | Only required when the collector wants to sample populations within specific time frames e.g. between when a trap was set and when the sample was collected                                                                                                                                                                                                                                                               |
| sample\_start\_time | Optional | Start time: ISO 8601 time format (hh:mm:ss)               | Only required when the collector wants to sample populations within specific time frames e.g. time example: 15:53:00                                                                                                                                                                                                                                                                                                      |
| sample\_end\_date   | Yes      | Collection date:ISO 8601 time format (hh:mm:ss)           | The date the sample was collected. If collection occurs monthly use the first day of each month i.e. 2001-01-01, 2001-02-01. Date example: 2008-09-15                                                                                                                                                                                                                                                                     |
| sample\_end\_time   | Optional | Time of the sample collection:                            | ISO 8601 time format (hh:mm:ss)                                                                                                                                                                                                                                                                                                                                                                                           |
| value               | Yes      | The numerical amount or result from the sample collection | The population data from study                                                                                                                                                                                                                                                                                                                                                                                            |
| sample\_info        | Optional | Additional sample information                             | Should be used when more information is required to understand the experiment, for example experimental variables, sub-locations, etc.Could report general info regarding sample location. Some users may report wind speeds Examples: “Forest” vs “Field”, “Winter”vs “Summer”, “Inside” vs “Outside”, “200 meters above sea level”                                                                                      |
| sample\_lat\_DD     | Optional | Latitude of sample area as a decimal degree               | Specific location of the sample Ranges \[-90,+90\] for latitude (north-south measurement)                                                                                                                                                                                                                                                                                                                                 |
| sample\_long\_DD    | Optional | Longitude of sample area as a decimal degree              | Ranges \[-180,180\] for longitude (east-west measurement)                                                                                                                                                                                                                                                                                                                                                                 |
| sample\_name        | Optional | A human readable sample name                              | May exist solely for the benefit of the depositor in organizing their data, use their own internal naming conventions etc.Naming convention is not restricted, but any encoded metadata should be revealed in the other data fields. For example, you may name a sample named ‘Aphid1\_StickyTrap\_Jan4,’ but you will still have “Sticky Trap” listed in a Collection Method field, and “Jan 4, 2017” in the date field. |
| sample\_sex         | Optional | Information on the sex of the organism sampled            |                                                                                                                                                                                                                                                                                                                                                                                                                           |

# Data Standardization

## Standardizing Taxonomy

To standardise taxonomy, VecDyn includes the [The Catalogue of Life
database](http://www.catalogueoflife.org), which is the most
comprehensive and authoritative global index of species currently
available. Taxonomic data will be standarsied by curators upon the
addition of a dataset to the VecDyn database.

## Standardizing Geo Referencing

In order to standardise geographic information, the [the Global
Administrative Unit Layers (GAUL) 2014
databaset](http://www.fao.org/geonetwork/srv/en/metadata.show?id=12691)
has been incorporated into the VecDyn database. The GAUL database
systematises global administrative regions with a unified coding system
at country, first (e.g. departments) and second administrative levels
(e.g. districts). Each Administrative unit is assigned a unique ID and
is connected to a spatial polygon. Therefore data submitted to the
VecDyn database can berepresented spatially, as long as a minimal set of
information is provided by the submitter e.g. country, county, region,
state.

## Standardizing Environmental Descriptions

Environemtnal descriptors can be standardized using
[ENVO](http://environmentontology.org/Browse-EnvO). ENVO is an ontology
which represents knowledge about environments,environmental processes,
ecosystems, habitats, and related entities.

# Templates, Examples & Tutorials

[VecDyn
Template](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv).

[Build a VecDyn Template dataframe in R
Markdown](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd).

[Example data
set](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv)

[R markdown recipe: Clean a data set, transform it into the VecDyn
format and produce a time
series](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd)

# Issues, troubleshooting & suggestions

Any suggestions or todos with regards to the database (e.g. new columns,
schema modifications etc.) can be logged as [Issues on
GitHub](https://github.com/vectorbite/VectorBiteDataPlatform/issues).
Issues allow for discussions among multiple users, file attachments,
colour-coded labels etc.

## Known isses

The FAO’s GUAL data set has been restructured for VecDyn. A new column
was created which represents an individual ID for each admin unit. This
creates a few minor issues, since some region codes are not unique and
therefore, an additional ‘b’ has been added to the end of
each’ADM\_CODE’ which has been used in VecDyn as a ‘Primary
key’

| ADM\_CODE  | ADM2\_NAME                        | ADM1\_NAME   | ADM0\_NAME                  |
| ---------- | --------------------------------- | ------------ | --------------------------- |
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

# Miscellaneous

The `GPDD` directory also contains the documentation of the [**G**lobal
**P**opulation **D**ynamics
**D**atabase](http://www3.imperial.ac.uk/cpb/databases/gpdd), a
pre-existing database of population dynamics, hosted in Silwood Park,
Imperial College London since 1999. VecDyn aims to learn from both
GPDD’s success and potential shortcomings as it moves forward.
