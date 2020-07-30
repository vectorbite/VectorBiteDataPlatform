## Submitting data

1. Download the latest templates by right clicking on the following links

    - [vecdyn data template](https://raw.githubusercontent.com/vectorbite/VectorBiteDataPlatform/master/static/additional_files/Template_and_Scripts/vecdyn_template .csv' ) and selecting ‘save.as’.
    
2. You can refer to the [field definitions section](https://vectorbitedataplatform.readthedocs.io/en/latest/vecdyn/field_definitions/) to guide you through the data collection and compilation process.

3. To submit your data-set, upload and submit the data-set via the [upload page](https://www.vectorbyte.org/vecdyn/submit_vecdyn_data) on the VectorByTE web app.

4. In order to submit a data-set to VectorByte it must first pass through the validator to check that it is canonical (as defined by the entries in the [field definitions section](https://vectorbitedataplatform.readthedocs.io/en/latest/vecdyn/field_definitions/) ). See validator section below for more information. The validator should run relatively quickly, but validation time is dependent on the size of the data-set. Thus if you have uploaded a data-set of a few thousand rows, it may be worth taking a few minutes to go and get a coffee whilst the validation runs.

5. Once the data-set has passed validation it will be submitted to the VectorByte team for upload. Once you have done this, you have no direct access to the data any more. However, if you do make a mistake, do just email the team and they should be able to identify and delete the offending data-set before upload.

    **Important**: Please make a note of the **date** and **time** that you uploaded the data-set which you want discarded. This will make it a lot easier for the team to identify which data-set is yours.

6. We’ll contact you one your data-set has been added to the database.

### CSV format

Data should be submitted in the following CSV format:

- All entries are double quoted  (" ")

- Missing values are set to empty  ("")

- File encoding is set to "UTF-8"

## General submission guidelines. 

You may find that you can complete each table partially and you end up with missing fields. You can refer to the 'Data collection models' section below which lists which fields are required.  If you have any doubts please try submitting the data, if it does pass validation you will receive a report informing you which required fields are missing. If you have any other doubts please email the VectorBite team. 



## Create VecDyn template in R Markdown


```{r}
vecdyn_template  <- data.frame(taxon = character(),
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

## Validator

Vecdyn has a validation tool built in to allow a digitiser to quickly check whether their candidate dataset for upload is in the correct format. In order to submit a dataset to VectorByte it must first pass through the validator to check that it is canonical (as defined by the entries in the [field definitions](field_definitions.md) section.)

The validator has a simple workflow as follows:

## ![vecdyn_validator](/home/matt/NewWeb2py/web2py/applications/VectorBiteDataPlatform/static/docs/vecdyn/images/vecdyn_validator_big.png)Validation report 

If the validation fails, you will be returned a report in-line within the validator page:

Here is an example report from a test data-set which failed, the CSV is not formatted correctly and there are data type errors.

```
            ========================
            Vecdyn Validation Report
            ========================
            Satus = "Failed"
            =================================================================
            Please fix the problems below before resubmitting the dataset.
            =================================================================
            
            Problems
            ========
            
dataset_check - bad header
--------------------------
:missing: set([])
:record: ('taxon', 'location_description', 'study_collection_area', 'geo_datum', 'gps_obfuscation_info', 'species_id_method', 'study_design', 'sampling_strategy', 'sampling_method', 'sampling_protocol', 'measurement_unit', 'value_transform', 'sample_start_date', 'sample_start_time', 'sample_end_date', 'sample_end_time', 'sample_value', 'sample_sex', 'sample_stage', 'sample_location', 'sample_collection_area', 'sample_lat_dd', 'sample_long_dd', 'sample_environment', 'additional_location_info', 'additional_sample_info', 'sample_name', '', '', '')
:row: 1
:unexpected: set([''])

sample_end_date error - entry must be in date format: %Y-%m-%d
--------------------------------------------------------------
:column: 15
:field: sample_end_date
:record: ('Coquillettidia perturbans', 'Manatee County,Florida,United States of America', '', '', '', 'SPECIES_MORPHO', '', '', 'LIGHT,CO2', 'CDC_LIGHT', '', '', '2012-03-21', '', '2012-03-2jjkjkjk2', '', '1', 'female', 'adult', 'Tallevast', '', '27.4266', '-82.52471', '', '', '', '2012-03-21_D3T_F1T')
:row: 14
:value: 2012-03-2jjkjkjk2

sample_end_date error - entry must be in date format: %Y-%m-%d
--------------------------------------------------------------
:column: 15
:field: sample_end_date
:record: ('Coquillettidia perturbans', 'Manatee County,Florida,United States of America', '', '', '', 'SPECIES_MORPHO', '', '', 'LIGHT,CO2', 'CDC_LIGHT', '', '', '2012-05-07', '', 'kjhkhkhjkh', '', '2', 'female', 'adult', 'Braden River Park', '', '27.44893', '-82.498664', '', '', '', '2012-05-07_D2BP2_F2BP')
:row: 134
:value: kjhkhkhjkh

sample_value error - entry must be numeric
------------------------------------------
:column: 17
:field: sample_value
:record: ('Anopheles crucians', 'Manatee County,Florida,United States of America', '', '', '', 'SPECIES_MORPHO', '', '', 'LIGHT,CO2', 'CDC_LIGHT', '', '', '2012-05-22', '', '2012-05-23', '', '51jnjkh', 'female', 'adult', 'Port', '', '27.640483', '-82.552667', '', '', '', '2012-05-22_B1P_G2P')
:row: 228
:value: 51jnjkh

            Summary
            =======
            Found 4 problems in total.
            :dataset_check: 1
:sample_end_date error: 2
:sample_value error: 1


```

