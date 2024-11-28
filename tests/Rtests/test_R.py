import pytest

from sdd_code.utilities import parameters as param

# If rpy2/R aren't installed then skip these tests
try:
    import rpy2
    import rpy2.robjects as robjects
except ImportError:
    rpy2 = None


@pytest.mark.skipif(
    rpy2 is None, reason="Skipping R integration tests if rpy2 is not installed"
)
def test_testthat():
    r = robjects.r
    R_tests = param.LOCAL_ROOT / "sdd_code" / "sddR" / "tests" / "testthat.R"

    try:
        r.source(R_tests.as_posix())
        tests_passed = True
    except rpy2.rinterface_lib.embedded.RRuntimeError:
        tests_passed = False

    assert tests_passed, "R testthat tests failed, run in RStudio to evaluate and fix"
