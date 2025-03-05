import os
from sdd_code.utilities import parameters as param
from pathlib import Path


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


def set_r_home():
    """Set the environment variable R_HOME to a specific R installation directory.
    Modify the path as needed based on the R version and installation location.
    """
    # Specify the R home directory based on your setup
    r_home_path = Path('BaseDirectory + param.R_VERSION)
    # Update this to the appropriate R installation

    if r_home_path.is_dir():
        os.environ["R_HOME"] = str(r_home_path)
    else:
        raise FileNotFoundError(f"R_HOME path '{r_home_path}' does not exist.")

        set_r_home()


set_r_home()
