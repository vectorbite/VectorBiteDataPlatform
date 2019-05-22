import csv
import logging
import vtfuncs

logger = logging.getLogger("web2py.app.vbdp")


def index():
    rows = B(db2(db2.published_data).count())
    taxa = B(db2(db2.taxonomy).count())
    pubs = B(db2(db2.citation).count())
    locs = B(db2(db2.studylocation).count())
    return dict(rows=rows, taxa=taxa, pubs=pubs, locs=locs)


def about():
    """
    Controller for about page
    """
    return locals()


@auth.requires_login()
def view_vectraits():
    # A simple demonstration of an interface to explore the published vectraits dataset.
    db2.maintable.uid.readable = False

    grid = SQLFORM.smartgrid(db2.published_data,
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


def validate_vectraits():
    report = ""
    failed = False
    validated = False
    form = SQLFORM.factory(
        Field('dataset_upload', 'upload'), table_name="dataset_upload")
    if form.validate():
        origin_filename = request.vars.dataset_upload.filename
        temp_filename = form.vars.dataset_upload
        logger.info("Validating {}...".format(origin_filename))
        logger.debug("(stored at {})".format(temp_filename))
        # Hacky method to open and read in whole file without actually using request.vars.dataset_upload.file.read()
        # Don't know why that method was giving inconsistent results, but this seems to work.
        with open(request.folder + "uploads/" + form.vars.dataset_upload) as candidate_src:
            candidate_reader = csv.reader(candidate_src, quotechar='"')
            candidate = [x for x in candidate_reader]
        if len(candidate) < 1:
            logger.warning(
                "Uploaded file {} (stored at {}) does not contain any information".format(
                    origin_filename,
                    temp_filename))
            report = "Uploaded file {} does not contain any information".format(origin_filename)
            failed = True
            validated = True
        elif len(candidate) == 1:
            logger.warning(
                "Uploaded file {} (stored at {}) does not contain both headers and values".format(
                    origin_filename,
                    temp_filename))
            report = "Uploaded file {} does not contain both headers and values".format(origin_filename)
            failed = True
            validated = True
        else:
            # Process
            candidate_len = len(candidate) - 1
            logger.debug("File length: {}".format(candidate_len))
            logger.debug("Header row length: {}".format(len(candidate[0])))
            logger.info("Verifying integrity of {}".format(origin_filename))
            logger.setLevel(logging.INFO)
            report, failed = vtfuncs.validate_vectraits(candidate, origin_filename)
            validated = True

    # if form.process().accepted:
    #     session.flash = 'form accepted'
    # elif form.errors:
    #     session.flash = 'form has errors'
    if validated and not failed:   # If report has been processed but did not fail
        session.flash = T("Dataset validated successfully.")
        session.current_origin_filename = origin_filename
        session.current_temp_filename = temp_filename
        session.current_file_length = candidate_len
        redirect(URL('vectraits', 'validation_successful'))
    elif validated and failed:
        import os
        logger.debug("Validation failed, removing temp file {}".format(temp_filename))
        try:
            os.remove(os.path.join(request.folder, "uploads", temp_filename))
        except OSError:
            logger.exception("Temp file not present upon post-validation delete")
    return dict(form=form, report=report)


def validation_successful():
    origin_filename = None
    temp_filename = None
    origin_filename = session.current_origin_filename
    temp_filename = session.current_temp_filename
    file_length = session.current_file_length
    if origin_filename and temp_filename:
        return dict(filename=B(origin_filename), tempname=B(temp_filename), file_length=B(file_length))
    else:
        logger.info("No origin or temp file found. Redirecting.")
        session.flash = CENTER(
            "Dataset not verified due to internal error. Please try again or contact the site administrators.",
            _style='color: red')
        redirect(URL('vectraits', 'index'))


@auth.requires_login()
def submit_dataset_for_upload():
    import os
    import shutil
    failed = False
    # Move file
    try:
        shutil.copy(
            os.path.join(request.folder, "uploads", session.current_temp_filename),
            os.path.join(request.folder, "uploads", "validated", session.current_temp_filename)
        )
        logger.debug("Dataset moved to submission file: {} -> {}".format(
            os.path.join(request.folder, "uploads", session.current_temp_filename),
            os.path.join(request.folder, "uploads", "validated", session.current_temp_filename)))
        os.remove(os.path.join(request.folder, "uploads", session.current_temp_filename))
        logger.debug("Deleting temp file {} from uploads".format(session.current_temp_filename))

    except IOError:
        logger.exception("Temp file not present upon post-validation copy")
        failed = True
    logger.debug("Resetting session filenames to None")
    # TODO: Don't actually want to do this resetting once dataset uploader is in place
    session.current_origin_filename = None
    session.current_temp_filename = None
    session.current_file_length = None
    if failed:
        session.flash = CENTER("Dataset not submitted due to internal error. Please try again or contact the site administrators.", _style='color: red')
    else:
        session.flash = T("Dataset submitted for upload.")
    redirect(URL('vectraits', 'index'))
    return True


def cancel_dataset_upload():
    import os
    logger.debug("Deleting temp file {}".format(session.current_temp_filename))
    try:
        os.remove(os.path.join(request.folder, "uploads", session.current_temp_filename))
    except OSError:
        logger.exception("Temp file not present upon post-validation delete")
    logger.debug("Resetting session filenames to None")
    session.current_origin_filename = None
    session.current_temp_filename = None
    session.current_file_length = None
    session.flash = T("Dataset upload cancelled.")
    redirect(URL('vectraits', 'index'))
    return True


def upload_vectraits():
    report = ""
    vtfuncs.upload_vectraits_dataset()
    return dict(report=report)
