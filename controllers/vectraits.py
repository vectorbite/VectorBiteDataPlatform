def view_citations():
    # create the SQLFORM grid to show the existing assignments
    # and set up actions to be applied to selected rows - these
    # are powered by action functions defined below
    grid = SQLFORM.grid(db2.citation,
                        csv=True,
                        deletable=False,
                        create=False,
                        details=False,
                        editable=False,
                        # links=links,
                        paginate=False)

    return dict(form=grid)