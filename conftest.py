"""Configuration functioons for pytest

Enables --sdd_file='...' argument and --sdd_metadata='....' on pytest command line
"""


def pytest_addoption(parser):
    parser.addoption("--sdd_file", action="append", default=[])
    parser.addoption("--sdd_metadata", action="append", default=[])


def pytest_generate_tests(metafunc):
    custom_arguments = ["sdd_file", "sdd_metadata"]
    for arg in custom_arguments:
        if arg in metafunc.fixturenames:
            if metafunc.config.getoption(arg):
                metafunc.parametrize(
                    arg, metafunc.config.getoption(arg), scope="session"
                )
            else:
                metafunc.parametrize(arg, [None], scope="session")
