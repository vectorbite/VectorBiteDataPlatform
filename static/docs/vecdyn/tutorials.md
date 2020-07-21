---
title: "Mapping existing data to Vecdyn Template in R markdown"
author: Matthew Watts
date: July 2020
output:
  html_document:
    keep_md: true
---




In this tutorial we will map an existing vector population data set to the VecDyn format. 

Please refer to the 'R for Data Science guide'(https://r4ds.had.co.nz/) for further information on some of the techniques we use here. 

Load the following packages (and install if required)


```r
library(tidyverse)
```

```
## -- Attaching packages ------------------------------------------------------------------------------------------ tidyverse 1.3.0 --
```

```
## v ggplot2 3.3.0     v purrr   0.3.4
## v tibble  3.0.1     v dplyr   0.8.5
## v tidyr   1.0.3     v stringr 1.4.0
## v readr   1.3.1     v forcats 0.5.0
```

```
## -- Conflicts --------------------------------------------------------------------------------------------- tidyverse_conflicts() --
## x dplyr::filter() masks stats::filter()
## x dplyr::lag()    masks stats::lag()
```

```r
library(readr)
library(lubridate)
```

```
## 
## Attaching package: 'lubridate'
```

```
## The following objects are masked from 'package:dplyr':
## 
##     intersect, setdiff, union
```

```
## The following objects are masked from 'package:base':
## 
##     date, intersect, setdiff, union
```

```r
library(plyr)
```

```
## ------------------------------------------------------------------------------
```

```
## You have loaded plyr after dplyr - this is likely to cause problems.
## If you need functions from both plyr and dplyr, please load plyr first, then dplyr:
## library(plyr); library(dplyr)
```

```
## ------------------------------------------------------------------------------
```

```
## 
## Attaching package: 'plyr'
```

```
## The following objects are masked from 'package:dplyr':
## 
##     arrange, count, desc, failwith, id, mutate, rename, summarise,
##     summarize
```

```
## The following object is masked from 'package:purrr':
## 
##     compact
```

You will need to create and fill out two templates. One containing all the publication information and one which will store the data. We'll start with the data template. 


Create the VecDyn data template / data-frame and name it.



```r
vecdyn_mcm_2012  <- data.frame(
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
                      sample_value = numeric(),
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

#write.csv(VecDyn_template, file = "VecDyn_template.csv", row.names = FALSE)
```

In this example, we will use a Manatee County Mosquito collection data-set. When importing data-sets, make sure you set 'stringsAsFactors=FALSE' to ensure R does not automatically convert strings to factors.


```r
Manatee_County_Mosquito_2012 <- read.csv(url("https://zenodo.org/record/1217702/files/VectorBase-2012-Manatee_County_Mosquito_Control_District_Florida_USA.csv?download=1"), stringsAsFactors=FALSE)
```

Inspect the data-frame.


```r
head(Manatee_County_Mosquito_2012)
```

```
##                 collection_ID               sample_ID collection_date_start
## 1 MCMCD_2012_collection_00001 MCMCD_2012_sample_00001            2012-03-21
## 2 MCMCD_2012_collection_00001 MCMCD_2012_sample_00002            2012-03-21
## 3 MCMCD_2012_collection_00003 MCMCD_2012_sample_00003            2012-03-21
## 4 MCMCD_2012_collection_00005 MCMCD_2012_sample_00004            2012-03-21
## 5 MCMCD_2012_collection_00007 MCMCD_2012_sample_00005            2012-03-21
## 6 MCMCD_2012_collection_00007 MCMCD_2012_sample_00006            2012-03-21
##   collection_date_end            trap_id  GPS_lat   GPS_lon        location
## 1          2012-03-22 2012-03-21_B4HS_G1 27.51632 -82.53773 Highland Shores
## 2          2012-03-22 2012-03-21_B4HS_G1 27.51632 -82.53773 Highland Shores
## 3          2012-03-22 2012-03-21_B4J_G1J 27.55402 -82.54548           Carrs
## 4          2012-03-22   2012-03-21_D1_C3 27.48887 -82.59214      Manatee HS
## 5          2012-03-22   2012-03-21_D3_D8 27.43945 -82.54893         Mullins
## 6          2012-03-22   2012-03-21_D3_D8 27.43945 -82.54893         Mullins
##    location_ADM2 location_ADM1         location_country trap_type attractant
## 1 Manatee County       Florida United States of America CDC_LIGHT  LIGHT,CO2
## 2 Manatee County       Florida United States of America CDC_LIGHT  LIGHT,CO2
## 3 Manatee County       Florida United States of America CDC_LIGHT  LIGHT,CO2
## 4 Manatee County       Florida United States of America CDC_LIGHT  LIGHT,CO2
## 5 Manatee County       Florida United States of America CDC_LIGHT  LIGHT,CO2
## 6 Manatee County       Florida United States of America CDC_LIGHT  LIGHT,CO2
##   trap_number trap_duration                   species identification_method
## 1           1             1          Culex salinarius        SPECIES_MORPHO
## 2           1             1           Culex coronator        SPECIES_MORPHO
## 3           1             1         Culex nigripalpus        SPECIES_MORPHO
## 4           1             1                     BLANK        SPECIES_MORPHO
## 5           1             1         Culex nigripalpus        SPECIES_MORPHO
## 6           1             1 Anopheles quadrimaculatus        SPECIES_MORPHO
##   developmental_stage    sex sample_count
## 1               adult female            2
## 2               adult female            3
## 3               adult female            3
## 4               adult female            0
## 5               adult female            1
## 6               adult female            2
```

All geo-names should be presented in one field. The Manatee_County data set's study location is characterized using 3 fields, we need to combine this information into one field.  We can use a tidyr function called "unite" to do this. 


```r
Manatee_County_Mosquito_2012 <-
  Manatee_County_Mosquito_2012 %>%
  tidyr::unite("location_description", c("location_ADM2","location_ADM1", "location_country"), sep = ",")
```

Extract all the data from the Manatee_County_Mosquito_2012 to individual vectors. Each new vector name represents a name in the VecDyn template


```r
taxon <- Manatee_County_Mosquito_2012$species

sample_value <- Manatee_County_Mosquito_2012$sample_count

sample_sex <- Manatee_County_Mosquito_2012$sex

sample_stage <-  Manatee_County_Mosquito_2012$developmental_stage

sample_start_date <- Manatee_County_Mosquito_2012$collection_date_start

sample_end_date <- Manatee_County_Mosquito_2012$collection_date_end

sample_lat_dd <- Manatee_County_Mosquito_2012$GPS_lat

sample_long_dd <- Manatee_County_Mosquito_2012$GPS_lon

sample_location <- Manatee_County_Mosquito_2012$location

location_description <- Manatee_County_Mosquito_2012$location_description

sampling_method <- Manatee_County_Mosquito_2012$attractant

sampling_protocol <- Manatee_County_Mosquito_2012$trap_type

species_id_method <- Manatee_County_Mosquito_2012$identification_method

sample_name <-  Manatee_County_Mosquito_2012$trap_id
```

Bind the extracted values together creating and create a new data-frame.  We then bind the new data-frame with the vecdyn_mcm_2012 template.


```r
a <- cbind(taxon, sample_value, sample_sex, sample_stage, sample_start_date, sample_end_date, sample_lat_dd, sample_long_dd, sample_location, location_description, sampling_method, sampling_protocol, species_id_method, sample_name)

a <- data.frame(a, stringsAsFactors=FALSE)

vecdyn_mcm_2012 <- rbind.fill(vecdyn_mcm_2012, a)
```

You should check to see if the number of observations in the newly created vecdyn_mcm_2012 data frame match the number of observations in the original manatee county data frame.

All VecDyn dates need to be formatted as Y-m-d, in this example the dates are already in the correct format. 


```r
vecdyn_mcm_2012 <-
  vecdyn_mcm_2012 %>%
  dplyr::mutate(sample_end_date = as.Date(as.character(sample_end_date, format = "%Y/%m/%d"))) %>%
  dplyr::mutate(sample_start_date = as.Date(as.character(sample_start_date, format = "%Y/%m/%d"))) %>%
  # We also convert the sample_value field to numeric so we can create a time series in the next step
  dplyr::mutate(sample_value = as.numeric(sample_value))
```

We can test our new data frame set against the original data frame to see if they produce the same results.


```r
vecdyn_mcm_2012  %>%
  dplyr::select(sample_value, sample_end_date) %>%
  dplyr::group_by(sample_end_date) %>%
  ggplot(aes(sample_end_date, sample_value)) + geom_line() +
  scale_x_date(date_breaks = "1 month", date_minor_breaks = "1 week",
             date_labels = "%B")
```

![](vecdyn-tutorial-mapping-data_files/figure-html/unnamed-chunk-9-1.png)<!-- -->


```r
Manatee_County_Mosquito_2012  %>%
  dplyr::select(sample_count, collection_date_end) %>%
  plyr::mutate(collection_date_end = as.Date(as.character(collection_date_end, format = "%Y/%m/%d"))) %>%
  dplyr::mutate(sample_count = as.numeric(sample_count)) %>%
  ggplot(aes(collection_date_end, sample_count)) + geom_line() +
  scale_x_date(date_breaks = "1 month", date_minor_breaks = "1 week",
             date_labels = "%B")
```

![](vecdyn-tutorial-mapping-data_files/figure-html/unnamed-chunk-10-1.png)<!-- -->

Finally write the data set to CSV, set all missing value to blank ""


```r
write_csv(vecdyn_mcm_2012, "vecdyn_mcm_2012.csv", na = "")
```

Next complete the publication information, this can be submitted as a CV or using the online web form when you submit the main data-set. The publication information for our example data-set here is found here https://zenodo.org/record/1217702#.Xvs89ygza70. Note that this information should only be recorded as one line (or row) for each field. 


```r
rm(list=setdiff(ls(), c("vecdyn_mcm_2012")))
```



```r
vecdyn_publication_info_mcm_2012  <- data.frame(title=character(), # name of collection title
                 collection_author=character(), 
                 dataset_doi=character(),
                 publication_doi = character(),
                 description = character(),
                 url = character(),
                 contact_name=character(),
                 contact_affiliation=character(),
                 email=character(),
                 orcid=character(),
                 dataset_license=character(),
                 stringsAsFactors=FALSE)
```

Next fill the appropriate fields


```r
title <- "Manatee County Mosquito Control District entomological monitoring 2012"
collection_author <- "Joe Bloggs"
dataset_doi <- "10.5281/zenodo.1217702"
description <- "Mosquito surveillance from the Manatee County Mosquito Control District Vector Surveillance program to survey mosquito population"
url <- "https://zenodo.org/record/1217702#.XwbwICgzZPZ"
contact_name <- "Joe Bloggs"
contact_affiliation <- "Manatee County Mosquito Control District"
email <- "Joe Bloggs@joebloggs.com"
dataset_license=character <- "open"
```

Bind them to the main publication info data frame


```r
a <- cbind(title, collection_author, dataset_doi, description, url, contact_name, contact_affiliation, email, dataset_license)
a <- data.frame(a, stringsAsFactors=FALSE)
vecdyn_publication_info_mcm_2012 <- rbind.fill(vecdyn_publication_info_mcm_2012, a)

# clear environment

rm(list=setdiff(ls(), c("vecdyn_mcm_2012", "vecdyn_publication_info_mcm_2012")))
```

Write as a CSV


```r
write.csv(vecdyn_publication_info_mcm_2012, file = "vecdyn_publication_info_mcm_2012.csv", row.names = FALSE)
```







