## Submitting data

1. Download the latest templates by right clicking on the following links
    - [vecdyn data template](https://github.com/vectorbite/VectorBiteDataPlatform/blob/master/static/documentation/VecDyn/Template_and_Scripts/vecdyn_template%20.csv) and selecting ‘save.as’.
    - [vecdyn publication info template](https://github.com/vectorbite/VectorBiteDataPlatform/blob/master/static/documentation/VecDyn/Template_and_Scripts/vecdyn_publication_information.csv) and selecting ‘save.as’.
2. You can refer to the 'Field definitions section' to guide you through the data collection and compilation process.
3. To submit your dataset, upload and submit the dataset via the [upload page](https://www.vectorbyte.org/vecdyn/submit_vecdyn_data) on the VectorByTE web app.
4. We’ll contact you regarding the outcome of your submission once we have had a look at it.


## General information about the VecDyn template

VecDyn data is stored in two separate files, one dedicated for storing publication information,  one dedicated for storing time-series data and meta-data (data describing how the data was collected).  Data-sets come in many forms, you may receive a data-set which contains all relevant data in one file or one that is split into several files or sources i.e. publication information from a web page and time series data from a file.

You may find that you can complete each table partially and you end up with missing fields. You can refer to the 'Data collection models' section below which lists which fields are required.  If you have any doubts we can decide if the data-set is complete at a later date and even request information from the author if required.

## Templates

Note that all data frame fields are created in character format,
you'll need to convert them to the correct formats at a later stage.
You can use this data frame as a guide to help you convert your data-set to the VecDyn format.
You can either import data into into the data frames below or just rename the field names of the
data-set you are working on.  However,  you need to make sure all the columns are in the correct
order as below,  even if your data set is missing certain fields. In this case you need to create
them  and leave them blank.

## Create vecdyn template in R Markdown

```{r}
publication_information_template <-data.frame(title=character(),
                 cdataset_citation=character(),
                             publication_citation = character(),
                             description = character(),
                             url = character(),
                             contact_name=character(),
                             contact_affiliation=character(),
                             email=character(),
                             orcid=character(),
                             dataset_license=character(),
                             project_identifier=character(),
                             publication_status=character(),
                 stringsAsFactors=FALSE)
write.csv(publication_information_template, file = "vecdyn_publication_information.csv", row.names = FALSE)
```


```{r}
vecdyn_template  <- data.frame(title = character(),
                             taxon = character(),
                             location_description = character(),
                             study_collection_area = character(),
                             geo_datum = character(),
                             gps_obfuscation_info = character(),
                             species_id_method = character(),
                             study_design = character(),
                             sampling_strategy = character(),
                             sampling_method = character(),
                             sampling_protocol = character(),
                             measurement_unit = character(),
                             value_transform = character(),
                              sample_start_date = character(),
                             sample_start_time = character(),
                             sample_end_date =  character(),
                             sample_end_time = character(),
                             sample_value = character(),
                             sample_sex = character(),
                             sample_stage = character(),
                             sample_location = character(),
                             sample_collection_area = character(),
                             sample_lat_dd = character(),
                             sample_long_dd = character(),
                             sample_environment = character(),
                             additional_location_info = character(),
                             additional_sample_info = character(),
                             sample_name = character(),
                             stringsAsFactors=FALSE)
write.csv(vecdyn_template , file = "vecdyn_template .csv", row.names = FALSE)

```