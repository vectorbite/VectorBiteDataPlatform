---
title: "Mapping existing data to Vecdyn Template in R markdown"
author: Matthew Watts
date: July 2020
output:
  html_document:
    keep_md: true
---


```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

In this tutorial we will map an existing vector population data set to the VecDyn format. 

Please refer to the 'R for Data Science guide'(https://r4ds.had.co.nz/) for further information on some of the techniques we use here. 

Load the following packages (and install if required)

```{r}
library(tidyverse)
library(readr)
library(lubridate)
library(plyr)
```

Create the VecDyn data template / data-frame and name it.


```{r}

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

```{r}

Manatee_County_Mosquito_2012 <- read.csv(url("https://zenodo.org/record/1217702/files/VectorBase-2012-Manatee_County_Mosquito_Control_District_Florida_USA.csv?download=1"), stringsAsFactors=FALSE)

```

Inspect the data-frame.

```{r}
head(Manatee_County_Mosquito_2012)
```

All geo-names should be presented in one field. The Manatee_County data set's study location is characterized using 3 fields, we need to combine this information into one field.  We can use a tidyr function called "unite" to do this. 

```{r}
Manatee_County_Mosquito_2012 <-
  Manatee_County_Mosquito_2012 %>%
  tidyr::unite("location_description", c("location_ADM2","location_ADM1", "location_country"), sep = ",")

```

Extract all the data from the Manatee_County_Mosquito_2012 to individual vectors. Each new vector name represents a name in the VecDyn template

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

Bind the extracted values together creating and create a new data-frame.  We then bind the new data-frame with the vecdyn_mcm_2012 template.

```{r}

a <- cbind(taxon, sample_value, sample_sex, sample_stage, sample_start_date, sample_end_date, sample_lat_dd, sample_long_dd, sample_location, location_description, sampling_method, sampling_protocol, species_id_method, sample_name)

a <- data.frame(a, stringsAsFactors=FALSE)

vecdyn_mcm_2012 <- rbind.fill(vecdyn_mcm_2012, a)

```

You should check to see if the number of observations in the newly created vecdyn_mcm_2012 data frame match the number of observations in the original manatee county data frame.

All VecDyn dates need to be formatted as Y-m-d, in this example the dates are already in the correct format. 

```{r}
vecdyn_mcm_2012 <-
  vecdyn_mcm_2012 %>%
  dplyr::mutate(sample_end_date = as.Date(as.character(sample_end_date, format = "%Y/%m/%d"))) %>%
  dplyr::mutate(sample_start_date = as.Date(as.character(sample_start_date, format = "%Y/%m/%d"))) %>%
  # We also convert the sample_value field to numeric so we can create a time series in the next step
  dplyr::mutate(sample_value = as.numeric(sample_value))


```

We can test our new data frame set against the original data frame to see if they produce the same results.

```{r}
vecdyn_mcm_2012  %>%
  dplyr::select(sample_value, sample_end_date) %>%
  dplyr::group_by(sample_end_date) %>%
  ggplot(aes(sample_end_date, sample_value)) + geom_line() +
  scale_x_date(date_breaks = "1 month", date_minor_breaks = "1 week",
             date_labels = "%B")

```

```{r}

Manatee_County_Mosquito_2012  %>%
  dplyr::select(sample_count, collection_date_end) %>%
  plyr::mutate(collection_date_end = as.Date(as.character(collection_date_end, format = "%Y/%m/%d"))) %>%
  dplyr::mutate(sample_count = as.numeric(sample_count)) %>%
  ggplot(aes(collection_date_end, sample_count)) + geom_line() +
  scale_x_date(date_breaks = "1 month", date_minor_breaks = "1 week",
             date_labels = "%B")

```

Finally write the data set to CSV, set all missing value to blank ""

```{r}

write.csv(vecdyn_mcm_2012, "vecdyn_mcm_2012.csv", row.names = FALSE, quote=TRUE, na = "", fileEncoding = "UTF-8")

```

Next complete the publication information, this can be submitted as a CV or using the online web form when you submit the main data-set. The publication information for our example data-set here is found here https://zenodo.org/record/1217702#.Xvs89ygza70. Note that this information should only be recorded as one line (or row) for each field. 

```{r}
rm(list=setdiff(ls(), c("vecdyn_mcm_2012")))
```

You will also need to provide publication information for the data-set on the VecDyn data submissions page (example below) . 

```{r}

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



# Extracting observational climate data to spatial-temporal sample points [trap locations]

In this section of the tutorial, we will show you how to combine observational climate data and Vecdyn data. 
You can run through the above steps to get the data set we'll be working with. Please note for simplicity, we should you how to download and process max daily temp and daily precipitation. Depending on the species studied or study methodology, it may be appropriate to use daily min temps, take an average of min / max temps or calculate the range. You can adapt the code below to do this, minimum daily temperature data can also be sourced from the links below.  

## General guidelines 

CPC Global Temperature data provided by the NOAA/OAR/ESRL PSD, Boulder, Colorado, USA, from their Web site at https://www.esrl.noaa.gov/psd/ 

In order to download the maximum daily temperature in degrees celsius (tmax) datasets (in order for workflow to complete), please follow the link below: 

Index of ftp://ftp.cdc.noaa.gov/Datasets/cpc_global_temp/

Store these netCDF files in your main working directory


CPC Global Unified Precipitation (inches) data provided by the NOAA/OAR/ESRL PSD,	Boulder, Colorado, USA, from their Web site at https://www.esrl.noaa.gov/psd/

In order to download the daily precipitation datasets (in order for workflow to complete), please follow the link below: 
ftp://ftp.cdc.noaa.gov/Datasets/cpc_global_precip/

Store these netCDF files in your main working directory


```{r}
library(tidyverse)
library(lubridate)
library(sf)
library(tmap)

# Create a Spatial reference system
project_crs <- 4326


# rename main data set
vector_abun <- vecdyn_mcm_2012

# Create a year field from the dates, we will use this later for the climate extraction
vector_abun$year <- format(as.Date(vector_abun$`sample_start_date`), "%Y")

# conver long / lats to an sf spatial object
vector_abun = st_as_sf(vector_abun, coords = c("sample_long_dd", "sample_lat_dd"), crs = project_crs,  remove = FALSE)

# Visualize trap locations 

# get unique trap locations
traps <- dplyr::distinct(vector_abun, sample_lat_dd, sample_long_dd, geometry)

# Obtain USA state map from maps package
usa = st_as_sf(maps::map("state", fill = TRUE, plot = FALSE))
usa = st_set_crs(usa, project_crs)

# Obtain Florida from the USA map
state = subset(usa, grepl("florida", usa$ID))
usa <- st_buffer(usa, 0)

# Plot locations 
tm_shape(usa) +
  tm_polygons() + 
  tm_shape(traps) +
  tm_dots()

tm_shape(state) +
  tm_polygons() + 
  tm_shape(traps) +
  tm_dots()


```


```{r}

###################################################################################################################
#EXTRACTION TMAX - Note that the CPC climate data spans from 1979 to 2019,remove observations outside of this range
###################################################################################################################
#Load packages
library(RNetCDF)
library(raster)
library(rgdal)
library(sf)
library(sp)

# create a vector of years in the data set (we use this to select tmax files)
years <- st_set_geometry(vector_abun, NULL)
years <- dplyr::distinct(years, year)
years <- as.vector(years$year)

# create start message
print (paste(Sys.time(),"start"))

# count the number of rows in the traps dataframe so we can create an empty df
df_count <- NROW(traps)

# Create a new dataframe with the same number of rows as there are traps 
tmaxAll <- as.data.frame(matrix(0, ncol = 0, nrow = df_count))

# Copy the geometry to the dataframe
tmaxAll$sample_lat_dd <- traps$sample_lat_dd
tmaxAll$sample_long_dd <- traps$sample_long_dd

# loop through each year in the years vector and look for matching file names in the Wd
for (y in 1:length(years))
{
    # create file pattern
    pat <-paste("tmax.",years[y], sep="")
    
    year <- years[y]
    
    #list the files matching the pattern
    listfiles <- list.files(pattern = pat)
    
    # create a loop that runs through every matching file in the wb
    for(f in listfiles)
    {
      
    # create a raster brick, each file in the brick will represent a day of temperature sampling
      tmax = brick(f)
      # rotate the raster brick to convert to conventional -180 to 180 sample_long_dd
      tmax <- rotate(tmax)
      # replace -999 values with NA 
      tmax <- reclassify(tmax, cbind(-999, NA))
      # create a day variable from the brick from each layer, representing each day in the year 
      days <- nlayers(tmax) 
      # ensure the Coordinate Reference System in the temp data and trap sites are matching
      shp = st_transform(traps, crs(tmax))
      #Extract data from each layer in the brick
      for (i in 1:nlayers(tmax))
        {
        print (paste(Sys.time(),"extracting-", "dateset:", f, ",year",year, ",Day:",i))
        #print(c(i, f))
        tmaxEx <- raster::extract(tmax[[i]], 
                as_Spatial(shp),
                method = 'bilinear', 
                fun = mean,
                na.rm = T)
        # create a dataframe out of the extracted data 
        tmaxexdf <- as.data.frame(tmaxEx)
        # name the column name by year
        colnames(tmaxexdf) <- paste(year, i, sep = "-")
        # bind newly created dataframe to the tmaxall, each loop in the cycle will create a new column
        tmaxAll <- cbind(tmaxAll,tmaxexdf)
      
      }
    }}

# convert the dataset to the correct format 
max_temp <- tmaxAll %>% gather(date, max_temp, -sample_lat_dd, -sample_long_dd)

# Now we have temperature for every day of each trap location

print (paste(Sys.time(),"finished Run tmax"))

# if you are dealing with a big dataset it would be a good idea to save this as a csv and re import it later
#write.csv(max_temp, file = "max_temp.csv", row.names=FALSE)


rm(list=setdiff(ls(), c("vector_abun", "project_crs", "vecdyn_mcm_2012", "max_temp")))
```

```{r}
################################################################################
#EXTRACTION Precip - same steps as above
################################################################################
#Load packages
library(RNetCDF)
library(raster)
library(rgdal)
library(sf)
library(sp)

project_crs <- "+proj=longlat +WGS84 (EPSG: 4326) +init=epsg:4326 +proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs +towgs84=0,0,0"

# create a vector of years in the data set (we use this to select tmax files)
years <- st_set_geometry(vector_abun, NULL)
years <- dplyr::distinct(years, year)
years <- as.vector(years$year)

# get unique trap locations
traps <- dplyr::distinct(vector_abun, sample_lat_dd, sample_long_dd, geometry)


print (paste(Sys.time(),"start"))

df_count <- NROW(traps)

precAll <- as.data.frame(matrix(0, ncol = 0, nrow = df_count))

precAll$sample_lat_dd <- traps$sample_lat_dd

precAll$sample_long_dd <- traps$sample_long_dd

for (y in 1:length(years))
{
  pat<-paste("precip.",years[y], sep="")
  year <- years[y]
  listfiles <- list.files(pattern = pat)
  for(f in listfiles)
  {
    precip = brick(f)
    precip <- rotate(precip)
    precip <- reclassify(precip, cbind(-999, NA))
    days <- nlayers(precip) 
    shp = st_transform(traps, crs(precip))
    for (i in 1:nlayers(precip))
    {
      print (paste(Sys.time(),"extracting-", "dateset:", f, ",year",year, ",Day:",i))
      precipEx <- raster::extract(precip[[i]], 
                                  as_Spatial(shp),
                                  method = 'bilinear',
                                  fun = mean,
                                  na.rm = T)
      precipexdf <- as.data.frame(precipEx)
      colnames(precipexdf) <- paste(year, i, sep = "-")
      precAll <- cbind(precAll,precipexdf)
    }
  }}
precip <- precAll %>% gather(date, precip, -sample_lat_dd, -sample_long_dd)

print (paste(Sys.time(),"finished Run precip"))


rm(list=setdiff(ls(), c("vector_abun", "project_crs", "vecdyn_mcm_2012", "max_temp", "precip", "traps")))
```


```{r}
######################################
#Join the climate data to main data set
######################################


# join climate datasets together by lat / long and date

clim_df <- dplyr::inner_join(max_temp, precip, by = c("sample_lat_dd", "sample_long_dd", "date"))

#convert year-Day of the year into standard date format
clim_df$date <- as.Date(clim_df$date, format="%Y-%j")


```

For the sake of this tutorial we will simplify the abundance data set - consider now that we have two data sets, we need to join them together. This could be done it in different ways depending on what analysis we want to achieve i.e. a standard linear regression or time series analysis. 

For a linear regression we can join the matching mosquito abundance observations to the matching climate observations.
We could also take average of all the observations by weeks, since the mosquito traps in this data set are only collected once a week.



```{r}

# convert dates to epiweeks in the climate data frame and average values by epi week

clim_df_averages <-
clim_df %>%
  dplyr::mutate(epi_week = epiweek(date)) %>%
  dplyr::select(sample_lat_dd, sample_long_dd, epi_week, max_temp, precip) %>%
  dplyr::group_by(sample_lat_dd, sample_long_dd, epi_week) %>%
  dplyr::summarise(max_temp = mean(max_temp), precip = mean(precip))
  

vector_abun_clim_averages <-
  vector_abun %>%
  dplyr::mutate(epi_week = epiweek(sample_end_date)) %>%
  dplyr::group_by(sample_lat_dd, sample_long_dd, epi_week, taxon, sample_sex) %>%
  dplyr::summarise(sample_value = mean(sample_value)) %>%
  dplyr::left_join(clim_df_epi_week_averages, by = c("sample_lat_dd", "sample_long_dd", "epi_week"))  


# Plot results

ggplot(vector_abun_clim_averages, aes(x=epi_week, y=`sample_value`)) +
  geom_line()


ggplot(vector_abun_clim_averages, aes(x=epi_week, y=max_temp)) +
  geom_line()

ggplot(vector_abun_clim_averages, aes(x=epi_week, y=precip)) +
  geom_line()




```