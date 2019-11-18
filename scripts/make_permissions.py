from gluon.tools import Auth
from gluon import current
# import logzero


def construct_permissions():
    """Automatically construct permissions hierarchy"""
    # logger = logzero.setup_logger(logfile="web2py.log",
    #                                       formatter=logging.Formatter(
    #                                           '%(asctime)s - %(levelname)-7s - %(funcName)s - %(message)s'),
    #                                       disableStderrLogger=True)
    # logger.info("Constructing permissions system...")
    print("Constructing permissions system...")
    #
    # logger.info("Linking to db...")
    db = current.db
    auth = Auth(db)
    try:
        # logger.info("Creating user groups...")
        groupid_vbadmin = auth.add_group("VectorbiteAdmin", "Administrator group, has all permissions.")
        groupid_vdview = auth.add_group("VD Viewer", "Can view VecDyn.")
        groupid_vtview = auth.add_group("VT Viewer", "Can view VecTraits.")
        groupid_vdupload = auth.add_group("VD Uploader", "Can view and upload to VecDyn.")
        groupid_vtupload = auth.add_group("VT Uploader", "Can view and upload to VecTraits.")
        groupid_vdcurate = auth.add_group("VD Curator", "Can view, upload to, and curate VecDyn.")
        groupid_vtcurate = auth.add_group("VT Curator", "Can view, upload to, and curate VecTraits.")
        groupid_viewall = auth.add_group("View All", "Can view both databases.")

        # logger.info("Creating permissions...")
        # logger.debug("Adding permissions for Admin...")
        auth.add_permission(groupid_vbadmin, "view", "vecdyn")
        auth.add_permission(groupid_vbadmin, "upload", "vecdyn")
        auth.add_permission(groupid_vbadmin, "curate", "vecdyn")
        auth.add_permission(groupid_vbadmin, "view", "vectraits")
        auth.add_permission(groupid_vbadmin, "upload", "vectraits")
        auth.add_permission(groupid_vbadmin, "curate", "vectraits")

        # logger.debug("Adding permissions for View accounts...")
        auth.add_permission(groupid_vdview, "view", "vecdyn")

        auth.add_permission(groupid_vtview, "view", "vectraits")

        # logger.debug("Adding permissions for Upload accounts...")
        auth.add_permission(groupid_vdupload, "view", "vecdyn")
        auth.add_permission(groupid_vdupload, "upload", "vecdyn")

        auth.add_permission(groupid_vtupload, "view", "vectraits")
        auth.add_permission(groupid_vtupload, "upload", "vectraits")

        # logger.debug("Adding permissions for Curator accounts...")
        auth.add_permission(groupid_vdcurate, "view", "vecdyn")
        auth.add_permission(groupid_vdcurate, "upload", "vecdyn")
        auth.add_permission(groupid_vdcurate, "curate", "vecdyn")

        auth.add_permission(groupid_vtcurate, "view", "vectraits")
        auth.add_permission(groupid_vtcurate, "upload", "vectraits")
        auth.add_permission(groupid_vtcurate, "curate", "vectraits")

        # logger.debug("Adding permissions for Viewall account...")
        auth.add_permission(groupid_viewall, "view", "vecdyn")
        auth.add_permission(groupid_viewall, "view", "vectraits")

        # logger.info("Permission complete, comitting db...")
        db.commit()
    except Exception:
        # logger.exception("Encountered exception when constructing permissions system. Rolling back.")
        print("Encountered exception when constructing permissions system. Rolling back.")
        db.rollback()
    # logger.info("Permissions system created")
    return True


if __name__ == "__main__":
    construct_permissions()
