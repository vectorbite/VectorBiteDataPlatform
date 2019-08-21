## Release Notes
Current version: **0.3.11**

---
### 0.3.11
- Fixed validator
    - Now actually fails when essential columns are completely missing
    - Now correctly handles the following variants of missing data:
        - `""`
        - `NA`
        - `na`
        - `NaN`
        - `nan`
- Updated documentation to more explicitly state that missing data SHOULD be left entirely blank.

### 0.3.10
- Added documentation on data digitisation and submission procedure

### 0.3.9
- Temporarily disabled VD home statistics
- Added documentation links to navbar
### 0.3.8
- Enhanced download pages
- vecdyn docs updates

### 0.3.7
- Fixed contact pages
- Fixed task manager
- Implemented data bulk uploader and normal uploader via web2py scheduler.
- Auto vecdyn-taxon standard implemented into scheduler
- Small changes to vecdyn back end and scheduler set-up to reject duplicate data-sets.
- Fixed site statistics queries.
- Updated favicon

#### 0.3.6
- Fixed "About us" page

#### 0.3.5
- Fixed "Explore Vectraits" button

#### 0.3.4
- Moved documentation in preparation for readthedocs
- Added new VecTraits template

#### 0.3.3
- Added two new fields to vecdyn publication info db.

#### 0.3.2
- Fixed VecDyn index page links, text updates.
- Moved submit vecdyn data to vecdyn controller.
- Added key database statistics to vecdyn index & admin pages.

#### 0.3.1
- Fixed VecDyn index page button

#### 0.3.0
- Moved VecDyn data submission to scheduler
- Refactored vecdyn to one controller

---

### 0.2
#### 0.2.2
- Added vectraits validation -> submission workflow
- Added skeleton for automatic documentation via readthedocs

#### 0.2.1
- Added about pages for all subsites
- Added vital db statistics for VecTraits

#### 0.2.0
- Rethemed the entire site and reorganised to a subsite structure

---

### 0.1
#### 0.1.1
- Modified vectraits models to correctly handle integer data

#### 0.1.0
- Resructured vecdyn database files
- Fixed vecdyn data downloader bug
    - VecDyn now fully functional
- Migrated VecTraits to PostgreSQL
- **Alpha-release-ready VBDP version**

---

### 0.0
#### 0.0.9
- gbif & gadm updates
    - Incorporated gbif taxonimc and gadm spatial database into vecdyn database

#### 0.0.8
- Completed Vecdyn Admin Interface (beta)
    - Fixed general layout, page linking and logic. Interface allows admin to upload datasets, visualise data entries, standardise taxonomic data and geographic data.

##### 0.0.7
- Full controller code cleanup
    - Fixed small coding style errors and improved readability throughout the codebase

#### 0.0.6
- Minor wording change in admin interface

#### 0.0.5
- Minor changes to Vecdyn data manager

#### 0.0.4
- Improved dataset rights facility

#### 0.0.3
- Added documentation
    - Release procedure
    - Logging guide

#### 0.0.2
- Added comments, added Country csv file

#### 0.0.1
- Added release notes
- Implemented GitFlow
- Improved code style
