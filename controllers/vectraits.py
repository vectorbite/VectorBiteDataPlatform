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
