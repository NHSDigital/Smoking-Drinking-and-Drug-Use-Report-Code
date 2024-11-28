import os
from sdd_code.utilities import parameters as param


def set_r_libs():
    """Set the environment variable R_LIBS_USER to a local renv library.
    Checks for survey package to validate library, if not installed then
    will not change R_LIBS_USER.
    """
    lib_root = param.LOCAL_ROOT / "sdd_code" / "sddR" / "renv" / "library"

    if not lib_root.exists():
        return

    libs_user = None
    r_versions = (x for x in lib_root.iterdir() if x.is_dir())
    for r_folder in r_versions:
        libs = (x for x in r_folder.iterdir() if x.is_dir())
        for lib_folder in libs:
            if lib_folder.glob("survey"):
                libs_user = lib_folder.as_posix()
                break
    if libs_user is None:
        return
    else:
        os.environ["R_LIBS_USER"] = libs_user


set_r_libs()
