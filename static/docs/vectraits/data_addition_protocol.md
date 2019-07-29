## Adding new data

Please follow the following instructions for adding new data, either digitized from the literature, or raw data obtained from experiments.

### Data sources
These will typically come from published papers, dissertations, and reports.

### Overall workflow

The overall steps are:

- Compile the sources/papers that are candidates for digitization
- Check if they have already been digitized into VecTraits/BioTraits
- Add them to the Biotraits Mendeley library
- Digitize
- Validate your filled-in template on rwww.vectorbyte.org, see the [validator documentation](validator.md) for more detail
- Re-classify them on the Biotraits Mendeley Library as being digitized

#### Before digitizing data
Before starting to digitize new data, and in order to avoid duplicating data already in the database, please check your citations against those already in the database. To do this you can use the `searchcite` tool, which you can either obtain from the development team or from [this repository](www.github.com/).

<!-- ### Storing the candidate papers

Once you have determined that a paper's data are suitable for BioTraits (and have not already been digitized), please add the papers pdf version to the mendeley library entry -->

### Using the VecTraits/BioTraits template

When you have new data to include in the dataset, is really important to
firstly "map" it to the template. There are here a few guidelines:

- It can be a good idea to put your new data in a new directory within the `BioTraitsDB` repository under `Digitized-Subsets` and work on them there, so all changes you make are stored and shared there with the rest of the VecTraits/BioTraits team.
- If you do not have access to the `BioTraitsDB` repository then it is worth keeping your data in an organised manner on a local drive until such a time when you do get access to the repository.
- Open both template and raw data and first try to match all those fields for which you have data (you can start matching column names, maybe some of them are the same).
- Pay special attention to inputting data into the following columns:
    - `originalid`
    - `originaltraitvalue`
    - `originaltraitunit`
    - `location`
    - `locationdate`
    - `locationdateprecision`
    - `citation`
    - `published`
    - `embargorelease`
    - `submittedby`
    - `citation`

<!-- -   Data will ultimately be converted to SI units. In case your data is not in SI units, store it in the `OriginalTraitValue` and
    `OriginalTraitValueUnits`. Then you will be able to
    convert the original values to SI using the provided `mass
    calculator` tool (see below). SI data will be stored in the
    `StandarizedTraitValue` and
    `StandarizedTraitValueUnits` columns.   -->

- If you are not sure abut the meaning of the field (column) name, you can have a look at the [Field Definitions](field_definition_overview.md). If you still have doubts, just ask!

- Fill the `submittedby` column with your name (if you have digitized the data) or the name of the appropriate person and put the corresponding e-mail address in the `contributoremail` column.

- Leave empty all fields with no value.

- A biotraits data template containing all field names is available [here](https://www.vectorbyte.org/VectorBiteDataPlatform/vectraits/vectraits_template.html).


### Standardizing original data reference

It is important that each row have a complete reference for the data
source (unless it is an unpublished dataset). There is a column called
`Citation` that contains the full citation. Having the
citation in full is really important for retrieving the Digital Objects
Identifier (DOI) of that reference. To obtain the DOIs (if not already
provided), save a file containing all the full citations for which you
need to find the DOI. Then you can use the `ref2doi` tool,
which can be downloaded from the `dgkontopoulos/ref2doi`
repository on BitBucket. A help/protocol file for using this tool is in
the repository.

### Standardizing taxonomy

We are currently building a taxonomy standardizer tool. This is based on
the R package `taxize` (A guide to use this package can be
found [here](http://cran.r-project.org/web/packages/taxize/vignettes/taxize_vignette.html).
In the meantime you can directly use this package to retrieve all the
taxonomic information.

First, you should check the species name (or minimum taxonomic level you
have). This tool queries the Global Names Resolver through R and then
parses the results.

We call the `gnr_resolve` tool by submitting the unique
names in the `interactor1` (or `interactor2`) column.
Once it has finished, the output returns four different columns:
`submitted_name`, `matched_name`,
`score` (grade of similitude between submitted and matched
names) and `source` (for each entry, the tool queries
different sources to check the name). Then, we will match the
`submmited_name` against the `matched_name` (the
one queried by the tool), both in the results output. We will find that
for some names we will have an exact match but for others not. For those
names that there isn’t an exact match (e.g. the
`matched_name` includes author and year besides species name
depending on source), we will compare the scores. If for an entry, we
get the same scores for all the matches, we can use any
`matched_name` (but just keeping the species name and
removing the extra information). Otherwise, we will use the matched name
with the highest score.

Once we have checked all the names, we will retrieve the taxonomy using
the `tax_name` function. You will need to select the
database of interest to search for the taxonomy (NCBI is being used in
the dataset as a first option, but if this is not available you can also use ITIS). First we will try to query the species name, but in case
that doesn’t work, we will use the genus name. Finally, we will fill the
dataset with our results.

### Special cases

There are some special cases where the metabolic traits were measured
not for a whole species but for a part of it. For example, the database can accommodate measures for tissues, leaves, etc. In these cases is necessary to distinguish between whole organism or part. There are then specific columns to do this: `interactor1part` and
`interactor1parttype`.

Please let us know if you find any specific case for which you have
problems, as this could help us to improve the dataset and make the data template as comprehensive and general as possible.

<!-- ### Examples

If you have any doubts about how you can do something and you want to
view some examples, you can have a look in the directories for the data
already mapped. These are available in the BioTraitsDB repo. You can have a
look at Biotraits, ChenThomas, Burnside or any of the directories here.
Here are the files you will typically find in any one of these example
directories:

- `Name-Raw.csv` or `Name-Raw.xls` files:
    Contain the raw data, where "Name" is the name of your raw
    data file. Please avoid using excel to the extent possible — storing
    data in \*.csv is best.

-   `NameTemplate.R`: Script (written in R) used to map the
    raw data to the template.

-   `.Rdata` and `.csv`: Matched datasets
    including full citation and stored in both R and CSV files. See next
    section for more details.

-   `GetDOI.csv`: CSV file where the full citation is stored
    to apply the `ref2doi` tool and get the DOI numbers.

-   `DOI.csv`: Results from the `ref2doi` tool. As
    explained in the `ref2doi` protocol, this file will be a
    tab delimited file with columns for the input reference, the result
    provided by CrossRef and the corresponding DOI.-->

### Storing the raw data

Your raw data can be stored in both `.Rdata` and
`.csv` files, but CSV is preferred. Please, fill all the rows in your file and try to not
leave blank spaces. You can use NULL or NA if you don’t have data to
fill in some fields. Once the data have been mapped let us know. Then we
will review it and import it into Biotraits.
