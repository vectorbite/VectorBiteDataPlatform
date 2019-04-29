import csv
import logging
import vtfuncs

logger = logging.getLogger("web2py.app.vbdp")


def view_vectraits():
    # A simple demonstration of an interface to explore the published vectraits dataset.
    db2.maintable.uid.readable = False

    grid = SQLFORM.smartgrid(db2.published_data,
                             # linked_tables=['experimentalconditions', 'taxonomy', 'studylocation', 'sourceinfo', 'traitdescription'],
                             csv=True,
                             deletable=False,
                             create=False,
                             details=False,
                             editable=False,
                             paginate=50)

    return dict(form=grid)


def view_citations():
    # create the SQLFORM grid to show the existing assignments
    # and set up actions to be applied to selected rows - these
    # are powered by action functions defined below
    db2.citation.citationid.readable = False

    grid = SQLFORM.smartgrid(db2.citation,
                             csv=True,
                             deletable=False,
                             create=False,
                             details=False,
                             editable=False,
                             # links=links,
                             paginate=50)

    return dict(form=grid)


def validate_test():
    report = ""
    form = SQLFORM.factory(
        Field('csvfile', 'upload'), table_name="dataset_upload")
    if form.validate():
        origin_filename = request.vars.csvfile.filename
        temp_filename = form.vars.csvfile
        logger.info("Validating {}...".format(origin_filename))
        logger.debug("(stored at {})".format(temp_filename))
        # Hacky method to open and read in whole file without actually using request.vars.csvfile.file.read()
        # Don't know why that method was giving inconsistent results, but this seems to work.
        with open(request.folder + "uploads/" + form.vars.csvfile) as candidate_src:
            candidate_reader = csv.reader(candidate_src, quotechar='"')
            candidate = [x for x in candidate_reader]
        if len(candidate) < 1:
            logger.warning(
                "Uploaded file {} (stored at {}) does not contain any information".format(
                    origin_filename,
                    temp_filename))
            # TODO: Throw error back to user
        elif len(candidate) == 1:
            logger.warning(
                "Uploaded file {} (stored at {}) does not contain both headers and values".format(
                    origin_filename,
                    temp_filename))
            # TODO: Throw error back to user
        else:
            # Process
            logger.debug("File length: {}".format(len(candidate) - 1))
            logger.debug("Header row length: {}".format(len(candidate[0])))
            logger.info("Verifying integrity of {}".format(origin_filename))
            logger.setLevel(logging.INFO)
            report = vtfuncs.validate_vectraits(candidate, origin_filename)
            # logger.debug(IS_INT_IN_RANGE(minimum=0)(-1))
            # logger.info(IS_LENGTH(5)('1234567'))

        # Create class for a vectraits row
        #     This can go in the modules folder
        # Class can have validators for each variable within it
        # Convert each entry in a row into a dict
        #     Could do this by using the header row as keys
        #     Might need to zip the header and current row together or something?
        # pass keyword to class constructor as follows: vt_row = vt_row_class(**row)
        # Could also do this as a list ie vt_row = vt_row_class(*row)
        #     This would also not require the dictionary conversion step

    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form, report=report)
