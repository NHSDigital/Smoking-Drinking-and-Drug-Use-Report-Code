from pathlib import Path
import sdd_code.utilities.parameters as param
import os


def set_r_home():
    """Set the environment variable R_HOME to a specific R installation directory.
    Modify the path as needed based on the R version and installation location.
    """
    # Specify the R home directory based on your setup
    r_home_path = Path('BaseDirectory' + param.R_VERSION)
    # Update this to the appropriate R installation

    if r_home_path.is_dir():
        os.environ["R_HOME"] = str(r_home_path)
    else:
        raise FileNotFoundError(f"R_HOME path '{r_home_path}' does not exist.")

        set_r_home()


set_r_home()
