# Mapping Data to Vecdyn Template in R Tutorial (Rmarkdown)


Your challenge will be to clean-up and process data-sets, mapping them to the vecdyn template. Try to map what you can, you might find that some data-sets provide more information than what is required for the vecdyn database (e.g. the GPDD data has many additional fields we do not need).  Work with R notebooks or r studio markdown so you can save all your code and we can go back to it at a later date and re-edit if necessary.

You'll probably need to use a number of packages and techniques to achieve your goal. You should refer to the 'R for Data Science guide'(https://r4ds.had.co.nz/) or materials you have been provided by Imperial.

You can find the R code which will help you build a vecdyn template under the 'Template' section below.

# Mapping To The Vecdyn Template Example

Load the following packages (and install if required)

```{r}
# install.packages("tidyverse")
# install.packages("readr")
# install.packages("plyr")
# install.packages("scales")
library(tidyverse)
library(readr)
library(plyr)
library(scales)
library(lubridate)

```

Load up the VecDyn template / data-frame and name it.

```{r}
vecdyn_mcm_2012  <- data.frame(title = character(),
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

Import the Manatee County Mosquito Data Set (2012). When importing data-sets, make sure you set '=FALSE' to ensure R doesnt apply any unwanted formatting to the data-frame.

```{r}
Manatee_County_Mosquito_2012_download <- read.csv(url("https://zenodo.org/record/1217702/files/VectorBase-2012-Manatee_County_Mosquito_Control_District_Florida_USA.csv?download=1"), stringsAsFactors=FALSE)

Manatee_County_Mosquito_2012 <- Manatee_County_Mosquito_2012_download
```

Check the data-frame to see if everything went to plan.

In this data-set, trap_id, gps_lat, gps_long & location all vary together, in this data-set this represents trap location.  Location_ADM2, location_ADM1, location_country represent the general study location.

```{r}
head(Manatee_County_Mosquito_2012)
```

One way to map the Manatee_County_Mosquito_2012 data-set to a vecdyn template is to extract values from the original data-frame and add them to the relevant fields in the vecdyn data frame.

Firstly though, some of the general geo-information about the study location is presented in 3 fields, we need to get this into 1 field.  We can use a tidyr package called unite these 3 fields into one.

```{r}
Manatee_County_Mosquito_2012 <-
  Manatee_County_Mosquito_2012 %>%
  tidyr::unite("location_description", c("location_ADM2","location_ADM1", "location_country"), sep = ",")

```

We can drop (not include) some of the fields that we do not require from the manatee county data set i.e. collection_ID (recreated in vecdyn db), sample_ID (recreated in vecdyn db), trap_number (no useful info) & trap_duration (specified by collection start and end dates)

Below, we extract values from Manatee_County_Mosquito_2012 data-frame

```{r}

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

Next we bind all the extracted values together creating a data-frame, we then bind the newly created data-frame with the vecdyn_mcm_2012 template we created at the beginning.

```{r}

a <- cbind(taxon, sample_value, sample_sex, sample_stage, sample_start_date, sample_end_date, sample_lat_dd, sample_long_dd, sample_location, location_description, sampling_method, sampling_protocol, species_id_method, sample_name)

a <- data.frame(a, stringsAsFactors=FALSE)

vecdyn_mcm_2012 <- rbind.fill(vecdyn_mcm_2012, a)

```

At this stage you can check to see if the number of observations in the newly created vecdyn_mcm_2012 data-frame match the number of observations in the original manatee county data frame.

We can now start formatting the data-set so we can produce a time series graph. Convert dates to the Y-m-d format, in the case of this data set the dates are already in the correct format. We also convert the sample_value field to numeric.

```{r}
vecdyn_mcm_2012 <-
  vecdyn_mcm_2012 %>%
  dplyr::mutate(sample_end_date = as.Date(as.character(sample_end_date, format = "%Y/%m/%d"))) %>%
  dplyr::mutate(sample_start_date = as.Date(as.character(sample_start_date, format = "%Y/%m/%d"))) %>%
  dplyr::mutate(sample_value = as.numeric(sample_value))


```

Give the data set a title

```{r}

vecdyn_mcm_2012 <-
  vecdyn_mcm_2012 %>%
  dplyr::mutate(title = 'Manatee_County_Monitoring_2012')


```

Test the data set by producing a time series plot in from our newly created vecdyn data-set and compare it using ggplot. Note that this particular data set contains lots of sampling stations within manatee_county.

```{r}
vecdyn_mcm_2012  %>%
  dplyr::filter(taxon == "Aedes aegypti")  %>%
  dplyr::select(sample_value, sample_end_date) %>%
  dplyr::group_by(sample_end_date) %>%
  dplyr::summarise(sample_value = sum(sample_value)) %>%
  ggplot(aes(sample_end_date, sample_value)) + geom_line() +
  scale_x_date(labels = date_format("%b/%y"))

```

```{r}

Manatee_County_Mosquito_2012  %>%
  dplyr::filter(species == "Aedes aegypti")  %>%
  dplyr::select(sample_count, collection_date_end) %>%
  dplyr::group_by(collection_date_end) %>%
  dplyr::summarise(sample_count = sum(sample_count)) %>%
  plyr::mutate(collection_date_end = as.Date(as.character(collection_date_end, format = "%Y/%m/%d"))) %>%
  dplyr::mutate(sample_count = as.numeric(sample_count)) %>%
  ggplot(aes(collection_date_end, sample_count)) + geom_line() +
  scale_x_date(labels = date_format("%b/%y"))

```

Finally write the data set to CSV, set all missing value to blank ""

```{r}
write_csv(vecdyn_mcm_2012, "vecdyn_mcm_2012.csv", na = "")
```

You can also fill out the be extracting data from the appropriate zenodo page.

```{r}
vecdyn_mcm_2012_publication_info  <-data.frame(title=character(),
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
                 data_rights=character(),
                 embargo_release_date=character(),
                 data_set_type=character(),
                 stringsAsFactors=FALSE)

#write.csv(vecdyn_mcm_2012_publication_info, file = "vecdyn_mcm_2012_publication_info.csv", row.names = FALSE)

```

### Linking Vecdyn Data To Climate Data

Run through the above tutorial to import all the data for the next steps.

```{r}

# install.packages("RNCEP")
# install.packages("tidyverse")
# install.packages("readr")
# install.packages("plyr")
# install.packages("scales")
library(RNCEP)
library(tidyverse)
library(readr)
library(plyr)
library(scales)
library(lubridate)
```

# Linking Vecdyn Data and Climate Data

Run through the above tutorial to import all the data for the next steps. 

```{r}
# install.packages("RNCEP")
# install.packages("tidyverse")
# install.packages("readr")
# install.packages("plyr")
# install.packages("scales")
library(RNCEP)
library(tidyverse)
library(readr)
library(plyr)
library(scales)
library(lubridate)
```

## RNCEP: Obtain, Organize, and Visualize NCEP Weather Data
This package contains functions that retrieve, organize, and visualize weather data from the NCEP/NCAR Reanalysis (http://www.esrl.noaa.gov/psd/data/gridded/data.ncep.reanalysis.html) and NCEP/DOE Reanalysis II (http://www.esrl.noaa.gov/psd/data/gridded/data.ncep.reanalysis2.html) data-sets. Data are queried via the Internet and may be obtained for a specified spatial and temporal extent or interpolated to a point in space and time. 

For this package, we need to convert the relevant data to numerical format. 

```{r}
vecdyn_mcm_2012$sample_value = as.numeric(vecdyn_mcm_2012$sample_value)
vecdyn_mcm_2012$sample_lat_dd = as.numeric(vecdyn_mcm_2012$sample_lat_dd)
vecdyn_mcm_2012$sample_long_dd = as.numeric(vecdyn_mcm_2012$sample_long_dd)
# take a sub sample just for the purpose of this tutorial i.e. quicker processing speed
vecdyn_mcm_2012 <- dplyr::filter(vecdyn_mcm_2012, sample_location == "Mullins")
```

Unfortunately the RNCEP doesnt allow us (as far as i know) to extract daily averages based on dates and point locations alone, we can only extract values at particular date-times to try to give us a representative indication of the temperature / rainfall that day. Therefore, we need to create sampling points spread throughout the day to get daily averages. 

With this data-set, a sample start and end date is provided. Lets extract values beginning from the start date and ending at the end date over a 24 hour period. It would best best to extract hourly data points, however, for the sake of this tutorial we will extract climate data at 6 hour intervals. 

Create a time variable, starting at 00.01 everyday, then every 6 hours. 

```{r}
vecdyn_mcm_2012_00  <- 
  vecdyn_mcm_2012 %>%
  dplyr::select(sample_start_date, sample_lat_dd, sample_long_dd) %>%
  dplyr::distinct() %>%
  dplyr::mutate(sample_start_time = "00:00:01") %>%
  dplyr::mutate(sample_start_datetime = sample_start_date) %>%
  tidyr::unite("sample_start_datetime", c("sample_start_date","sample_start_time"), sep = " ", remove = FALSE) %>%
  dplyr::mutate(sample_start_datetime  = as.POSIXct(sample_start_datetime , format = "%Y-%m-%d%H:%M:%S"))
vecdyn_mcm_2012_06  <- 
  vecdyn_mcm_2012 %>%
  dplyr::select(sample_start_date, sample_lat_dd, sample_long_dd) %>%
  dplyr::distinct() %>%
  dplyr::mutate(sample_start_time = "06:00:01") %>%
  dplyr::mutate(sample_start_datetime = sample_start_date) %>%
  tidyr::unite("sample_start_datetime", c("sample_start_date","sample_start_time"), sep = " ", remove = FALSE) %>%
  dplyr::mutate(sample_start_datetime  = as.POSIXct(sample_start_datetime , format = "%Y-%m-%d%H:%M:%S"))
vecdyn_mcm_2012_12  <- 
  vecdyn_mcm_2012 %>%
  dplyr::select(sample_start_date, sample_lat_dd, sample_long_dd) %>%
  dplyr::distinct() %>%
  dplyr::mutate(sample_start_time = "12:00:01") %>%
  dplyr::mutate(sample_start_datetime = sample_start_date) %>%
  tidyr::unite("sample_start_datetime", c("sample_start_date","sample_start_time"), sep = " ", remove = FALSE) %>%
  dplyr::mutate(sample_start_datetime  = as.POSIXct(sample_start_datetime , format = "%Y-%m-%d%H:%M:%S"))
vecdyn_mcm_2012_18  <- 
  vecdyn_mcm_2012 %>%
  dplyr::select(sample_start_date, sample_lat_dd, sample_long_dd) %>%
  dplyr::distinct() %>%
  dplyr::mutate(sample_start_time = "18:00:01") %>%
  dplyr::mutate(sample_start_datetime = sample_start_date) %>%
  tidyr::unite("sample_start_datetime", c("sample_start_date","sample_start_time"), sep = " ", remove = FALSE) %>%
  dplyr::mutate(sample_start_datetime  = as.POSIXct(sample_start_datetime , format = "%Y-%m-%d%H:%M:%S"))
vecdyn_mcm_2012_all <- rbind(vecdyn_mcm_2012_00,vecdyn_mcm_2012_06,vecdyn_mcm_2012_12,vecdyn_mcm_2012_18)
vecdyn_mcm_2012_all <- data.frame(vecdyn_mcm_2012_all)
```

In this example,  we use the date-time and location data obtained from the trap locations (gps coordinates)

```{r}
## Now collect cloud cover, temperature, and wind
## information for each point in the subset ##
vecdyn_mcm_2012_all$temp <- NCEP.interp(variable='air.sig995', level='surface', lat=vecdyn_mcm_2012_all$sample_lat_dd, lon=vecdyn_mcm_2012_all$sample_long_dd, dt=vecdyn_mcm_2012_all$sample_start_datetime, reanalysis2=FALSE, keep.unpacking.info=TRUE)
```

We now have temperature data for each trap site at a particular date-time. Note that we filtered sample_location == "Mullins" so we only extract values for a limited number of the trap locations.

Next lets take an average of the 6 hourly daily climate data creating a daily average

```{r}
vecdyn_mcm_2012_av_daily_temp <-
vecdyn_mcm_2012_all %>% 
  dplyr::group_by(sample_lat_dd, sample_long_dd, sample_start_date) %>%
  dplyr::summarise(avg_temp = mean(temp))
```

And now lets create a query that merges the temp data we just gathered back into the main data set.

```{r}
vecdyn_mcm_2012_with_temps <- 
  dplyr::inner_join(vecdyn_mcm_2012, vecdyn_mcm_2012_av_daily_temp, by = c("sample_lat_dd" = "sample_lat_dd","sample_long_dd" = "sample_long_dd", "sample_start_date"="sample_start_date"))
```

https://cran.r-project.org/web/packages/RNCEP/RNCEP.pdf
You can also repeat the steps for the relative humidity (‘rhum.sig995’ Relative Humidity), which can be used as a proxy for rainfall. 