Global **Vec**tor Population **Dyn**amics Database (VecDyn) Submission Documentation
====================================================================================

Requirements for Data sets not in VecDyn Format
-----------------------------------------------

If you are submitting a dataset in its current format, Please make sure
all the following fields are contained in your dataset.

<table>
<colgroup>
<col style="width: 18%" />
<col style="width: 8%" />
<col style="width: 51%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th>Field</th>
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
<td>The title should be related to the data series title and the study organism e.g. Tiger Mosquito Surveillance in Iowa</td>
</tr>
<tr class="even">
<td>taxon_name/s</td>
<td>yes</td>
<td>Classification of sample collected - could</td>
<td></td>
</tr>
<tr class="odd">
<td>countries</td>
<td>yes</td>
<td>Country where study was conducted</td>
<td>Use the United Nation’s “Standard Country” names. See here <a href="https://unstats.un.org/unsd/methodology/m49/" class="uri">https://unstats.un.org/unsd/methodology/m49/</a></td>
</tr>
<tr class="even">
<td>Description of locations</td>
<td>Yes</td>
<td>Description of study locations in order main unit to subdivisions</td>
<td>E.g.. town, county, state</td>
</tr>
<tr class="odd">
<td>sample_end_date</td>
<td>Yes</td>
<td>Collection date</td>
<td>The date the sample was collected.</td>
</tr>
<tr class="even">
<td>value</td>
<td>Yes</td>
<td>The numerical amount or result from the sample collection</td>
<td>The population data from study</td>
</tr>
<tr class="odd">
<td>Measurement unit</td>
<td>Yes</td>
<td>The entity observed. Entries could include, ‘individuals’, ‘adults’, ‘cells’, ‘egg masses’, and ‘pelts’</td>
</tr>
</tbody>
</table>

VecDyn Template Field descriptions
----------------------------------

<table style="width:100%;">
<colgroup>
<col style="width: 18%" />
<col style="width: 8%" />
<col style="width: 51%" />
<col style="width: 21%" />
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
<td>The title should be related to the data series title and the study organism e.g. Tiger Mosquito Surveillance in Iowa</td>
</tr>
<tr class="even">
<td>taxon_name</td>
<td>yes</td>
<td>Classification of the species colleced</td>
<td>Could be one or many species</td>
</tr>
<tr class="odd">
<td>country</td>
<td>yes</td>
<td>Country or countries where study was conducted</td>
<td></td>
</tr>
<tr class="even">
<td>location_description</td>
<td>yes</td>
<td>Description of study location/s</td>
<td>E.g.. town, county, state</td>
</tr>
<tr class="odd">
<td>location_environment</td>
<td>optional</td>
<td>General description about the location</td>
<td>Where possible, please use the Environment Ontology search feature to characterize the location environment</td>
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
<td>E.g. CDC light trap w/ CO2, Prokopack backpack aspirator, Quadrat countat</td>
</tr>
<tr class="odd">
<td>sampling_protocol</td>
<td>Optional</td>
<td>How entities were sampled</td>
<td>E.g. Count, Count (millions), Harvest, Index of abundance, Index of territories, Leaf area, Mean Count, Not Specified, Percent cover and Sample.</td>
</tr>
<tr class="even">
<td>measurement_unit</td>
<td>Optional</td>
<td>Unit of measurement</td>
<td>The entity observed. Entries could include, ‘individuals’, adults, cells, egg masses, and pelts</td>
</tr>
<tr class="odd">
<td>sample_collection_area</td>
<td>Optional</td>
<td>The spatial extent (area or volume) of the sample</td>
<td>If relevant (E.g.., when collection method is transect or quadrat), in units of area or volume, the spatial coverage of the sampling unit e.g. 100 m^2, 1 liter, 1 ha, 10m^3</td>
</tr>
<tr class="even">
<td>value_transform</td>
<td>Optional</td>
<td>Note if the original values have been transformed list details of the reference value of any data transformation</td>
<td>E.g..Base Year, Log, None, Not Specified, Proportion, Unknown, x 1000 lbs</td>
</tr>
<tr class="odd">
<td>sample_start_date</td>
<td>Optional</td>
<td>Start date</td>
<td>Only required when the collector wants to sample populations within specific time frames e.g. between when a trap was set and when the sample was collected</td>
</tr>
<tr class="even">
<td>sample_start_time</td>
<td>Optional</td>
<td>Start time</td>
<td>Only required when the collector wants to sample populations within specific time frames e.g. time example: 15:53:00</td>
</tr>
<tr class="odd">
<td>sample_end_date</td>
<td>Yes</td>
<td>Collection date</td>
<td>The date the sample was collected. If collection occurs monthly use the first day of each month i.e. 2001-01-01, 2001-02-01. Date example: 2008-09-15</td>
</tr>
<tr class="even">
<td>sample_end_time</td>
<td>Optional</td>
<td>Time of the sample collection:</td>
<td></td>
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
<td>Should be used when more information is required to understand the experiment, for example experimental variables, sub-locations, etc.Could report general info regarding sample location. Some users may report wind speeds Examples: Forest vs Field, Winter vs Summer, Inside vs Outside, 200 meters above sea level</td>
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
<td>May exist solely for the benefit of the depositor in organizing their data, use their own internal naming conventions etc.Naming convention is not restricted, but any encoded metadata should be revealed in the other data fields. For example, you may name a sample named Aphid1_StickyTrap_Jan4, but you will still have Sticky Trap listed in a Collection Method field, and Jan 4, 2017 in the date field.</td>
</tr>
<tr class="even">
<td>sample_sex</td>
<td>Optional</td>
<td>Information on the sex of the organism sampled</td>
<td></td>
</tr>
</tbody>
</table>
