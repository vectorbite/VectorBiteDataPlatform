#! /usr/bin/env python
import csv
from distutils.util import strtobool

# Read definitions csv
with open("defs.csv", "r") as f:
    freader = csv.reader(f)
    next(freader)
    defsdata = [{"name": x[0],
                 "description": x[1].replace("<br>", "\n"),     # Allow for <br> to be used to insert linebreaks.
                 "required": bool(strtobool(x[2])),             # Convert variants used to symbolise bools (y/n etc.)
                 "example": x[3],
                 "type": x[4],
                 "restrictions": list(filter(None, x[5:]))} for x in freader]

    # defsdata = defsdata[1:]

# Read stub template
with open("stub.stub", "r") as f:
    stub = f.read()

# Start summary table
    summary_str = "| Field | Type | Required | \n| ----: | :--: | :------: |\n"
# Create definition files
for definition in defsdata:
    outstr = stub
    outstr = outstr.replace("@NAME", definition["name"])
    outstr = outstr.replace("@TYPE", definition["type"])
    if definition["name"] == "locationdateprecision":
        # Shim to add locationdateprecision description
        descrip_str = definition["description"]
        descrip_str += """
        \n
| Ranking | Description             | Example                    | Date noted |
| ------- | ----------------------- | -------------------------- | ---------- |
| 5       | Full date provided      | 4 August 92                | 04/08/1992 |
| 4       | Month and year provided | August 1992                | 01/08/1992 |
| 3       | Month Range provided    | Summer 92 / June-August 92 | 01/06/1992 |
| 2       | Only year provided      | 1992                       | 01/01/1992 |
| 1       | Unusable date provided  | August                     | NA         |
| 0       | No date provided        | NA                         | NA         |
        """

        outstr = outstr.replace("@DESCRIP", descrip_str)
    else:
        outstr = outstr.replace("@DESCRIP", definition["description"])
    outstr = outstr.replace("@EXAMPLE", "*{}*".format(definition["example"]))
    if definition["required"]:
        outstr = outstr.replace("@REQ", "**This is a Required Field!**")
    else:
        outstr = outstr.replace("@REQ", "")

    if definition["restrictions"]:
        restriction_str = "| Restriction |\n| :---------: |\n"
        for restriction in definition["restrictions"]:
            restriction_str += "| {} |\n".format(restriction)
        outstr = outstr.replace("@RESTRICTIONS", restriction_str)
    else:
        outstr = outstr.replace("@RESTRICTIONS", "")

    # Write to summary
    summary_str += "| [{0}](../vectraits_field_definitions/{0}) | {1} | {2} |\n".format(definition["name"], definition["type"], definition["required"])

    # Write to file
    with open("../vectraits_field_definitions/{}.md".format(definition["name"]), "w+") as mdfile:
        mdfile.write(outstr)

with open("../field_definition_overview.md", "r") as f:
    field_def_overview = f.read()

print(summary_str)

field_def_overview = field_def_overview[:field_def_overview.find("## Field Definitions")] + "## Field Definitions\nPlease click on any field name to find more details about the field.\n\n" + summary_str
with open("../field_definition_overview.md", "w+") as f:
    f.write(field_def_overview)
