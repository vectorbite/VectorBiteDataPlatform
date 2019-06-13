
# TODO -  Data Management (curators only)

# Mapping Data to VecDyn Template format

Most population abundance and presence absence data will come from various government or research institutions in various table formats, whoever it may also come from many sources publication. 

*To prepare a dataset for the VecDyn database, follow the subsequent guidelines*

1. Download the latest template by right clicking on the following [link](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Template%26Scripts/VecDyn_template.csv) and selecting ‘save.as’.   A completed [example data set can be found here](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv). This will help you to understand how to compile data in the VecDyn template format. You can also access an example [R Markdown recipe](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/ManateeCountryMosquitoMonitoring.Rmd) that provides an example of converting an existing data set into a VecDyn formatted dataset.
2. You can refer to the [VecDyn Data Collection Specifications](#vecdyn-data-collection-specifications) to guide you through the data collection and compilation process.

*Notice that all files are in plain text e.g. ‘.csv’ format, and not in Excel format or similar. This facilitates text parsing by scripts, prevents data loss/corruption, and allows for detailed comparisons of changes via version control systems.

For testing purposes (*temporary*) first download the [example data set](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/Documentation/VecDyn/Examples/ManateeCountyMosquitoMonitoring/vecdyn_manatee_county_aedes_aegypti.csv) to try out the process.

Log on and go to the and go to the [VectorBiTE web app](http://www.vectorbyte.org) and go to ‘My collections’. This will
only work if you have been granted access rights.

*Note that the data upload facility (temporary) is only set up to process one dataset at a time, one data set compromises of one species and one main umbrella geographical location.*

### Adding data to the database (Curators only)

This process will only work if all entries are mapped to the VecDyn template, the file also needs to be submitted in CSV format.

Once logged into the VectorBiTE web application, in the navigation bar click on '**Management**', then '**Manage VecDyn Datasets**'. Next click on **‘Register New Dataset’**. 

Fill in the publication information table. Information captured in this table describes general meta data relating to the dataset i.e. title, DOI, collection author, copyright information and so on. If it is the first time of submitting a dataset for a particular collection author, then click on 'Add new next to ' the relevant field then insert and submit the new collection author details in the pop up box. 

You'll now see an entry in the table for the data set you have just registered.  You can now add a dataset to this entry (upload a CSV).  Click on ‘Add new data set to collection on the particular row of the dataset. 

Next select a taxon, it is best to search using the first box first. When you have found the taxon you are after. Hit the ‘select’ button on the aligning row.

Next select a geographical location, this either needs to be country or an ADM1 (e.g. State) or ADM2 (county) administrative subdivision. Again, hit the ‘select’ button on the row of your choice.

Next submit all the study data (metadata) and click on submit once you have completed the page.

Next you need to upload the complete csv. This will only upload fields related to the time series (sample data)

Once completed, you’ll be taken the final page where you can can verify if all the sample data is correct. If it is, click on ‘finish’ button.

However, if there is a problem you can delete or edit each entry. To delete all the entries hit ‘select’ all and scroll down to the bottom of the page and click ‘delete selected’ 

Note that you can also edit every part of your data after it has been submitted with the exception of taxon names and place names.

Restricted Data


