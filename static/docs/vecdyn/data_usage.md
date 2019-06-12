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