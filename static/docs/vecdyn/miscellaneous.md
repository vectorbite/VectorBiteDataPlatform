# Issues, troubleshooting & suggestions


Any suggestions or todos with regards to the database (e.g. new columns, schema modifications etc.) can be logged as [Issues on GitHub](https://github.com/vectorbite/VectorBiteDataPlatform/issues).
Issues allow for discussions among multiple users, file attachments, colour-coded labels etc.

# Known issues

The FAO’s GUAL data set has been restructured for VecDyn. A new column was created which represents an individual ID for each admin unit. This creates a few minor issues, since some region codes are not unique and therefore, an additional ‘b’ has been added to the end of each ADM\_CODE’ which has been used in VecDyn as a ‘Primary key’. 



| ADM_CODE   | ADM2_NAME                         | ADM1_NAME | ADM0_NAME                   |  Change   | 
| ---------- | --------------------------------- | --------- | --------------------------- | --------- | 
| 48472      | Administrative unit not available | Rukwa     | United Republic of Tanzania |           |
| 484722 | Administrative unit not available | Mwanza    | United Republic of Tanzania     | 2 added to end of ADM_CODE          |
| 22917      | Ifelodun                          | Kwara     | Nigeria                     |           |
| 229172 | Ifelodun                          | Osun      | Nigeria                         | 2 added to end of ADM_CODE          |
| 23036      | Surulere                          | Oyo       | Nigeria                     |           |
| 230362     | Surulere                          | Lagos     | Nigeria                     | 2 added to end of ADM_CODE         |
| 22602      | Osisioma Ngwa                     | Abia      | Nigeria                     |           |
| 226022 | Ukwa West                         | Abia      | Nigeria                         | 2 added to end of ADM_CODE           |
| 15426      | Gnral. Antonio Elizalde           | Guayas    | Ecuador                     |           |
| 154262 | Milagro                           | Guayas    | Ecuador                         | 2 added to end of ADM_CODE          |


# Credits

TODO

# Contact

Submitting data

# Citing  VecDyn

TODO

# References

TODO