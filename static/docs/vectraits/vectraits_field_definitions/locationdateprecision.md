[Back to Field Definitions](../../field_definition_overview)
# locationdateprecision

## Type
Integer

## Description
**This is a Required Field!**

The precision of the value in [locationdate](../locationdate) between 0 and 5. Below is a table which defines the different rankings. If unsure, it is best to be conservative and pick the lowest precision value you can be sure of.
        

| Ranking | Description             | Example                    | Date noted |
| ------- | ----------------------- | -------------------------- | ---------- |
| 5       | Full date provided      | 4 August 92                | 04/08/1992 |
| 4       | Month and year provided | August 1992                | 01/08/1992 |
| 3       | Month Range provided    | Summer 92 / June-August 92 | 01/06/1992 |
| 2       | Only year provided      | 1992                       | 01/01/1992 |
| 1       | Unusable date provided  | August                     | NA         |
| 0       | No date provided        | NA                         | NA         |
        
## Example
*0*

## Restrictions
| Restriction |
| :---------: |
| Not Null |
| 0 <= x <= 5 |

