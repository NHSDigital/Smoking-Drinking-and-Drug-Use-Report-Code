import pytest
import pandas as pd
import numpy as np

# If rpy2/R aren't installed then skip these tests
try:
    import rpy2
    import rpy2.robjects as robjects
    from sdd_code.models.r_integration import r_to_py, py_to_r
except ImportError:
    rpy2 = None


@pytest.mark.skipif(
    rpy2 is None, reason="Skipping R integration tests if rpy2 is not installed"
)
def test_py_to_r():
    r = robjects.r
    input_py_df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4],
            "b": ["test", "test2", "string", "blah"],
            "c": [0.1, 4.2, 0.1, 4.2],
        }
    )

    expected_R_df = r["data.frame"](
        a=r.c(1, 2, 3, 4),
        b=r.c("test", "test2", "string", "blah"),
        c=r.c(0.1, 4.2, 0.1, 4.2),
    )

    actual_R_df = py_to_r(input_py_df)

    assert r.isTRUE(r["all.equal"](expected_R_df, actual_R_df))


@pytest.mark.skipif(
    rpy2 is None, reason="Skipping R integration tests if R is not installed"
)
def test_r_to_py():
    r = robjects.r
    input_R_df = r["data.frame"](
        a=r.c(1, 2, 3, 4),
        b=r.c("test", "test2", "string", "blah"),
        c=r.c(0.1, 4.2, 0.1, 4.2),
    )

    expected_py_df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4],
            "b": ["test", "test2", "string", "blah"],
            "c": [0.1, 4.2, 0.1, 4.2],
        }
    )

    actual_py_df = (
        r_to_py(input_R_df)
        .reset_index(drop=True)
        .astype(
            {
                "a": np.int64,
                "c": np.float64,
            }
        )
    )

    pd.testing.assert_frame_equal(expected_py_df, actual_py_df)
