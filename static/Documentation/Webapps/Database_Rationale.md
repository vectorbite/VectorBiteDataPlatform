# Database Rationale
This document exists in part to provide a guide to the PostgreSQL db layout, and as an explanation for why various decisions have been made.

## Schemas
The database is split into a multitude of schemas, each with their own content and purpose.

| Schema    | Purpose              |
| --------- | -------------------- |
| vectraits | VecTraits data       |
| vecdyn    | VecDyn data          |
| vbdp      | Webapp and user data |
| geo?      | geographic data      |
| tax?      | taxonomic data       |

### User Permissions
**THIS IS A TODO**

Each user in the database should have differential access to different schemas. Geo and tax should be accessible by all other users, whilst vectraits and vecdyn should be accessible only to the appropriate users, so we keep data segregated. vbdp should probably just be independant of the others.

## VecTraits Rationale
Vectraits is split into a number of tables to prevent serious data duplication.

### Table hierarchy
```
.vectraits
└── maintable
    ├── experimentalconditions
    ├── taxonomy
    ├── studylocation
    ├── sourceinfo
    │   ├── citation
    │   └── contributor
    └── traitdescription
```
The maintable stores each trait observation along with associated metadata. Any metadata duplicated often (such as publication information) is stored in a separate table, and referenced by id.

### The published_data view
This database view (different from a view in Web2Py) provides easy access to a certain subset of the data, namely any data which is both published and has an embargo release date in the past. Whilst on the backend this is just a query preappended to any query run against the database via the view, to Web2Py this view is presented as a separate table.

This layout has the advantage of restricting access to banned data at a very low level, reducing the likelihood for information leaks as Web2Py literally doesn't know about some of the data via this dbview.
