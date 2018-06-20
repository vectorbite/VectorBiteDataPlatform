-   [Global **Vec**tor Population **Dyn**amics Database (VecDyn): User
    Data Submission
    Guide](#global-vector-population-dynamics-database-vecdyn-user-data-submission-guide)
    -   [What is VecDyn?](#what-is-vecdyn)
    -   [Submitting data](#submitting-data)
        -   [VecDyn template field
            descriptions](#vecdyn-template-field-descriptions)
        -   [Requirements for data sets not in the VecDyn
            format](#requirements-for-data-sets-not-in-the-vecdyn-format)
    -   [Templates, Examples & Tutorials](#templates-examples-tutorials)
    -   [Issues, troubleshooting &
        suggestions](#issues-troubleshooting-suggestions)

Global **Vec**tor Population **Dyn**amics Database (VecDyn): User Data Submission Guide
=======================================================================================

Welcome to VectorBiTE’s VecDyn database submission guidelines. This
document provides details and instructions on accessing and submitting
data. You can also access data collection templates and examples that
will help you to prepare data for submission.

What is VecDyn?
---------------

VecDyn is a global database for spatially- and temporally- explicit
presence-absence and abundance data. We accept and distribute data for
both animal and plant disease vectors.

Submitting data
---------------

*If you want to submit a dataset that is not in the vecdyn format,
please follow [Requirements for data sets not in the VecDyn
format](#requirements-for-data-sets-not-in-the-vecdyn-format). Otherwise
please read below*

1.  Download the latest template by right clicking on the following
    [link](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv).and
    selecting ‘save.as’.  
    A completed [example data set can be found
    here](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv).
    This will help you to understand how to compile data in the VecDyn
    template format. You can also access an example [R Markdown
    recipe](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd)
    that provides an example of converting an existing data set into a
    VecDyn formatted dataset. Notice that all files are in plain text
    e.g. ‘.csv’ format, and not in Excel format or similar. This
    facilitates text parsing by scripts, prevents data loss/corruption,
    and allows for detailed comparisons of changes via version control
    systems.

2.  You can refer to the [VecDyn template field
    descriptions](#vecdyn-template-field-descriptions) to guide you
    through the data collection and compilation process.

3.  To submit your dataset, upload and submit the dataset via the
    [upload page](http://vectorbyte.org/default/submit_data) on the
    VectorBiTE web app.

4.  We’ll contact you regarding the outcome of your submission once
    we’ve had a look at it.

### VecDyn template field descriptions

<table>
<colgroup>
<col style="width: 18%" />
<col style="width: 8%" />
<col style="width: 51%" />
<col style="width: 20%" />
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
<td>Yes</td>
<td>Short title identifying the data set</td>
<td>The title should be related to the collector name and the study organism e.g. Tiger Mosquito Surveillance in Iowa</td>
</tr>
<tr class="even">
<td>taxon_name</td>
<td>Yes</td>
<td>Classification of the species collected</td>
<td>Could be one or many species</td>
</tr>
<tr class="odd">
<td>country</td>
<td>Yes</td>
<td>Country or countries where study was conducted</td>
<td></td>
</tr>
<tr class="even">
<td>location _description</td>
<td>Yes</td>
<td>Description of study locations in order of largest to smallest subdivision</td>
<td>E.g. state, county, town</td>
</tr>
<tr class="odd">
<td>location_environment</td>
<td>Optional</td>
<td>General description about the location</td>
<td></td>
</tr>
<tr class="even">
<td>study_lat_DD</td>
<td>Optional</td>
<td>Latitude of study area as a decimal degree</td>
<td>General location of the study Ranges [-90,+90] for latitude (north-south measurement)</td>
</tr>
<tr class="odd">
<td>study_long_DD</td>
<td>Optional</td>
<td>Longitude of study area as a decimal degree</td>
<td>Ranges [-180,180] for longitude (east-west measurement)</td>
</tr>
<tr class="even">
<td>spatial_accuracy</td>
<td>Optional</td>
<td>Spatial accuracy of the given coordinates</td>
<td>Value between 0 - 6 indicating the accuracy of the location given. 0 = Unknown, 1 = &gt;100 km radius, 2 = 10 - &lt;100km, 3 = 1 - &lt;9km, 4 = 0.1 - 1km, 5 = 10 - 100m, 6 = accurate survey (incl. GPS) &lt;= 10m</td>
</tr>
<tr class="odd">
<td>location_extent</td>
<td>Optional</td>
<td>Indicate the size of the study site.</td>
<td>A value between 1 - 4. Where available absolute size is recorded in the Area field. 1 = Region &gt;10 km radius, 2 = Local Area 1-10 km radius, 3 = Extended Site 0.1-1 km radius, 4 = Precise Site &lt;0.1 km radius</td>
</tr>
<tr class="even">
<td>geo_datum</td>
<td>Optional</td>
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
<td>E.g. CDC light trap w/ CO2, Prokopack backpack aspirator, Quadrat countat</td>
</tr>
<tr class="odd">
<td>Measurement unit</td>
<td>Yes</td>
<td>What is the unit of measurement</td>
<td>E.g. ‘number of individuals’, ‘presence/absence’, ‘Presence only’, ‘proportion’, Percent cover</td>
</tr>
<tr class="even">
<td>sample_collection_area</td>
<td>Optional</td>
<td>The spatial extent (area or volume) of the sample</td>
<td>If relevant (E.g.., when collection method is transect or quadrat), in units of area or volume, the spatial coverage of the sampling unit e.g. 100 m^2, 1 liter, 1 ha, 10m^3</td>
</tr>
<tr class="odd">
<td>value_transform</td>
<td>Optional</td>
<td>Note if the original values have been transformed list details of the reference value of any data transformation</td>
<td>E.g..Base Year, Log, None, Not Specified, Proportion, Unknown, x 1000 lbs</td>
</tr>
<tr class="even">
<td>sample_start_date</td>
<td>Optional</td>
<td>Start date</td>
<td>Only required when the collector wants to sample populations within specific time frames e.g. between when a trap was set and when the sample was collected</td>
</tr>
<tr class="odd">
<td>sample_start_time</td>
<td>Optional</td>
<td>Start time</td>
<td>Only required when the collector wants to sample populations within specific time frames e.g. time example: 15:53:00</td>
</tr>
<tr class="even">
<td>sample_end_date</td>
<td>Yes</td>
<td>Collection date</td>
<td>The date the sample was collected. If collection occurs monthly use the first day of each month i.e. 2001-01-01, 2001-02-01. Date example: 2008-09-15</td>
</tr>
<tr class="odd">
<td>sample_end_time</td>
<td>Optional</td>
<td>Time of the sample collection:</td>
<td></td>
</tr>
<tr class="even">
<td>value</td>
<td>Yes</td>
<td>The numerical amount or result from the sample collection</td>
<td>The population data from study</td>
</tr>
<tr class="odd">
<td>sample_info</td>
<td>Optional</td>
<td>Additional sample information</td>
<td>Should be used when more information is required to understand the experiment, for example experimental variables, sub-locations, etc.Could report general info regarding sample location. Some users may report wind speeds Examples: Forest vs Field, Winter vs Summer, Inside vs Outside, 200 meters above sea level</td>
</tr>
<tr class="even">
<td>sample_lat_DD</td>
<td>Optional</td>
<td>Latitude of sample area as a decimal degree</td>
<td>Specific location of the sample Ranges [-90,+90] for latitude (north-south measurement)</td>
</tr>
<tr class="odd">
<td>sample_long_DD</td>
<td>Optional</td>
<td>Longitude of sample area as a decimal degree</td>
<td>Ranges [-180,180] for longitude (east-west measurement)</td>
</tr>
<tr class="even">
<td>sample_name</td>
<td>Optional</td>
<td>A human readable sample name</td>
<td>May exist solely for the benefit of the depositor in organizing their data, use their own internal naming conventions etc.Naming convention is not restricted, but any encoded metadata should be revealed in the other data fields. For example, you may name a sample named Aphid1_StickyTrap_Jan4, but you will still have Sticky Trap listed in a Collection Method field, and Jan 4, 2017 in the date field.</td>
</tr>
<tr class="odd">
<td>sample_sex</td>
<td>Optional</td>
<td>Information on the sex of the organism sampled</td>
<td></td>
</tr>
<tr class="even">
<td>sample_life_stage</td>
<td>Optional</td>
<td>Information on the life stage of the organism sampled</td>
<td>E.g adult, egg, larva, pupa</td>
</tr>
</tbody>
</table>

### Requirements for data sets not in the VecDyn format

*If you are submitting a dataset not in the VecDyn format, please make
sure you supply the following information.*

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 60%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th>Field</th>
<th>Details</th>
<th>Additional Notes</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Data set name</td>
<td>Short title identifying the data set</td>
<td>E.g. Mosquito Surveillance in Iowa</td>
</tr>
<tr class="even">
<td>Taxon name/s</td>
<td>Classification of samples collected</td>
<td></td>
</tr>
<tr class="odd">
<td>Country/countries</td>
<td>Country or countries where study was conducted</td>
<td></td>
</tr>
<tr class="even">
<td>Description of locations</td>
<td>Description of study locations in order of largest to smallest subdivision</td>
<td>E.g. state, county, town</td>
</tr>
<tr class="odd">
<td>Sample end date &amp; time</td>
<td>The date and time a sample was collected</td>
<td>Time is optional</td>
</tr>
<tr class="even">
<td>Value</td>
<td>The numerical amount or result from the sample collection</td>
<td></td>
</tr>
<tr class="odd">
<td>Measurement unit</td>
<td>What is the unit of measurement</td>
<td>E.g. ‘number of individuals’, ‘presence/absence’, ‘Presence only’, ‘proportion’, Percent cover</td>
</tr>
</tbody>
</table>

Templates, Examples & Tutorials
-------------------------------

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
-------------------------------------

Any suggestions or todos with regards to the database (e.g. new columns,
schema modifications etc.) can be logged as [Issues on
GitHub](https://github.com/vectorbite/VectorBiteDataPlatform/issues).
Issues allow for discussions among multiple users, file attachments,
colour-coded labels etc.
