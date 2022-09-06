import pandas as pd
import pytest

from sdd_code.utilities import derivations
from sdd_code.utilities import parameters as param


def test_age1115():
    """
    Tests age 11-15 derivation has been implemented correctly

    df.loc[df["age"] < 0, "age1115"] = df["age"]
    df.loc[(df["age"] > 0) & (df["age"] < 11), "age1115"] = 11
    df.loc[(df["age"] > 10) & (df["age"] < 16), "age1115"] = df["age"]
    df.loc[df["age"] > 14, "age1115"] = 15

    return df
    """

    input_df = pd.DataFrame({"age": [20, 10, 12, 14, 15, 16, 17, -1]})
    return_df = derivations.age1115(input_df)

    expected = [15, 11, 12, 14, 15, 15, 15, -1]
    actual = list(return_df['age1115'].astype(int))

    assert actual == expected, f"When checking for age11_15, expected to find {expected} but found {actual}"


def test_age1215():

    input_df = pd.DataFrame({"age": [10, 11, 12, 14, 15, 16, 17, -1]})
    return_df = derivations.age1215(input_df)

    expected = [12, 12, 12, 14, 15, 15, 15, -1]
    actual = list(return_df['age1215'].astype(int))

    assert actual == expected, f"When checking for age1215, expected to find {expected} but found {actual}"


def test_age1315():
    """
    Tests age 13-15 derivation has been implemented correctly

    df.loc[df["age"] < 10, "age1315"] = df["age"]
    df.loc[df["age"].isin([10, 11, 12]), "age1315"] = 13
    df.loc[(df["age"] > 12) & (df["age"] < 16), "age1315"] = df["age"]
    df.loc[df["age"] > 15, "age1315"] = 15

    return df
    """

    input_df = pd.DataFrame({"age": [20, 9, 10, 11, 12, 14, 15, 16, 17, -1]})
    return_df = derivations.age1315(input_df)

    expected = [15, 13, 13, 13, 13, 14, 15, 15, 15, -1]
    actual = list(return_df['age1315'].astype(int))

    assert actual == expected, f"When checking for age13_15, expected to find {expected} but found {actual}"


def test_dallast3():

    input_df = pd.DataFrame({"alevr": [1, 1, 1, 1, 1, -8, -9, 1, 1, 2],
                             "allast": [1, 2, 3, 4, 5, -1, -1, 6, 7, -1]})
    return_df = derivations.dallast3(input_df)

    expected = [1, 1, 1, 2, 2, -8, -9, 2, 2, 3]
    actual = list(return_df['dallast3'].astype(int))

    assert actual == expected, f"When checking for dallast3, expected to find {expected} but found {actual}"


def test_dallast5():

    input_df = pd.DataFrame({"alevr": [1, 1, 1, 1, 1, -8, -9, 1, 1, 2],
                             "allast": [1, 2, 3, 4, 5, -1, -1, 6, 7, -1]})
    return_df = derivations.dallast5(input_df)

    expected = [1, 1, 1, 2, 2, -8, -9, 3, 4, 5]
    actual = list(return_df['dallast5'].astype(int))

    assert actual == expected, f"When checking for dallast5, expected to find {expected} but found {actual}"


def test_dalagedru():
    
    input_df = pd.DataFrame({"alagednk": [-9, -1, 0, 2, 4, 10, 11, 12, 14, 16, 15]})
    return_df = derivations.dalagedru(input_df)

    expected = [-9, -1, 10, 10, 10, 10, 11, 12, 14, 15, 15]
    actual = return_df["dalagedru"].astype(int).to_list()

    assert actual == expected


def test_daldrunk():

    input_df = pd.DataFrame({"alevr": [1, 1, 1, 2, -1],
                             "alevrdnk": [1, 2, -9, -1, 1]})
    return_df = derivations.daldrunk(input_df)

    expected = [2, 1, -9,  3, -1]
    actual = list(return_df['daldrunk'].astype(int))

    assert actual == expected, f"When checking for daldrunk, expected to find {expected} but found {actual}"


def test_dal7beer():
    input_df = pd.DataFrame({"al7beer": [-9, 1, 2, 3, -1]})
    return_df = derivations.dal7beer(input_df)

    expected = [-9, 1, 1, 2, -1]
    actual = return_df["dal7beer"].astype(int).to_list()

    assert actual == expected, f"When checking for dal7beer, expected to find {expected} but found {actual}"


def test_dal7shan():
    input_df = pd.DataFrame({"al7shan": [-9, 1, 2, 3, -1]})
    return_df = derivations.dal7shan(input_df)

    expected = [-9, 1, 1, 2, -1]
    actual = return_df["dal7shan"].astype(int).to_list()

    assert actual == expected, f"When checking for dal7shan, expected to find {expected} but found {actual}"


def test_dal7winsh():
    input_df = pd.DataFrame({"al7winsh": [-9, 1, 2, 3, -1]})
    return_df = derivations.dal7winsh(input_df)

    expected = [-9, 1, 1, 2, -1]
    actual = return_df["dal7winsh"].astype(int).to_list()

    assert actual == expected, f"When checking for dal7winsh, expected to find {expected} but found {actual}"


def test_dal7spir():
    input_df = pd.DataFrame({"al7spir": [-9, 1, 2, 3, -1]})
    return_df = derivations.dal7spir(input_df)

    expected = [-9, 1, 1, 2, -1]
    actual = return_df["dal7spir"].astype(int).to_list()

    assert actual == expected, f"When checking for dal7spir, expected to find {expected} but found {actual}"


def test_dal7pops():
    input_df = pd.DataFrame({"al7pops": [-9, 1, 2, 3, -1]})
    return_df = derivations.dal7pops(input_df)

    expected = [-9, 1, 1, 2, -1]
    actual = return_df["dal7pops"].astype(int).to_list()

    assert actual == expected, f"When checking for dal7pops, expected to find {expected} but found {actual}"


def test_dal7any():
    input_df = pd.DataFrame({"dallast5": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, -9],
                             "dal7beer": [-9, 1, -9, -9, -9, -9, 1, -9, -9, -9, -9, -9],
                             "dal7shan": [-9, -9, 2, -9, -9, -9, -9, 2, -9, -9, -9, -9],
                             "dal7winsh": [-9, -9, -9, 1, -9, -9, -9, -9, 1, -9, -9, -9],
                             "dal7spir": [-9, -9, -9, -9, 1, -9, -9, -9, -9, 1, -9, -9],
                             "dal7pops": [-9, -9, -9, -9, -9, 2, -9, -9, -9, -9, 2, -9]})
    return_df = derivations.dal7any(input_df)

    expected = [-9, 1, 1, 1, 1, 1, -9, -9, -9, -9, -9, -9]
    actual = return_df["dal7any"].astype(int).to_list()

    assert actual == expected, f"When checking for dal7any, expected to find {expected} but found {actual}"


def test_dagedrank():
    input_df = pd.DataFrame({"alage": [-1, -9, 0, 3, 5, 8, 10, 11, 12, 13, 14,
                                       15, 16]})
    return_df = derivations.dagedrank(input_df)

    expected = [-1, -9, 10, 10, 10, 10, 10, 11, 12, 13, 14, 15, 15]
    actual = return_df["dagedrank"].astype(int).to_list()

    assert actual == expected, f"When checking for dagedrank, expected to find {expected} but found {actual}"


def test_dalunitsday():

    input_df = pd.DataFrame({"nal7ut": [-9,  1, -9, 0, 1, 1, 3, 3, 8, 5, 15],
                             "al7day": [-9, -9,  1, 1, 2, 1, 2, 1, 2, 1, 2]})

    return_df = derivations.dalunitsday(input_df)

    expected = [-9, -9, -9, 1, 1, 2, 2, 3, 3, 4, 4]
    actual = return_df["dalunitsday"].astype(int).to_list()

    assert actual == expected, f"When checking for dalunitsday, expected to find {expected} but found {actual}"


def test_nal7br():
    input_df = pd.DataFrame({"alevr": [-9, 1, 1, 1, 1, 1, 1],
                             "allast": [-9, 1, 3, 3, 1, 2, 3],
                             "al7beer": [-9, -9, 2, 1, 1, 1, 1],
                             "albrstr": [-9, -9, 1, 1, 2, 3, 1],
                             "al7brbt": [-8, 0, 0, 1, 1, 1, 0],
                             "al7brhp": [-9, 0, 0, 1, 1, 1, 0],
                             "al7brlg": [-8, 0, 0, 1, 1, 1, 0],
                             "al7brpt": [-9, 0, 0, 1, 1, 1, 0],
                             "al7brsm": [-9, 0, 0, 1, 1, 1, 0]})
    return_df = derivations.nal7br(input_df)

    expected = [-9, -9, 0.5, 8, 12, 10, 0]
    actual = return_df["nal7br"].astype(float).to_list()

    assert actual == expected, f"When checking for nal7br, expected to find {expected} but found {actual}"


def test_nal7pp():
    input_df = pd.DataFrame({"alevr": [-9, 1, 1, 1, 1],
                             "allast": [-9, 1, 3, 3, 2],
                             "al7pops": [-9, -9, 2, 1, 1],
                             "al7ppcn": [-9, 0, 0, 1, 0],
                             "al7ppbt": [-8, 0, 0, 1, 0]})
    return_df = derivations.nal7pp(input_df)

    expected = [-9, -9, 0.75, 3, 0]
    actual = return_df["nal7pp"].astype(float).to_list()

    assert actual == expected, f"When checking for nal7pp, expected to find {expected} but found {actual}"


def test_nal7sd():
    input_df = pd.DataFrame({"alevr": [-9, 1, 1, 1, 1],
                             "allast": [-9, 1, 3, 3, 2],
                             "al7shan": [-9, -9, 2, 1, 1],
                             "al7sdpt": [-9, 0, 0, 1, 0],
                             "al7sdhp": [-8, 0, 0, 1, 0]})
    return_df = derivations.nal7sd(input_df)

    expected = [-9, -9, 0.25, 1.5, 0]
    actual = return_df["nal7sd"].astype(float).to_list()

    assert actual == expected, f"When checking for nal7sd, expected to find {expected} but found {actual}"


def test_nal7sp():
    input_df = pd.DataFrame({"alevr": [-9, 1, 1, 1, 1],
                             "allast": [-9, 1, 3, 3, 2],
                             "al7spir": [-9, -9, 2, 1, 1],
                             "al7spgs": [-9, 0, 0, 1, 0]})
    return_df = derivations.nal7sp(input_df)

    expected = [-9, -9, 0.5, 1, 0]
    actual = return_df["nal7sp"].astype(float).to_list()

    assert actual == expected, f"When checking for nal7sp, expected to find {expected} but found {actual}"


def test_nal7winsh():
    input_df = pd.DataFrame({"alevr": [-9, 1, 1, 1, 1],
                             "allast": [-9, 1, 3, 3, 2],
                             "al7winsh": [-9, -9, 2, 1, 1],
                             "al7wnshgs": [-8, 0, 0, 1, 0]})
    return_df = derivations.nal7winsh(input_df)

    expected = [-9, -9, 1, 2, 0]
    actual = return_df["nal7winsh"].astype(float).to_list()

    assert actual == expected, f"When checking for nal7winsh, expected to find {expected} but found {actual}"


def test_nal7ut():
    input_df = pd.DataFrame({"alevr":  [-9, 1, 1, 1, 1, 1, 1, 1, 1],
                             "allast": [-1, -9, 1, 1, 1, 1, 1, 1, 1],
                             "nal7br": [-1, 1, -9, 2, 2, 2, 2, 2, 0],
                             "nal7pp": [-1, 2, 2, -9, 3, 3, 3, 2, 0],
                             "nal7sd": [-1, 3, 3, 3, -9, 4, 4, 2, 0],
                             "nal7sp": [-1, 4, 4, 4, 4, -9, 5, 2, 0],
                             "nal7winsh": [-1, 5, 5, 5, 5, 5, -9, 2, 0]})
    return_df = derivations.nal7ut(input_df)

    expected = [-9, -9, -9, -9, -9, -9, -9, 10, 0]
    actual = return_df["nal7ut"].astype(float).to_list()

    assert actual == expected, f"When checking for nal7ut, expected to find {expected} but found {actual}"


def test_nal7utg():
    input_df = pd.DataFrame({"nal7ut": [-9, -1, -8, 0, 3, 8, 22, 100]})
    return_df = derivations.nal7utg(input_df)

    expected = [-9, -1, -8, 1, 2, 3, 4, 4]
    actual = return_df["nal7utg"].astype(int).to_list()

    assert actual == expected, f"When checking for nal7utg, expected to find {expected} but found {actual}"


def test_nal7utg4():
    input_df = pd.DataFrame({"nal7ut": [-9, -1, -8, 0, 3, 8, 12, 100]})
    return_df = derivations.nal7utg4(input_df)

    expected = [-9, -1, -8, 1, 2, 3, 4, 4]
    actual = return_df["nal7utg4"].astype(int).to_list()

    assert actual == expected, f"When checking for nal7utg4, expected to find {expected} but found {actual}"


def test_nal7utg7():
    input_df = pd.DataFrame({"nal7ut": [-9, -1, -8, 0.5, 1, 2.5, 3.5, 5, 7.5, 11, 50]})
    return_df = derivations.nal7utg7(input_df)

    expected = [-9, -1, -8, 1, 2, 3, 3, 4, 5, 6, 7]
    actual = return_df["nal7utg7"].astype(int).to_list()

    assert actual == expected, f"When checking for nal7utg7, expected to find {expected} but found {actual}"


def test_dalshop4():
    input_df = pd.DataFrame({"altry4": [-9, -8, -1, 1, 1, 2, 1, 1],
                             "altryshp": [-1, -1, -1, 1, 1, -1, 2, 1],
                             "alacbs4": [-1, -1, -1, 1, 2, -1, -1, -9]})
    return_df = derivations.dalshop4(input_df)

    expected = [-9, -8, -1, 1, 2, 2, 2, -9]
    actual = return_df["dalshop4"].astype(int).to_list()

    assert actual == expected, f"When checking for dalshop4, expected to find {expected} but found {actual}"


def test_dalpub4():
    input_df = pd.DataFrame({"altry4": [-9, -8, -1, 1, 1, 2, 1, 1],
                             "altrypub": [-1, -1, -1, 1, 1, -1, 2, 1],
                             "alacbp4": [-1, -1, -1, 1, 2, -1, -1, -9]})
    return_df = derivations.dalpub4(input_df)

    expected = [-9, -8, -1, 1, 2, 2, 2, -9]
    actual = return_df["dalpub4"].astype(int).to_list()

    assert actual == expected, f"When checking for dalpub4, expected to find {expected} but found {actual}"


def test_dalgot4():
    input_df = pd.DataFrame({"dalshop4": [2, 1, -9, 2, -9, -1],
                             "dalpub4": [2, 2, -9, 2, 1, -1],
                             "altryels": [2, 2, 1, 2, 1, -1],
                             "algivpar": [2, 2, -9, -9, 1, -1],
                             "algivfre": [2, 2, -9, 2, 1, -1],
                             "algivrel": [2, -9, -9, 2, 1, -1],
                             "algivsib": [2, 2, -9, 2, 1, -1],
                             "algivoth": [2, 2, -9, 2, 1, -1],
                             "altakhom": [2, -9, -9, 2, 1, -1],
                             "altakfre": [2, 2, -9, 2, 2, -1],
                             "alstlhom": [2, 2, -8, 2, 2, -1],
                             "alstlfre": [2, -8, -9, 2, 2, -1],
                             "alstloth": [2, 2, -9, 2, 1, -1]})
    return_df = derivations.dalgot4(input_df)

    expected = [2, 1, 1, -9, 1, -1]
    actual = return_df["dalgot4"].astype(int).to_list()

    assert actual == expected, f"When checking for dalgot4, expected to find {expected} but found {actual}"


def test_dal4dru6():
    input_df = pd.DataFrame({"alevr":   [2, 1, -9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                             "allast":  [-1, 6, -1, -9, 1, 1, 1, 1, 1, 1, 1, 1],
                             "al4wdru": [-1, 1, -1, 1, -9, 2, 1, 1, 1, 1, 1, 1],
                             "al4wfrq": [-1, 1, -1, 1, 1, 1, 0, 1, 2, 3, 10, -9]})

    return_df = derivations.dal4dru6(input_df)

    expected = [5, 5, -9, -9, -9, 1, 1, 2, 2, 3, 4, 6]
    actual = return_df["dal4dru6"].astype(int).to_list()

    assert actual == expected, f"When checking for dal4dru6, expected to find {expected} but found {actual}"


def test_dal4dru5():

    input_df = pd.DataFrame({"dal4dru6": [1, 2, 3, 4, 5, 6, -1]})

    return_df = derivations.dal4dru5(input_df)

    expected = [1, 2, 3, 3, 5, 6, -1]
    actual = list(return_df['dal4dru5'].astype(int))

    assert actual == expected, f"When checking for dal4dru5, expected to find {expected} but found {actual}"


def test_dalbuyper():
    input_df = pd.DataFrame({"albuyels":   [1, 0, 0, 0, -9, -9],
                             "albuyfre":  [0, 1, 0, 0, 1, 0],
                             "albuystr": [0, 1, 1, 0, 0, 0]})

    return_df = derivations.dalbuyper(input_df)

    expected = [1, 1, 1, 0, 1, -9]
    actual = return_df["dalbuyper"].astype(int).to_list()

    assert actual == expected, f"When checking for dalbuyper, expected to find {expected} but found {actual}"


def test_dalbuyret():
    input_df = pd.DataFrame({"albuyoff":   [1, 0, 0, 0, -9, -9],
                             "albuyshp":  [0, 0, 0, 0, 1, 0],
                             "albuygar":  [0, 1, 0, 0, 0, 0],
                             "albuypub":  [0, 0, 0, 0, -9, 0],
                             "albuyclu": [0, 1, 1, 0, 0, 0]})

    return_df = derivations.dalbuyret(input_df)

    expected = [1, 1, 1, 0, 1, -9]
    actual = return_df["dalbuyret"].astype(int).to_list()

    assert actual == expected, f"When checking for dalbuyret, expected to find {expected} but found {actual}"


def test_dalushmo():

    input_df = pd.DataFrame({"alushom": [-9,  1, -9, 0, 0, -1],
                             "alusohm": [-9, -9,  1, 1, 0, -1]})

    return_df = derivations.dalushmo(input_df)

    expected = [-9, 1, 1, 1, 0, -1]
    actual = return_df["dalushmo"].astype(int).to_list()

    assert actual == expected, f"When checking for dalushmo, expected to find {expected} but found {actual}"


def test_daluswho():

    input_df = pd.DataFrame({"alownoth": [1,  1, 2, 2, -9, -1],
                             "aluspar": [1, -9,  1, -9, 0, -1],
                             "alussib": [0, -9,  0, 0, 0, -1],
                             "alusfreb": [0, -9,  0, 1, 0, -1],
                             "alusfreo": [0, -9,  1, 0, 1, -1],
                             "alusfres": [0, -9,  0, 0, 1, -1],
                             "alusgb": [0, -9,  1, -9, 0, -1],
                             "alusoth": [0, -9,  1, 0, -9, -1]})

    return_df = derivations.daluswho(input_df)

    expected = pd.DataFrame(
        {
            "daluspar": [0, 0, 1, -9, 0, -1],
            "dalussib": [0, 0, 0, 0, 0, -1],
            "dalusfreb": [0, 0, 0, 1, 0, -1],
            "dalusfreo": [0, 0, 1, 0, 1, -1],
            "dalusfres": [0, 0, 0, 0, 1, -1],
            "dalusgb": [0, 0, 1, -9, 0, -1],
            "dalusoth": [0, 0, 1, 0, -9, -1]
        }
    ).astype(int)
    actual = return_df[["daluspar", "dalussib", "dalusfreb", "dalusfreo",
                       "dalusfres", "dalusgb", "dalusoth"]].astype(int)

    pd.testing.assert_frame_equal(actual, expected)


def test_dalusfre():

    input_df = pd.DataFrame({"alownoth":   [1, 2, 2, 2, -9],
                             "alusfreb":  [1, 0, 0, 0, 0],
                             "alusfreo":  [0, 1, -9, 0, 1],
                             "alusfres": [0, 1, 0, 0, 0],
                             "alusgb": [0, -9, 0, 0, 1]})

    return_df = derivations.dalusfre(input_df)

    expected = [0, 1, -9, 0, 1]
    actual = return_df["dalusfre"].astype(int).to_list()

    assert actual == expected, f"When checking for dalusfre, expected to find {expected} but found {actual}"


def test_dallastwk():

    input_df = pd.DataFrame({"dallast5": [1, 2, 3, 4, 5, -8, -9]})

    return_df = derivations.dallastwk(input_df)

    expected = [1, 0, 0, 0, 0, -9, -9]
    actual = return_df["dallastwk"].astype(int).to_list()

    assert actual == expected, f"When checking for dallastwk, expected to find {expected} but found {actual}"


def test_ethnicgp5():

    input_df = pd.DataFrame({"ethnic": [1, 4, 11, 2, 17, -8, -9, 5, 15]})

    return_df = derivations.ethnicgp5(input_df)

    expected = [1, 1, 3, 1, 5, -8, -9, 2, 4]
    actual = return_df["ethnicgp5"].astype(int).to_list()

    assert actual == expected, f"When checking for ethnicgp5, expected to find {expected} but found {actual}"


def test_ethnicgp4():

    input_df = pd.DataFrame({"ethnicgp5": [1, 1, 3, 1, 5, -8, -9, 2, 4]})

    return_df = derivations.ethnicgp4(input_df)

    expected = [1, 1, 3, 1, 4, -8, -9, 2, 4]
    actual = return_df["ethnicgp4"].astype(int).to_list()

    assert actual == expected, f"When checking for ethnicgp4, expected to find {expected} but found {actual}"


def test_dalfam():
    input_df = pd.DataFrame({"alevr":   [1, 1, 2, 1, -9, 2],
                             "alparst":  [-1, -1, 3, -1, -1, -9],
                             "alpar":  [-1, 1, -1, 4, -1, -1],
                             "alparknw": [-1, -9, -1, 2, -1, -1]})

    return_df = derivations.dalfam(input_df)

    expected = [-1, 1, 3, 2, -9, -9]
    actual = return_df["dalfam"].astype(int).to_list()

    assert actual == expected, f"When checking for dalfam, expected to find {expected} but found {actual}"


def test_dalfamknw():
    input_df = pd.DataFrame({"alevr":   [-9, 1, 2, 1, 1, 1, 1, 1],
                             "alfreq":  [-1, -9, -1, 2, 3, 1, 4, 2],
                             "alpar":  [-1, -9, -1, -9, 1, 2, 3, 4]})

    return_df = derivations.dalfamknw(input_df)

    expected = [-9, -9, -1, -9, 1, 1, 1, 2]
    actual = return_df["dalfamknw"].astype(int).to_list()

    assert actual == expected, f"When checking for dalfamknw, expected to find {expected} but found {actual}"


def test_dfamdrin():
    input_df = pd.DataFrame({"alwhodr": [-9, -1, -8, 0, 1, 2, 3, 6]})
    return_df = derivations.dfamdrin(input_df)

    expected = [-9, -1, -8, 0, 1, 2, 3, 3]
    actual = return_df["dfamdrin"].astype(int).to_list()

    assert actual == expected, f"When checking for dfamdrin, expected to find {expected} but found {actual}"


def test_ddgany(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [4, -9, 4, -8, 4, 4, 4, -9, 4, 4, 4, -8, -8, 4, -9, -9, 4],
            [4, -9, 4, -9, 4, -9, -9, 4, -9, 4, -9, -9, -9, 4, -9, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [3, 4, 3, 2, 3, 3, -8, 2, 3, 2, 4, 4, 1, 1, -9, 3, 3],
        ]
    )
    return_df = derivations.ddgany(input_df)

    expected = [-8, -9, 0, 1]
    actual = return_df["ddgany"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgany, expected to find {expected} but found {actual}"


def test_ddgyrany(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [4, -9, 4, -8, 3, 4, 4, -9, 4, 3, 4, -8, -8, 3, -9, -9, 4],
            [4, -9, 4, -9, 3, -9, -9, 4, -9, 3, -9, -9, -9, 4, -9, 4, 4],
            [4, 3, 4, 4, 3, 3, 4, 4, 4, 3, 4, 4, 4, 3, 4, 4, 4],
            [3, 4, 3, 2, 3, 3, -8, 2, 3, 2, 4, 4, 1, 1, -9, 3, 3],
        ]
    )
    return_df = derivations.ddgyrany(input_df)

    expected = [-8, -9, 0, 1]
    actual = return_df["ddgyrany"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyrany, expected to find {expected} but found {actual}"


def test_ddgmonany(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [2, -9, 4, -8, 3, 2, 4, -9, 4, 3, 4, -8, -8, 2, -9, -9, 4],
            [4, -9, 4, -9, 2, -9, -9, 2, -9, 3, -9, -9, -9, 2, -9, 4, 4],
            [4, 3, 4, 4, 3, 2, 2, 2, 4, 3, 4, 4, 4, 3, 4, 2, 4],
            [3, 4, 3, 2, 3, 3, -8, 2, 3, 2, 4, 4, 1, 1, -9, 3, 3],
        ]
    )
    return_df = derivations.ddgmonany(input_df)

    expected = [-8, -9, 0, 1]
    actual = return_df["ddgmonany"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmonany, expected to find {expected} but found {actual}"


def test_ddgdrugs():
    input_df = pd.DataFrame(
        {
            "ddgmonany": [1, 2, -8, 2, 2, 2],
            "ddgyrany": [2, 1, 2, 2, -9, 2],
            "ddgany": [-9, 2, 1, 2, -8, -8]
        }
    )
    return_df = derivations.ddgdrugs(input_df)

    expected = [4, 3, 2, 1, -9, -8]
    actual = return_df["ddgdrugs"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgdrugs, expected to find {expected} but found {actual}"


def test_dcgstg2():
    input_df = pd.DataFrame(
        {
            "cgstat": [1, 1, 2, 3, 4, 4, 5, 6, -9, -8],
            "cgireg": [2, 1, 2, 3, 1, 3, 1, 2, -8, -9],
            "cg7": [1, 1, 1, 1, 2, 2, 2, 2, -9, -8],
            "cg7mon": [1, 2, 0, 0, 0, 0, 0, 0, -9, -0],
            "cg7tue": [2, 0, 0, 0, 0, 0, 1, 0, -9, -8],
            "cg7wed": [5, 0, 0, 0, 0, 0, 2, 0, 1, -4],
            "cg7thu": [3, 0, 0, 0, 0, 0, 0, 0, -9, -8],
            "cg7fri": [2, 1, 0, 0, 2, 0, 0, 0, -9, -1],
            "cg7sat": [6, 0, 0, 0, 0, 0, 0, 0, 2, -8],
            "cg7sun": [1, 0, 0, 0, 0, 1, 0, 0, -9, 0],
        }
    )
    return_df = derivations.dcgstg2(input_df)

    expected = [1, 1, 2, 1, 1, 1, 1, 2, -9, -8]
    actual = return_df["dcgstg2"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgstg2, expected to find {expected} but found {actual}"


def test_dcgstg3():
    input_df = pd.DataFrame(
        {
            "cgstat": [1, 1, 2, 3, 4, 4, 5, 6, -9, -8],
            "cgireg": [2, 1, 2, 3, 1, 3, 1, 2, -8, -9],
            "cg7": [1, 1, 1, 1, 2, 2, 2, 2, -9, -8],
            "cg7mon": [1, 2, 0, 0, 0, 0, 0, 0, -9, -0],
            "cg7tue": [2, 0, 0, 0, 0, 0, 1, 0, -9, -8],
            "cg7wed": [5, 0, 0, 0, 0, 0, 2, 0, 1, -4],
            "cg7thu": [3, 0, 0, 0, 0, 0, 0, 0, -9, -8],
            "cg7fri": [2, 1, 0, 0, 2, 0, 0, 0, -9, -1],
            "cg7sat": [6, 0, 0, 0, 0, 0, 0, 0, 2, -8],
            "cg7sun": [1, 0, 0, 0, 0, 1, 0, 0, -9, 0],
        }
    )
    return_df = derivations.dcgstg3(input_df)

    expected = [2, 2, 3, 2, 2, 2, 1, 3, -9, -8]
    actual = return_df["dcgstg3"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgstg3, expected to find {expected} but found {actual}"


def test_dcgstg5():
    input_df = pd.DataFrame(
        {
            "cgstat": [1, 1, 2, 3, 4, 4, 5, 6, -9, -8, 3, 1],
            "cgireg": [2, 1, 2, 3, 1, 3, 1, 2, -8, -9, -1, -1],
            "cg7": [1, 1, 1, 1, 2, 2, 2, 2, -9, -8, 2, 2],
            "cg7mon": [1, 2, 0, 0, 0, 0, 0, 0, -9, -0, 0, 0],
            "cg7tue": [2, 0, 0, 0, 0, 0, 1, 0, -9, -8, 0, 0],
            "cg7wed": [5, 0, 0, 0, 0, 0, 2, 0, 1, -4, 0, 0],
            "cg7thu": [3, 0, 0, 0, 0, 0, 0, 0, -9, -8, 0, 0],
            "cg7fri": [2, 1, 0, 0, 2, 0, 0, 0, -9, -1, 0, 0],
            "cg7sat": [6, 0, 0, 0, 0, 0, 0, 0, 2, -8, 0, 0],
            "cg7sun": [1, 0, 0, 0, 0, 1, 0, 0, -9, 0, 0, 0],
        }
    )
    return_df = derivations.dcgstg5(input_df)

    expected = [2, 2, 4, 2, 2, 2, 1, 4, -9, -8, 3, 5]
    actual = return_df["dcgstg5"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgstg5, expected to find {expected} but found {actual}"


def test_dusexxx(all_drugs=param.DRUGS):

    drug_freq = ["dgfq" + drug for drug in all_drugs]
    drug_heard = ["dghd" + drug for drug in all_drugs]
    drug_tried = ["dgtd" + drug for drug in all_drugs]
    drug_use = ["duse" + drug for drug in all_drugs]

    test_df_list = []
    expected_df_list = []
    # Create the new duseXXX column for each drug
    for dgfq, dghd, dgtd, duse in zip(drug_freq, drug_heard, drug_tried, drug_use):
        test_df = pd.DataFrame({
            dgfq: [1, 2, 3, -8, -9, 3, 1, 2, 3],
            dghd: [-8, -9, 2, 1, 1, 1, 1, 1, 1],
            dgtd: [1, 2, 1, 2, -8, -9, 1, 1, 1],
        })
        expected_df = pd.DataFrame({
            dgfq: [1, 2, 3, -8, -9, 3, 1, 2, 3],
            dghd: [-8, -9, 2, 1, 1, 1, 1, 1, 1],
            dgtd: [1, 2, 1, 2, -8, -9, 1, 1, 1],
            duse: [-8, -9, 4, 4, -8, -9, 1, 2, 3]
        })
        test_df_list.append(test_df)
        expected_df_list.append(expected_df)

    input_df = pd.concat(test_df_list, axis=1)
    expected = pd.concat(expected_df_list, axis=1)
    actual = derivations.dusexxx(input_df)

    expected = expected.reindex(sorted(expected.columns), axis=1)
    actual = actual.reindex(sorted(actual.columns), axis=1)

    pd.testing.assert_frame_equal(actual, expected)


def test_dfas():
    input_df = pd.DataFrame(
        {
            "ownbed": [-9, 2, 2, 2, 1],
            "fambath": [-8, -8, 1, 1, 2],
            "famdish": [-1, -1, -1, 2, 1],
            "famhols": [1, 1, 1, 1, 2],
            "famcomp": [1, 1, 1, 1, 2],
            "famcars": [1, 1, 1, 1, 2]
        }
    )
    return_df = derivations.dfas(input_df)

    expected = [-9, -8, -1, 0, 6]
    actual = return_df["dfas"].astype(int).to_list()

    assert actual == expected, f"When checking for dfas, expected to find {expected} but found {actual}"


def test_dfasbands():
    input_df = pd.DataFrame({"dfas": [-9, -8, 0, 6, 7, 10, 11, 12]})
    return_df = derivations.dfasbands(input_df)

    expected = [-9, -8, 1, 1, 2, 2, 3, 3]
    actual = return_df["dfasbands"].astype(int).to_list()

    assert actual == expected, f"When checking for dfasbands, expected to find {expected} but found {actual}"


def test_dcg7tot():
    input_df = pd.DataFrame(
        {
            "cg7": [1, 1, 1, 1, 2, -9, -1],
            "cg7mon": [0, -9, 0, 1, -1, -1, 0],
            "cg7tue": [2, -9, 0, 5, -1, -1, 0],
            "cg7wed": [5, -9, 0, -9, -1, 1, 0],
            "cg7thu": [0, -9, 0, 0, -1, -1, 0],
            "cg7fri": [2, -9, 0, 0, -1, -1, 0],
            "cg7sat": [6, -9, 0, 0, -1, -1, 1],
            "cg7sun": [0, -9, 0, 0, -1, -1, 0],
        }
    )
    return_df = derivations.dcg7tot(input_df)

    expected = [15, -8, 0, 6, 0, -9, -1]
    actual = return_df["dcg7tot"].astype(int).to_list()

    assert actual == expected, f"When checking for dcg7tot, expected to find {expected} but found {actual}"


def test_dcg7day():

    input_df = pd.DataFrame({"dcg7tot": [-1, -9, 0, 2, 14],
                             "cg7mon": [-1, 0,  0, -9, 2],
                             "cg7tue": [-1, 0,  0, 0, 2],
                             "cg7wed": [-1, 0,  0, 1, 2],
                             "cg7thu": [-1, 0,  0, 0, 2],
                             "cg7fri": [-1, 0,  0, 1, 2],
                             "cg7sat": [-1, 0,  0, -9, 2],
                             "cg7sun": [-1, 1,  0, 0, 2]})

    return_df = derivations.dcg7day(input_df)

    expected = pd.DataFrame(
        {
            "dcg7any": [-1, -9, 0, 1, 1],
            "dcg7mon": [-1, -9, 0, 0, 1],
            "dcg7tue": [-1, -9, 0, 0, 1],
            "dcg7wed": [-1, -9, 0, 1, 1],
            "dcg7thu": [-1, -9, 0, 0, 1],
            "dcg7fri": [-1, -9, 0, 1, 1],
            "dcg7sat": [-1, -9, 0, 0, 1],
            "dcg7sun": [-1, -9, 0, 0, 1]
        }
    ).astype(int)
    actual = return_df[["dcg7any", "dcg7mon", "dcg7tue", "dcg7wed",
                       "dcg7thu", "dcg7fri", "dcg7sat", "dcg7sun"]].astype(int)

    pd.testing.assert_frame_equal(actual, expected)


def test_dcg7totg():
    input_df = pd.DataFrame({"dcg7tot": [-1, -9, 0, 5, 9, 17, 29, 45, 75]})
    return_df = derivations.dcg7totg(input_df)

    expected = [-1, -9, 1, 2, 3, 4, 5, 6, 7]
    actual = return_df["dcg7totg"].astype(int).to_list()

    assert actual == expected, f"When checking for dcg7totg, expected to find {expected} but found {actual}"


def test_dcgsmk():

    input_df = pd.DataFrame({"dcgstg3": [1, 2, 3, -1, -8, -9]})

    return_df = derivations.dcgsmk(input_df)

    expected = [1, 1, 0, -1, -8, -9]
    actual = return_df["dcgsmk"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgsmk, expected to find {expected} but found {actual}"


def test_dlssmk():

    input_df = pd.DataFrame({"lssmk": [1, 0, -9, -1]})

    return_df = derivations.dlssmk(input_df)

    expected = [1, 0, 0, 0]
    actual = return_df["dlssmk"].astype(int).to_list()

    assert actual == expected, f"When checking for dlssmk, expected to find {expected} but found {actual}"


def test_dlsalc():

    input_df = pd.DataFrame({"lsalc": [1, 0, -9, -1]})

    return_df = derivations.dlsalc(input_df)

    expected = [1, 0, 0, 0]
    actual = return_df["dlsalc"].astype(int).to_list()

    assert actual == expected, f"When checking for dlsalc, expected to find {expected} but found {actual}"


def test_dlsdrg():

    input_df = pd.DataFrame({"lsdrg": [1, 0, -9, -1]})

    return_df = derivations.dlsdrg(input_df)

    expected = [1, 0, 0, 0]
    actual = return_df["dlsdrg"].astype(int).to_list()

    assert actual == expected, f"When checking for dlsdrg, expected to find {expected} but found {actual}"


def test_dcgfam():
    input_df = pd.DataFrame(
        {
            "cgireg": [-9, -8, 3, -1, -1, -1, -1],
            "cgstat": [-9, 1, 4, 5, 6, 6, 5],
            "cgfams": [-1, -1, -1, -1, -1, 5, 6],
            "cgfamn": [-1, -1, -1, -1, 1, -1, -1],
            "cgfamz": [-1, -1, 2, -9, -1, -1, -1]
        }
    )
    return_df = derivations.dcgfam(input_df)

    expected = [-9, -8, 2, -9, 1, 5, 5]
    actual = return_df["dcgfam"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgfam, expected to find {expected} but found {actual}"


def test_dcgfam4():

    input_df = pd.DataFrame({"dcgfam": [-1, -9, 1, 4, 5]})

    return_df = derivations.dcgfam4(input_df)

    expected = [-1, -9, 1, 3, 4]
    actual = return_df["dcgfam4"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgfam4, expected to find {expected} but found {actual}"


def test_dcgppfr():
    input_df = pd.DataFrame(
        {
            "cgppfrsa": [-9, -1, 1, 0, 0, 0, 0],
            "cgppfrol": [-9, -1, 0, 1, 0, 0, 0],
            "cgppfryo": [-9, -1, 0, 0, 1, 0, 0],
            "cgppgb": [-9, -1, 0, 0, 0, 1, 0]
        }
    )
    return_df = derivations.dcgppfr(input_df)

    expected = [-9, -1, 1, 1, 1, 1, 0]
    actual = return_df["dcgppfr"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgppfr, expected to find {expected} but found {actual}"


def test_dcggetp():
    input_df = pd.DataFrame(
        {
            "cggetgiv": [1, 0, 0, 0, -1, 0],
            "cggetsib": [0, 1, 0, 0, -1, -9],
            "cggetpar": [0, 0, 1, 0, -1, 0],
            "cggetelg": [-9, 0, 0, 1, -1, -9],
        }
    )
    return_df = derivations.dcggetp(input_df)

    expected = [1, 1, 1, 1, -1, -9]
    actual = return_df["dcggetp"].astype(int).to_list()

    assert actual == expected, f"When checking for dcggetp, expected to find {expected} but found {actual}"


def test_dcggets():
    input_df = pd.DataFrame(
        {
            "cggetnew": [1, 0, 0, 0, -1, -9],
            "cggetsup": [0, 1, 0, 0, -1, 0],
            "cggetgar": [0, 0, 1, 0, -1, 0],
            "cggetsho": [-9, 0, 0, 1, -1, 0],
        }
    )
    return_df = derivations.dcggets(input_df)

    expected = [1, 1, 1, 1, -1, -9]
    actual = return_df["dcggets"].astype(int).to_list()

    assert actual == expected, f"When checking for dcggets, expected to find {expected} but found {actual}"


def test_dcgbuyp():
    input_df = pd.DataFrame(
        {
            "cggetfre": [1, 2, -1, -9],
            "cggetels": [-9, 1, -1, 0],
        }
    )
    return_df = derivations.dcgbuyp(input_df)

    expected = [1, 1, -1, -9]
    actual = return_df["dcgbuyp"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgbuyp, expected to find {expected} but found {actual}"


def test_dcglongg():

    input_df = pd.DataFrame({"cglong": [1, 2, 3, 4, -9, -1]})

    return_df = derivations.dcglongg(input_df)

    expected = [1, 1, 1, 2, -9, -1]
    actual = return_df["dcglongg"].astype(int).to_list()

    assert actual == expected, f"When checking for dcglongg, expected to find {expected} but found {actual}"


def test_dcg7totg2():
    input_df = pd.DataFrame({"dcg7tot": [-1, -9, 0, 5, 20, 21, 75]})
    return_df = derivations.dcg7totg2(input_df)

    expected = [-1, -9, 1, 1, 1, 2, 2]
    actual = return_df["dcg7totg2"].astype(int).to_list()

    assert actual == expected, f"When checking for dcg7totg2, expected to find {expected} but found {actual}"


def test_dcgstopg():

    input_df = pd.DataFrame({"cgstop": [1, 2, 3, 4, -9, -1]})

    return_df = derivations.dcgstopg(input_df)

    expected = [1, 1, 2, 2, -9, -1]
    actual = return_df["dcgstopg"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgstopg, expected to find {expected} but found {actual}"


def test_dcgstopwg():

    input_df = pd.DataFrame({"cgstopw": [1, 2, 3, 4, -9, -1]})

    return_df = derivations.dcgstopwg(input_df)

    expected = [1, 1, 2, 2, -9, -1]
    actual = return_df["dcgstopwg"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgstopwg, expected to find {expected} but found {actual}"


def test_dcgtrystp():
    input_df = pd.DataFrame(
        {
            "cgevrstp": [1, 2, 1, 1, 2, 2, 1,  -8, -1],
            "cglikstp": [1, 1, 2, 3, 2, 3, -9, 1, -1],
            }
    )

    return_df = derivations.dcgtrystp(input_df)

    expected = [1, 2, 3, 3, 4, 4, -9, -8, -1]
    actual = return_df["dcgtrystp"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgtrystp, expected to find {expected} but found {actual}"


def test_dcgelbuy():
    input_df = pd.DataFrame(
        {
            "cgshopp": [-9, -8, -1, 1, 1, 2, 2, 8],
            "cgacbsp": [-9, -8, -1, 1, 2, 1, 2, 8],
        }
    )
    return_df = derivations.dcgelbuy(input_df)

    expected = [-9, -8, -1, 1, 2, 3, 3, -1]
    actual = return_df["dcgelbuy"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgelbuy, expected to find {expected} but found {actual}"


def test_dcggupxxx():

    input_df = pd.DataFrame({"cgstat": [-9, 1, 1, 2, 2, 3, 4, 5, 3, 4, 5],
                             "cgevrstp": [-1, 2, -8, 2, 2, 1, 1, 1, 1, 1, 1],
                             "cgireg": [-1, -1,  -1, 1, -9, -1, -1, -1, -1, -1, -1],
                             "cggupadn": [-1, -1,  -1, -2, 2, 1, 2, 2, 2, 2, 2],
                             "cggupads": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 2],
                             "cggupecg": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 2],
                             "cggupelc": [-1, -1,  -1, -2, 2, 2, 1, 2, 2, 2, 2],
                             "cggupfan": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 2],
                             "cggupfas": [-1, -1,  -1, -2, 2, 2, 2, 1, 2, 2, 2],
                             "cggupgpn": [-1, -1,  -1, -2, 2, 2, 2, 2, 1, 2, 2],
                             "cggupgps": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 2],
                             "cgguphen": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 2],
                             "cgguphes": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 1, 2],
                             "cggupnin": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 2],
                             "cggupnis": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 1],
                             "cggupnon": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 2],
                             "cggupnos": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 1, 2],
                             "cggupstn": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 2],
                             "cggupsts": [-1, -1,  -1, -2, 2, 2, 2, 2, 2, 2, 1]
                             })

    return_df = derivations.dcggupxxx(input_df)

    expected = pd.DataFrame(
        {
            "dcggupad": [-9, -1, -9, -1, -1, 1, 0, 0, 0, 0, 0],
            "dcggupecg": [-9, -1, -9, -1, -1, 0, 1, 0, 0, 0, 0],
            "dcggupfa": [-9, -1, -9, -1, -1, 0, 0, 1, 0, 0, 0],
            "dcggupgp": [-9, -1, -9, -1, -1, 0, 0, 0, 1, 0, 0],
            "dcgguphe": [-9, -1, -9, -1, -1, 0, 0, 0, 0, 1, 0],
            "dcggupni": [-9, -1, -9, -1, -1, 0, 0, 0, 0, 0, 1],
            "dcggupno": [-9, -1, -9, -1, -1, 0, 0, 0, 0, 1, 0],
            "dcggupst": [-9, -1, -9, -1, -1, 0, 0, 0, 0, 0, 1],
        }
    ).astype(int)
    actual = return_df[["dcggupad", "dcggupecg", "dcggupfa", "dcggupgp",
                       "dcgguphe", "dcggupni", "dcggupno", "dcggupst"]].astype(int)

    pd.testing.assert_frame_equal(actual, expected)


def test_dcggupany():
    input_df = pd.DataFrame(
        {
            "dcggupad": [-1, 1, 1, 0, -9],
            "dcggupecg": [-1, 0, 1, 0, 0],
            "dcggupfa": [-1, 1, 1, 0, 0],
            "dcggupgp": [-1, 0, 1, 0, 0],
            "dcgguphe": [-1, 0, 1, 0, 0],
            "dcggupni": [-1, 0, 1, 0, 0],
            "dcggupno": [-1, 0, 1, 0, 0],
            "dcggupst": [-1, 0, 1, 0, 0],
        }
    )
    return_df = derivations.dcggupany(input_df)

    expected = [-1, 1, 1, 0, -9]
    actual = return_df["dcggupany"].astype(int).to_list()

    assert actual == expected, f"When checking for dcggupany, expected to find {expected} but found {actual}"


def test_dcgoft():

    input_df = pd.DataFrame({"dcgstg5": [1, 2, 3, 4, 5, -9, -1]})

    return_df = derivations.dcgoft(input_df)

    expected = [3, 3, 2, 1, 99, -9, -1]
    actual = return_df["dcgoft"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgoft, expected to find {expected} but found {actual}"


def test_dcgsec2():

    input_df = pd.DataFrame({"cgfams": [1, 2, 3, 4, 5, 6, -9, -1]})

    return_df = derivations.dcgsec2(input_df)

    expected = [1, 1, 1, 1, 2, 1, -9, -1]
    actual = return_df["dcgsec2"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgsec2, expected to find {expected} but found {actual}"


def test_dcgppfam():
    input_df = pd.DataFrame(
        {
            "cgpppar": [-9, -1, 1, 0, 0, 0],
            "cgppsib": [-9, -1, 0, 1, 0, 0],
            "cgppoth": [-9, -1, 0, 0, 1, 0],
        }
    )
    return_df = derivations.dcgppfam(input_df)

    expected = [-9, -1, 1, 1, 1, 0]
    actual = return_df["dcgppfam"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgppfam, expected to find {expected} but found {actual}"


def test_dcgshboth():
    input_df = pd.DataFrame(
        {
            "cgshin": [-9, 5, -1, -8, 4, 3, 4, 5, 6],
            "cgshcar": [5, -8, -1, 1, 2, 4, -9, -9, -8],
        }
    )
    return_df = derivations.dcgshboth(input_df)

    expected = [-9, -9, -1, 1, 1, 1, 1, -9, -9]
    actual = return_df["dcgshboth"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgshboth, expected to find {expected} but found {actual}"


def test_dcgelgtoth():
    input_df = pd.DataFrame(
        {
            "cgelgtpha": [-1, -8, -9, 1, 1, 0, 1, 0],
            "cgelgtoth": [-1, -8, -9, 1, 0, 0, -9, -9],
        }
    )
    return_df = derivations.dcgelgtoth(input_df)

    expected = [-1, -9, -9, 1, 1, 0, 1, -9]
    actual = return_df["dcgelgtoth"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgelgtoth, expected to find {expected} but found {actual}"


def test_dcgelgtgiv():
    input_df = pd.DataFrame(
        {
            "cgelgtgiv": [-1, -8, -9, 1, 0, 0, 1, 0],
            "cgelgtsib": [-1, -8, -9, 1, 1, 0, -9, -9],
            "cgelgtpar": [-1, -8, -9, 1, 1, 0, 0, 0],
            "cgelgtelg": [-1, -8, -9, 1, 0, 0, -9, 0],
        }
    )
    return_df = derivations.dcgelgtgiv(input_df)

    expected = [-1, -9, -9, 1, 1, 0, 1, -9]
    actual = return_df["dcgelgtgiv"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgelgtgiv, expected to find {expected} but found {actual}"


def test_dcgelgtshp():
    input_df = pd.DataFrame(
        {
            "cgelgtnew": [-1, -8, -9, 1, 0, 0, 0, 0],
            "cgelgtsho": [-1, -8, -9, 1, 1, 0, -9, -9],
            "cgelgtsup": [-1, -8, -9, 1, 0, 0, 1, 0],
            "cgelgtpha": [-1, -8, -9, 1, 0, 0, -9, 0],
            "cgelgtgar": [-1, -8, -9, 1, 0, 0, 0, 0],
            "cgelgtoth": [-1, -8, -9, 1, 0, 0, -9, 0],
        }
    )
    return_df = derivations.dcgelgtshp(input_df)

    expected = [-1, -9, -9, 1, 1, 0, 1, -9]
    actual = return_df["dcgelgtshp"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgelgtshp, expected to find {expected} but found {actual}"


def test_dcgelgtppl():
    input_df = pd.DataFrame(
        {
            "cgelgtfre": [-1, -8, -9, 1, 0, 0, 0, 0],
            "cgelgtels": [-1, -8, -9, 1, 1, 0, 1, -9],
        }
    )
    return_df = derivations.dcgelgtppl(input_df)

    expected = [-1, -9, -9, 1, 1, 0, 1, -9]
    actual = return_df["dcgelgtppl"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgelgtppl, expected to find {expected} but found {actual}"


def test_dcgelec():
    input_df = pd.DataFrame(
        {
            "cgelecevr": [-1, -8, -9, 1, 2, 3, 4, 5, -1],
            "cgelechd": [-1, 1, 1, 1, 1, 1, 1, 1, 2],
        }
    )
    return_df = derivations.dcgelec(input_df)

    expected = [-1, -8, -9, 2, 3, 4, 5, 6, 1]
    actual = return_df["dcgelec"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgelec, expected to find {expected} but found {actual}"


def test_ddgyrty():

    input_df = pd.DataFrame({"duseamp": [-1, -9, 4, 4, -9, 2, 2, 4, 1, 4, 3],
                             "dusecan": [-1, -9, 1, 4, 4, 4, 4, 1, 1, 4, 4],
                             "dusecok": [-1, -9,  4, 4, 4, 4, 4, 2, 4, 3, 4],
                             "dusecrk": [-1, -9,  4, 4, 2, 4, 4, 2, -9, 3, -9],
                             "duseecs": [-1, -9,  -9, 4, 4, 4, 4, 4, 4, 4, 3],
                             "dusegas": [-1, -9,  4, 2, 4, 4, 4, -9, 4, 4, 4],
                             "duseher": [-1, -9,  4, -9, 4, 4, 4, 2, 4, 4, 4],
                             "duseket": [-1, -9,  4, -9, 4, 4, 4, 4, 4, 4, 4],
                             "duseleg": [-1, -9,  4, 4, 4, 4, 4, 4, 1, 4, 4],
                             "duselsd": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, 4],
                             "dusemph": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, 4],
                             "dusemsh": [-1, -9,  4, 4, 4, -9, 4, 4, 4, 4, 4],
                             "dusemth": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, 4],
                             "dusenox": [-1, -9,  4, 4, 4, 4, -9, 4, 4, 3, 4],
                             "duseoth": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, 4],
                             "dusepop": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 3, 4],
                             "dusetrn": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, -9],
                             "dgampij": [-1, -1,  -1, -1, -1, 1, 0, -1, 0, -1, -1],
                             })

    return_df = derivations.ddgyrty(input_df)

    expected = [7, -9, 1, 2, 3, 3, 4, 5, 6, 7, -9]
    actual = return_df["ddgyrty"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyrty, expected to find {expected} but found {actual}"


def test_ddgyrty5():

    input_df = pd.DataFrame({"duseamp": [-1, -9, 4, 4, -9, 2, 2, 4, 1, 4, 3],
                             "dusecan": [-1, -9, 1, 4, 4, 4, 4, 1, 1, 4, 4],
                             "dusecok": [-1, -9,  4, 4, 4, 4, 4, 2, 4, 3, 4],
                             "dusecrk": [-1, -9,  4, 4, 2, 4, 4, 2, -9, 3, -9],
                             "duseecs": [-1, -9,  -9, 4, 4, 4, 4, 4, 4, 4, 3],
                             "dusegas": [-1, -9,  4, 2, 4, 4, 4, -9, 4, 4, 4],
                             "duseher": [-1, -9,  4, -9, 4, 4, 4, 2, 4, 4, 4],
                             "duseket": [-1, -9,  4, -9, 4, 4, 4, 4, 4, 4, 4],
                             "duseleg": [-1, -9,  4, 4, 4, 4, 4, 4, 1, 4, 4],
                             "duselsd": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, 4],
                             "dusemph": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, 4],
                             "dusemsh": [-1, -9,  4, 4, 4, -9, 4, 4, 4, 4, 4],
                             "dusemth": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, 4],
                             "dusenox": [-1, -9,  4, 4, 4, 4, -9, 4, 4, 3, 4],
                             "duseoth": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, 4],
                             "dusepop": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 3, 4],
                             "dusetrn": [-1, -9,  4, 4, 4, 4, 4, 4, 4, 4, -9],
                             "dgampij": [-1, -1,  -1, -1, -1, 1, 0, -1, 0, -1, -1],
                             })

    return_df = derivations.ddgyrty5(input_df)

    expected = [5, -9, 1, 2, 3, 3, 4, 3, 4, 5, -9]
    actual = return_df["ddgyrty5"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyrty5, expected to find {expected} but found {actual}"


def test_ddganyresponse(all_drugs=param.DRUGS):

    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [-1, -8, -9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [1, 2, 3, 4, -1, -8, -9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        ]
    )

    return_df = derivations.ddganyresponse(input_df)

    expected = [-9, 1]
    actual = return_df["ddganyresponse"].astype(int).to_list()

    assert actual == expected, f"When checking for ddganyresponse, expected to find {expected} but found {actual}"


def test_ddganynotvs(all_drugs=param.DRUGS):

    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [-8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [1, 2, 3, 4, -8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]
    )

    # replace dusegas with 1 to check doesn't affect expected outcome
    # dusegas should be ignored for this function
    input_df["dusegas"] = [1, 1, 1, 1]

    return_df = derivations.ddganynotvs(input_df)

    expected = [-8, -9, 2, 1]
    actual = return_df["ddganynotvs"].astype(int).to_list()

    assert actual == expected, f"When checking for ddganynotvs, expected to find {expected} but found {actual}"


def test_ddgmonanynotvs(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [-8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [1, 2, 3, 4, -8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]
    )

    # replace dusegas with 1 to check doesn't affect expected outcome
    # dusegas should be ignored for this function
    input_df["dusegas"] = [1, 1, 1, 1]

    return_df = derivations.ddgmonanynotvs(input_df)

    expected = [-8, -9, 2, 1]
    actual = return_df["ddgmonanynotvs"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmonanynotvs, expected to find {expected} but found {actual}"


def test_ddgyranynotvs(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [-8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [1, 2, 4, 4, -8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]
    )

    # replace dusegas with 1 to check doesn't affect expected outcome
    # dusegas should be ignored for this function
    input_df["dusegas"] = [1, 1, 1, 1]

    return_df = derivations.ddgyranynotvs(input_df)

    expected = [-8, -9, 2, 1]
    actual = return_df["ddgyranynotvs"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyranynotvs, expected to find {expected} but found {actual}"


def test_ddganynotps(all_drugs=param.DRUGS):

    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [-8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [1, 2, 3, 4, -8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]
    )

    # replace duseleg and dusenox with 1 to check doesn't affect expected outcome
    # they should be ignored for this function
    input_df["duseleg"] = [1, 1, 1, 1]
    input_df["dusenox"] = [1, 1, 1, 1]

    return_df = derivations.ddganynotps(input_df)

    expected = [-8, -9, 2, 1]
    actual = return_df["ddganynotps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddganynotps, expected to find {expected} but found {actual}"


def test_ddgmonanynotps(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [-8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [1, 2, 3, 4, -8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]
    )

    # replace duseleg and dusenox with 1 to check doesn't affect expected outcome
    # they should be ignored for this function
    input_df["duseleg"] = [1, 1, 1, 1]
    input_df["dusenox"] = [1, 1, 1, 1]

    return_df = derivations.ddgmonanynotps(input_df)

    expected = [-8, -9, 2, 1]
    actual = return_df["ddgmonanynotps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmonanynotps, expected to find {expected} but found {actual}"


def test_ddgyranynotps(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in all_drugs],
        data=[
            [-8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [1, 2, 4, 4, -8, -9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]
    )

    # replace duseleg and dusenox with 1 to check doesn't affect expected outcome
    # they should be ignored for this function
    input_df["duseleg"] = [1, 1, 1, 1]
    input_df["dusenox"] = [1, 1, 1, 1]

    return_df = derivations.ddgyranynotps(input_df)

    expected = [-8, -9, 2, 1]
    actual = return_df["ddgyranynotps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyranynotps, expected to find {expected} but found {actual}"


def test_ddgevrcla(a_drugs=param.DRUGS_CLASSA):

    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in a_drugs] + ["duseamp", "dgampij"],
        data=[
            [-9, 4, 4, 4, 4, 4, 4, 4, 4],
            [-8, -9, 4, 4, 4, 4, 4, 4, 4],
            [1, 2, 3, -8, -9, 4, 4, 4, 4],
            [-9, -8, 4, 4, 4, 4, 4, 1, 1],
            [4, 4, 4, 4, 4, 4, 4, 4, 4],
        ]
    )

    return_df = derivations.ddgevrcla(input_df)

    expected = [-9, -8, 1, 1, 2]
    actual = return_df["ddgevrcla"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgevrcla, expected to find {expected} but found {actual}"


def test_ddgmoncla(a_drugs=param.DRUGS_CLASSA):

    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in a_drugs] + ["duseamp", "dgampij"],
        data=[
            [-9, 4, 4, 4, 4, 4, 4, 4, 4],
            [-8, -9, 4, 4, 4, 4, 4, 4, 4],
            [1, 2, 3, -8, -9, 4, 4, 4, 4],
            [-9, -8, 4, 4, 4, 4, 4, 1, 1],
            [2, 3, 4, 4, 4, 4, 4, 4, 4],
        ]
    )

    return_df = derivations.ddgmoncla(input_df)

    expected = [-9, -8, 1, 1, 2]
    actual = return_df["ddgmoncla"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmoncla, expected to find {expected} but found {actual}"


def test_ddgyrcla(a_drugs=param.DRUGS_CLASSA):

    input_df = pd.DataFrame(
        columns=["duse" + drug for drug in a_drugs] + ["duseamp", "dgampij"],
        data=[
            [-9, 4, 4, 4, 4, 4, 4, 4, 4],
            [-8, -9, 4, 4, 4, 4, 4, 4, 4],
            [1, 2, 3, -8, -9, 4, 4, 4, 4],
            [-9, -8, 4, 4, 4, 4, 4, 1, 1],
            [3, 4, 4, 4, 4, 4, 4, 4, 4],
        ]
    )

    return_df = derivations.ddgyrcla(input_df)

    expected = [-9, -8, 1, 1, 2]
    actual = return_df["ddgyrcla"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyrcla, expected to find {expected} but found {actual}"


def test_ddgevropi():

    input_df = pd.DataFrame(
        columns=["duseher", "dusemth"],
        data=[
            [-9, 4],
            [-8, -9],
            [1, 2],
            [3, 4],
            [4, 4],
        ]
    )

    return_df = derivations.ddgevropi(input_df)

    expected = [-9, -8, 1, 1, 2]
    actual = return_df["ddgevropi"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgevropi, expected to find {expected} but found {actual}"


def test_ddgmonopi():

    input_df = pd.DataFrame(
        columns=["duseher", "dusemth"],
        data=[
            [-9, 4],
            [-8, -9],
            [1, 2],
            [2, 3],
            [4, 4],
        ]
    )

    return_df = derivations.ddgmonopi(input_df)

    expected = [-9, -8, 1, 2, 2]
    actual = return_df["ddgmonopi"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmonopi, expected to find {expected} but found {actual}"


def test_dyropi():

    input_df = pd.DataFrame(
        columns=["duseher", "dusemth"],
        data=[
            [-9, 4],
            [-8, -9],
            [1, 2],
            [3, 4],
        ]
    )

    return_df = derivations.ddgyropi(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgyropi"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyropi, expected to find {expected} but found {actual}"


def test_ddgevrps():

    input_df = pd.DataFrame(
        columns=["duseleg", "dusenox"],
        data=[
            [-9, 4],
            [-8, -9],
            [1, 2],
            [2, 3],
            [4, 4],
        ]
    )

    return_df = derivations.ddgevrps(input_df)

    expected = [-9, -8, 1, 1, 2]
    actual = return_df["ddgevrps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgevrps, expected to find {expected} but found {actual}"


def test_ddgmonps():

    input_df = pd.DataFrame(
        columns=["duseleg", "dusenox"],
        data=[
            [-9, 4],
            [-8, -9],
            [1, 2],
            [2, 3],
            [4, 4]
        ]
    )

    return_df = derivations.ddgmonps(input_df)

    expected = [-9, -8, 1, 2, 2]
    actual = return_df["ddgmonps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmonps, expected to find {expected} but found {actual}"


def test_ddgyrps():

    input_df = pd.DataFrame(
        columns=["duseleg", "dusenox"],
        data=[
            [-9, 4],
            [-8, -9],
            [1, 2],
            [3, 4],
        ]
    )

    return_df = derivations.ddgyrps(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgyrps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyrps, expected to find {expected} but found {actual}"


def test_ddgevrpsy():

    input_df = pd.DataFrame(
        columns=["dusemsh", "duselsd", "duseket"],
        data=[
            [-9, 4, 4],
            [-8, -9, -9],
            [1, 2, 3],
            [4, 4, 4],
        ]
    )

    return_df = derivations.ddgevrpsy(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgevrpsy"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgevrpsy, expected to find {expected} but found {actual}"


def test_ddgmonpsy():

    input_df = pd.DataFrame(
        columns=["dusemsh", "duselsd", "duseket"],
        data=[
            [-9, 4, 4],
            [-8, -9, -9],
            [1, 1, 2],
            [2, 3, 4],
        ]
    )

    return_df = derivations.ddgmonpsy(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgmonpsy"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmonpsy, expected to find {expected} but found {actual}"


def test_ddgyrpsy():

    input_df = pd.DataFrame(
        columns=["dusemsh", "duselsd", "duseket"],
        data=[
            [-9, 4, 4],
            [-8, -9, -9],
            [1, 1, 2],
            [3, 3, 4],
        ]
    )

    return_df = derivations.ddgyrpsy(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgyrpsy"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyrpsy, expected to find {expected} but found {actual}"


def test_ddgevrstm():

    input_df = pd.DataFrame(
        columns=["duseecs", "dusecok", "dusecrk", "dusepop", "dusemph",
                 "duseamp"],
        data=[
            [-9, 4, 4, 4, 4, 4],
            [-8, -9, -9, -9, -9, -9],
            [1, 2, 3, 4, 4, 4],
            [4, 4, 4, 4, 4, 4],
        ]
    )

    return_df = derivations.ddgevrstm(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgevrstm"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgevrstm, expected to find {expected} but found {actual}"


def test_ddgmonstm():

    input_df = pd.DataFrame(
        columns=["duseecs", "dusecok", "dusecrk", "dusepop", "dusemph",
                 "duseamp"],
        data=[
            [-9, 4, 4, 4, 4, 4],
            [-8, -9, -9, -9, -9, -9],
            [1, 2, 3, 4, 4, 4],
            [2, 3, 4, 4, 4, 4],
        ]
    )

    return_df = derivations.ddgmonstm(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgmonstm"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmonstm, expected to find {expected} but found {actual}"


def test_ddgyrstm():

    input_df = pd.DataFrame(
        columns=["duseecs", "dusecok", "dusecrk", "dusepop", "dusemph",
                 "duseamp"],
        data=[
            [-9, 4, 4, 4, 4, 4],
            [-8, -9, -9, -9, -9, -9],
            [1, 2, 3, 4, 4, 4],
            [3, 4, 4, 4, 4, 4],
        ]
    )

    return_df = derivations.ddgyrstm(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgyrstm"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgyrstm, expected to find {expected} but found {actual}"


def test_ddgoc():
    input_df = pd.DataFrame(
        {
            "dgoc": [-1, -1, -9, -1, -1, 1, 2, 3, 4],
            "dgtdany": [-8, -9, 1, 2, 1, 1, 1, 1, 1],
            "dglast": [-1, -1, 1, -1, 3, 2, 1, 1, 1]
        }
    )
    return_df = derivations.ddgoc(input_df)

    expected = [-8, -9, -9, 1, 2, 3, 4, 5, 6]
    actual = return_df["ddgoc"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgoc, expected to find {expected} but found {actual}"


def test_ddgoc4():
    input_df = pd.DataFrame(
        {
            "ddgoc": [-8, -9, 1, 2, 3, 4, 5, 6],
        }
    )
    return_df = derivations.ddgoc4(input_df)

    expected = [-8, -9, 1, 2, 3, 3, 4, 4]
    actual = return_df["ddgoc4"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgoc4, expected to find {expected} but found {actual}"


def test_ddgtypleg():
    input_df = pd.DataFrame(
        {
            "dgtypleg": [-1, -8, -9, 1, 2, 3, 4]
        }
    )
    return_df = derivations.ddgtypleg(input_df)

    expected = [5, 5, 5, 1, 2, 3, 4]
    actual = return_df["ddgtypleg"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgtypleg, expected to find {expected} but found {actual}"


def test_ddgfq6():
    input_df = pd.DataFrame(
        {
            "dgusefq": [-8, -9, -1, 4, 5, -8, 2, 3, 4, 5, 1, -8, -9],
            "dgoc": [-1, -8, -9, 2, 2, 1, -1, -1, 1, 2, 2, 3, 4],
            "dglast": [-1, -1, 1, 1, 2, 2, -1, 3, 2, 1, 2, -8, -9],
            "dgtdany": [-8, -9, 1, 1, 1, 1, 2, 1, -8, -9, 1, 2, 1]
        }
    )
    return_df = derivations.ddgfq6(input_df)

    expected = [-8, -9, -9, 2, 3, 4, 6, 5, -8, -9, 1, 6, -9]
    actual = return_df["ddgfq6"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgfq6, expected to find {expected} but found {actual}"


def test_ddgfq8():
    input_df = pd.DataFrame(
        {
            "dgoc": [-1, -9, -9, 2, 2, 2, 2, 2, 1, 2, -1],
            "dgtdany": [-1, -8, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            "dglast": [-1, 1, 1, 2, 2, 2, 1, 1, 1, 3, -1],
            "dgusefq": [-1, -9, -9, 1, 2, 3, 4, 5, -1, -1, -1]
        }
    )
    return_df = derivations.ddgfq8(input_df)

    expected = [-9, -8, -9, 1, 2, 3, 4, 5, 6, 7, 8]
    actual = return_df["ddgfq8"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgfq8, expected to find {expected} but found {actual}"


def test_ddgfam():
    input_df = pd.DataFrame(
        {
            "dgfamst": [1, 1, 1, 1, -1],
            "dgfamfl": [-1, 2, 6, 1, -1],
            "dgfamkn": [-1, -1, -1, 3, -1],
        }
    )
    return_df = derivations.ddgfam(input_df)

    expected = [1, 2, 5, 3, -1]
    actual = return_df["ddgfam"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgfam, expected to find {expected} but found {actual}"


def test_ddgfam4():
    input_df = pd.DataFrame(
        {
            "ddgfam": [-8, -9, -1, 1, 2, 3, 4, 5],
        }
    )
    return_df = derivations.ddgfam4(input_df)

    expected = [-8, -9, -1, 1, 2, 3, 3, 4]
    actual = return_df["ddgfam4"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgfam4, expected to find {expected} but found {actual}"


def test_dtruexc():
    input_df = pd.DataFrame(
        {
            "truant": [-9, 2, -9, 1, 2, 1, 2],
            "excla": [-9, -9, 2, 2, 1, 1, 2],
            }
    )

    return_df = derivations.dtruexc(input_df)

    expected = [-9, -9, -9, 1, 1, 1, 2]
    actual = return_df["dtruexc"].astype(int).to_list()

    assert actual == expected, f"When checking for dtruexc, expected to find {expected} but found {actual}"


def test_ddgofxxx(all_drugs=param.DRUGS):

    drug_heard = ["dghd" + drug for drug in all_drugs]
    drug_off = ["dgof" + drug for drug in all_drugs]
    drug_off_derived = ["ddgof" + drug for drug in all_drugs]

    test_df_list = []
    expected_df_list = []
    # Create the new duseXXX column for each drug
    for dghd, dgof, ddgof in zip(drug_heard, drug_off, drug_off_derived):
        test_df = pd.DataFrame({
            dghd: [-8, -9, 2, 1, 1, 1],
            dgof: [1, -9, -1, 2, -9, 1],
        })
        expected_df = pd.DataFrame({
            dghd: [-8, -9, 2, 1, 1, 1],
            dgof: [1, -9, -1, 2, -9, 1],
            ddgof: [-8, -9, 2, 2, -9, 1]
        })
        test_df_list.append(test_df)
        expected_df_list.append(expected_df)

    input_df = pd.concat(test_df_list, axis=1)
    expected = pd.concat(expected_df_list, axis=1)
    actual = derivations.ddgofxxx(input_df)

    expected = expected.reindex(sorted(expected.columns), axis=1)
    actual = actual.reindex(sorted(actual.columns), axis=1)

    pd.testing.assert_frame_equal(actual, expected)


def test_ddgofany(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["ddgof" + drug for drug in all_drugs],
        data=[
            [-9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9],
            [-9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, -9, -9, 2, 2, 2, -8, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2],
        ]
    )
    return_df = derivations.ddgofany(input_df)

    expected = [-9, -9, 2, 1]
    actual = return_df["ddgofany"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgofany, expected to find {expected} but found {actual}"


def test_ddgofanyresponse(all_drugs=param.DRUGS):

    input_df = pd.DataFrame(
        columns=["ddgof" + drug for drug in all_drugs],
        data=[
            [-1, -8, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -8, -9],
            [1, 1, 2, 2, -9, -8, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9],
        ]
    )

    return_df = derivations.ddgofanyresponse(input_df)

    expected = [-9, 1]
    actual = return_df["ddgofanyresponse"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgofanyresponse, expected to find {expected} but found {actual}"


def test_ddgofanynotps(all_drugs=param.DRUGS):

    input_df = pd.DataFrame(
        columns=["ddgof" + drug for drug in all_drugs],
        data=[
            [-8, -9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, -9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 2, 2, 2, -8, -9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        ]
    )

    # replace ddgofleg and ddgofnox with 1 to check doesn't affect expected outcome
    # they should be ignored for this function
    input_df["ddgofleg"] = [1, 1, 1, 1]
    input_df["ddgofnox"] = [1, 1, 1, 1]

    return_df = derivations.ddgofanynotps(input_df)

    expected = [-8, -9, 2, 1]
    actual = return_df["ddgofanynotps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgofanynotps, expected to find {expected} but found {actual}"


def test_ddgofstm():

    input_df = pd.DataFrame(
        columns=["ddgofecs", "ddgofcok", "ddgofcrk", "ddgofpop", "ddgofmph",
                 "ddgofamp"],
        data=[
            [-9, 2, 2, 2, 2, 2],
            [-8, -9, -9, -9, -9, -9],
            [1, 2, -9, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
        ]
    )

    return_df = derivations.ddgofstm(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgofstm"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgofstm, expected to find {expected} but found {actual}"


def test_ddgofpsy():

    input_df = pd.DataFrame(
        columns=["ddgofmsh", "ddgoflsd", "ddgofket"],
        data=[
            [-9, 2, 2],
            [-8, -9, -9],
            [1, 2, -9],
            [2, 2, 2],
        ]
    )

    return_df = derivations.ddgofpsy(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgofpsy"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgofpsy, expected to find {expected} but found {actual}"


def test_ddgofps():

    input_df = pd.DataFrame(
        columns=["ddgofleg", "ddgofnox"],
        data=[
            [-9, 2],
            [-8, -9],
            [1, 2],
            [2, 2],
        ]
    )

    return_df = derivations.ddgofps(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgofps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgofps, expected to find {expected} but found {actual}"


def test_ddgofopi():

    input_df = pd.DataFrame(
        columns=["ddgofher", "ddgofmth"],
        data=[
            [-9, 2],
            [-8, -9],
            [1, 2],
            [2, 2],
        ]
    )

    return_df = derivations.ddgofopi(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgofopi"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgofps, expected to find {expected} but found {actual}"


def test_ddgofcla(a_drugs=param.DRUGS_CLASSA):

    input_df = pd.DataFrame(
        columns=["ddgof" + drug for drug in a_drugs] + ["ddgofamp"],
        data=[
            [-9, 2, 2, 2, 2, 2, 2, 2],
            [-8, -9, 2, 2, 2, 2, 2, 2],
            [1, -8, -9, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
        ]
    )

    return_df = derivations.ddgofcla(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddgofcla"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgofcla, expected to find {expected} but found {actual}"


def test_ddgageany(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["dgage" + drug for drug in all_drugs],
        data=[
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-9, 12, 13, 14, 15, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9],
            [1, 12, 13, 14, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 11, -1, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 12, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 13, -1, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1],
            [-1, -1, -1, -1, 14, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1],
            [15, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        ]
    )
    return_df = derivations.ddgageany(input_df)

    expected = [-1, -9, -9, 10, 11, 12, 13, 14, 15]
    actual = return_df["ddgageany"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgageany, expected to find {expected} but found {actual}"


def test_ddgageany11():

    input_df = pd.DataFrame({"ddgageany": [-9, -1, 5, 6, 7, 8, 9, 10, 11, 12, 16]})

    return_df = derivations.ddgageany11(input_df)

    expected = [-9, -1, 11, 11, 11, 11, 11, 11, 11, 12, 15]
    actual = return_df["ddgageany11"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgageany11, expected to find {expected} but found {actual}"


def test_ddgagexxx(all_drugs=param.DRUGS):

    input_columns = ["dgage" + drug for drug in all_drugs]
    output_columns = ["ddgage" + drug for drug in all_drugs]

    test_df_list = []
    expected_df_list = []
    # Create the new ddgageXXX column for each drug
    for dgage, ddgage in zip(input_columns, output_columns):
        test_df = pd.DataFrame({
            dgage: [-1, -9, 11, 15],
        })
        expected_df = pd.DataFrame({
            dgage: [-1, -9, 11, 15],
            ddgage: [-1, -9, 1, 0]
        })
        test_df_list.append(test_df)
        expected_df_list.append(expected_df)

    # Include the ddgageany variable
    ddgageany = pd.DataFrame({"ddgageany": [-1, -9, 11, 12]})

    input_df = pd.concat(test_df_list, axis=1)
    input_df = pd.concat([input_df, ddgageany], axis=1)
    expected = pd.concat(expected_df_list, axis=1)
    expected = pd.concat([expected, ddgageany], axis=1)
    actual = derivations.ddgagexxx(input_df)

    expected = expected.reindex(sorted(expected.columns), axis=1)
    actual = actual.reindex(sorted(actual.columns), axis=1)

    pd.testing.assert_frame_equal(actual, expected)


def test_ddgfirst():

    input_df = pd.DataFrame({"ddgageany": [-1, -9, 12, 13, 14, 15],
                             "ddgageamp": [-1, -9, 0, 0, 1, 0],
                             "ddgagecan": [-1, -9, 1, 0, 1, 0],
                             "ddgagecok": [-1, -9,  0, 0, -9, 0],
                             "ddgagecrk": [-1, -9,  0, 0, 1, 0],
                             "ddgageecs": [-1, -9,  -9, 0, 0, 0],
                             "ddgagegas": [-1, -9,  0, 1, 0, 0],
                             "ddgageher": [-1, -9,  0, -9, 0, 0],
                             "ddgageket": [-1, -9,  0, -9, 0, 0],
                             "ddgageleg": [-1, -9,  0, 0, 0, 0],
                             "ddgagelsd": [-1, -9,  0, 0, 0, 0],
                             "ddgagemph": [-1, -9,  0, 0, 0, 0],
                             "ddgagemsh": [-1, -9,  0, 0, 0, -9],
                             "ddgagemth": [-1, -9,  0, 0, 0, 0],
                             "ddgagenox": [-1, -9,  0, 0, 0, 0],
                             "ddgageoth": [-1, -9,  0, 0, 0, 0],
                             "ddgagepop": [-1, -9,  0, 0, 0, 1],
                             "ddgagetrn": [-1, -9,  0, 0, 0, 0],
                             })

    return_df = derivations.ddgfirst(input_df)

    expected = [-1, -9, 1, 2, 3, 4]
    actual = return_df["ddgfirst"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgfirst, expected to find {expected} but found {actual}"


def test_ddgfttyp():

    input_df = pd.DataFrame({"dgfttdamp": [-1, -9, 0, 0, 1, 0],
                             "dgfttdcan": [-1, -9, 1, 0, 1, 0],
                             "dgfttdcok": [-1, -9,  0, 0, -9, 0],
                             "dgfttdcrk": [-1, -9,  0, 0, 1, 0],
                             "dgfttdecs": [-1, -9,  -9, 0, 0, 0],
                             "dgfttdvs": [-1, -9,  0, 1, 0, 0],
                             "dgfttdher": [-1, -9,  0, -9, 0, 0],
                             "dgfttdket": [-1, -9,  0, -9, 0, 0],
                             "dgfttdleg": [-1, -9,  0, 0, 0, 0],
                             "dgfttdlsd": [-1, -9,  0, 0, 0, 0],
                             "dgfttdmph": [-1, -9,  0, 0, 0, 0],
                             "dgfttdmsh": [-1, -9,  0, 0, 0, -9],
                             "dgfttdmth": [-1, -9,  0, 0, 0, 0],
                             "dgfttdnox": [-1, -9,  0, 0, 0, 0],
                             "dgfttdoth": [-1, -9,  0, 0, 0, 0],
                             "dgfttdpop": [-1, -9,  0, 0, 0, 1],
                             "dgfttdtrn": [-1, -9,  0, 0, 0, 0],
                             })

    return_df = derivations.ddgfttyp(input_df)

    expected = [-1, -9, 1, 2, 3, 4]
    actual = return_df["ddgfttyp"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgfttyp, expected to find {expected} but found {actual}"


def test_ddglttyp():

    input_df = pd.DataFrame({"dglttdamp": [-1, -9, 0, 0, 1, 0],
                             "dglttdcan": [-1, -9, 1, 0, 1, 0],
                             "dglttdcok": [-1, -9,  0, 0, -9, 0],
                             "dglttdcrk": [-1, -9,  0, 0, 1, 0],
                             "dglttdecs": [-1, -9,  -9, 0, 0, 0],
                             "dglttdvs": [-1, -9,  0, 1, 0, 0],
                             "dglttdher": [-1, -9,  0, -9, 0, 0],
                             "dglttdket": [-1, -9,  0, -9, 0, 0],
                             "dglttdleg": [-1, -9,  0, 0, 0, 0],
                             "dglttdlsd": [-1, -9,  0, 0, 0, 0],
                             "dglttdmph": [-1, -9,  0, 0, 0, 0],
                             "dglttdmsh": [-1, -9,  0, 0, 0, -9],
                             "dglttdmth": [-1, -9,  0, 0, 0, 0],
                             "dglttdnox": [-1, -9,  0, 0, 0, 0],
                             "dglttdoth": [-1, -9,  0, 0, 0, 0],
                             "dglttdpop": [-1, -9,  0, 0, 0, 1],
                             "dglttdtrn": [-1, -9,  0, 0, 0, 0],
                             })

    return_df = derivations.ddglttyp(input_df)

    expected = [-1, -9, 1, 2, 3, 4]
    actual = return_df["ddglttyp"].astype(int).to_list()

    assert actual == expected, f"When checking for ddglttyp, expected to find {expected} but found {actual}"


def test_ddghdnotaw(all_drugs=param.DRUGS):
    input_df = pd.DataFrame(
        columns=["dghd" + drug for drug in all_drugs],
        data=[
            [-9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9],
            [-9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, -9, -9, 2, 2, 2, -8, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2],
        ]
    )
    # replace dghdgas with 1 to check doesn't affect expected outcome
    # should be ignored for this function
    input_df["dghdgas"] = [1, 1, 1, 1]

    return_df = derivations.ddghdnotaw(input_df)

    expected = [-9, -9, 1, 2]
    actual = return_df["ddghdnotaw"].astype(int).to_list()

    assert actual == expected, f"When checking for ddghdnotaw, expected to find {expected} but found {actual}"


def test_ddghdanyresponse(all_drugs=param.DRUGS):

    input_df = pd.DataFrame(
        columns=["dghd" + drug for drug in all_drugs],
        data=[
            [-1, -8, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -8, -9],
            [1, 1, 2, 2, -9, -8, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9],
        ]
    )

    # replace dghdgas with 1 to check doesn't affect expected outcome
    # should be ignored for this function
    input_df["dghdgas"] = [1, 1]

    return_df = derivations.ddghdanyresponse(input_df)

    expected = [-9, 1]
    actual = return_df["ddghdanyresponse"].astype(int).to_list()

    assert actual == expected, f"When checking for ddghdanyresponse, expected to find {expected} but found {actual}"


def test_ddghdnotawexps(all_drugs=param.DRUGS):

    input_df = pd.DataFrame(
        columns=["dghd" + drug for drug in all_drugs],
        data=[
            [-8, -9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, -9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 2, 2, 2, -8, -9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        ]
    )

    # replace dghdleg and dghdnox and dghdgas with 1 to check doesn't affect expected outcome
    # they should be ignored for this function
    input_df["dghdleg"] = [1, 1, 1, 1]
    input_df["dghdnox"] = [1, 1, 1, 1]
    input_df["dghdgas"] = [1, 1, 1, 1]

    return_df = derivations.ddghdnotawexps(input_df)

    expected = [-9, -9, 1, 2]
    actual = return_df["ddghdnotawexps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddghdnotawexps, expected to find {expected} but found {actual}"


def test_ddghdstm():

    input_df = pd.DataFrame(
        columns=["dghdamp", "dghdecs", "dghdpop", "dghdcrk", "dghdcok",
                 "dghdmph"],
        data=[
            [-9, 2, 2, 2, 2, 2],
            [-8, -9, -9, -9, -9, -9],
            [1, 2, -9, 2, 2, 2],
            [2, 2, 2, 2, 2, 2],
        ]
    )

    return_df = derivations.ddghdstm(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddghdstm"].astype(int).to_list()

    assert actual == expected, f"When checking for ddghdstm, expected to find {expected} but found {actual}"


def test_ddghdpsy():

    input_df = pd.DataFrame(
        columns=["dghdmsh", "dghdlsd", "dghdket"],
        data=[
            [-9, 2, 2],
            [-8, -9, -9],
            [1, 2, -9],
            [2, 2, 2],
        ]
    )

    return_df = derivations.ddghdpsy(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddghdpsy"].astype(int).to_list()

    assert actual == expected, f"When checking for ddghdpsy, expected to find {expected} but found {actual}"


def test_ddghdps():

    input_df = pd.DataFrame(
        columns=["dghdleg", "dghdnox"],
        data=[
            [-9, 2],
            [-8, -9],
            [1, 2],
            [2, 2],
        ]
    )

    return_df = derivations.ddghdps(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddghdps"].astype(int).to_list()

    assert actual == expected, f"When checking for ddghdps, expected to find {expected} but found {actual}"


def test_ddghdopi():

    input_df = pd.DataFrame(
        columns=["dghdher", "dghdmth"],
        data=[
            [-9, 2],
            [-8, -9],
            [1, 2],
            [2, 2],
        ]
    )

    return_df = derivations.ddghdopi(input_df)

    expected = [-9, -8, 1, 2]
    actual = return_df["ddghdopi"].astype(int).to_list()

    assert actual == expected, f"When checking for ddghdopi, expected to find {expected} but found {actual}"


def test_ddgwho():

    input_df = pd.DataFrame({"dgltown": [1, -9,  1, 1, 2, -1],
                             "dgltwogbf": [1,  1, 0, 0, -9, -1],
                             "dgltwofrs": [1, -9,  1, -9, 0, -1],
                             "dgltwofro": [0, -9,  0, 0, 0, -1],
                             "dgltwofrb": [0, -9,  0, 1, 0, -1],
                             "dgltwopar": [0, -9,  1, 0, 1, -1],
                             "dgltwooth": [0, -9,  0, 0, 1, -1],
                             "dgltwoels": [0, -9,  1, -9, 0, -1]
                             })

    return_df = derivations.ddgwho(input_df)

    expected = pd.DataFrame(
        {
            "ddgltown": [0, -9, 0, 0, 1, -1],
            "ddgltwogbf": [1, 1, 0, 0, 0, -1],
            "ddgltwofrs": [1, -9, 1, -9, 0, -1],
            "ddgltwofro": [0, -9, 0, 0, 0, -1],
            "ddgltwofrb": [0, -9, 0, 1, 0, -1],
            "ddgltwopar": [0, -9, 1, 0, 0, -1],
            "ddgltwooth": [0, -9, 0, 0, 0, -1],
            "ddgltwoels": [0, -9, 1, -9, 0, -1]
        }
    ).astype(int)
    actual = return_df[["ddgltown", "ddgltwogbf", "ddgltwofrs", "ddgltwofro", "ddgltwofrb",
                       "ddgltwopar", "ddgltwooth", "ddgltwoels"]].astype(int)

    pd.testing.assert_frame_equal(actual, expected)


def test_ddgltwofre():

    input_df = pd.DataFrame({"dgltwogbf": [1, 0, 0, 0, -9],
                             "dgltwofrs": [1, 0, 0, 0, 0],
                             "dgltwofro": [0, 1, -9, 0, 1],
                             "dgltwofrb": [0, 1, 0, 0, 0],
                             "dgltown": [2, 1, -9, 2, -9]
                             })

    return_df = derivations.ddgltwofre(input_df)

    expected = [0, 1, -9, 0, 1]
    actual = return_df["ddgltwofre"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgltwofre, expected to find {expected} but found {actual}"


def test_ddgfamknw():
    input_df = pd.DataFrame(
        {
            "dgtdany": [2, -8, -9, 1, 1, 1, 1, 1],
            "ddgfam": [-1, -8, -9, 1, 2, 3, 4, 1],
            "dgfamfl": [-1, -8, -9, 1, 2, 3, 4, 5],
        }
    )
    return_df = derivations.ddgfamknw(input_df)

    expected = [-1, -8, -9, 1, 1, 1, 1, 2]
    actual = return_df["ddgfamknw"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgfamknw, expected to find {expected} but found {actual}"
    
    
def test_ddglast3():
    input_df = pd.DataFrame(
        {
            "ddgany": [-8, -9, 0, 1],
            "ddgmonany": [0, 1, -8, -9],
        }
    )
    return_df = derivations.ddglast3(input_df)

    expected = [-8, 1, 3, 2]
    actual = return_df["ddglast3"].astype(int).to_list()

    assert actual == expected, f"When checking for ddglast3, expected to find {expected} but found {actual}"


def test_dcgevr():
    input_df = pd.DataFrame(
        {"dcgstg5": [-1, -8, -9, 1, 2, 3, 4, 5]}
    )
    return_df = derivations.dcgevr(input_df)

    expected = [-1, -8, -9, 1, 1, 1, 1, 2]
    actual = return_df["dcgevr"].astype(int).to_list()

    assert actual == expected, f"When checking for dcgevr, expected to find {expected} but found {actual}"


def test_ddgevrcan():
    input_df = pd.DataFrame(
        {"dusecan": [-8, -9, 1, 2, 3, 4]}
    )
    return_df = derivations.ddgevrcan(input_df)

    expected = [-8, -9, 1, 1, 1, 2]
    actual = return_df["ddgevrcan"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgevrcan, expected to find {expected} but found {actual}"


def test_ddgevrvs():
    input_df = pd.DataFrame(
        {"dusegas": [-8, -9, 1, 2, 3, 4]}
    )
    return_df = derivations.ddgevrvs(input_df)

    expected = [-8, -9, 1, 1, 1, 2]
    actual = return_df["ddgevrvs"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgevrvs, expected to find {expected} but found {actual}"


def test_dmultievr():
    input_df = pd.DataFrame(
        {
            "dcgevr": [-8, -9, -9, -9, 1, 1, 0, 0],
            "ddgany": [-8, -9, 0, 1, 1, 0, 1, 0],
            "alevr": [-8, -9, 0, 0, 1, 1, 0, 0]
        }
    )
    return_df = derivations.dmultievr(input_df)

    expected = [-9, -9, -9, 1, 1, 1, 1, 0]
    actual = return_df["dmultievr"].astype(int).to_list()

    assert actual == expected, f"When checking for dmultievr, expected to find {expected} but found {actual}"


def test_ddgmonvs():
    input_df = pd.DataFrame(
        {"dusegas": [-8, -9, 1, 2, 3, 4]}
    )
    return_df = derivations.ddgmonvs(input_df)

    expected = [-8, -9, 1, 2, 2, 2]
    actual = return_df["ddgmonvs"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmonvs, expected to find {expected} but found {actual}"


def test_ddgmoncan():
    input_df = pd.DataFrame(
        {"dusecan": [-8, -9, 1, 2, 3, 4]}
    )
    return_df = derivations.ddgmoncan(input_df)

    expected = [-8, -9, 1, 2, 2, 2]
    actual = return_df["ddgmoncan"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmoncan, expected to find {expected} but found {actual}"


def test_dmultirec():
    input_df = pd.DataFrame(
        {
            "cg7": [-8, -9, -9, -9, 1, 1, 0, 0],
            "dallast5": [-8, -9, 0, 1, 1, 0, 1, 0],
            "ddgmonany": [-8, -9, 0, 0, 1, 1, 0, 0]
        }
    )
    return_df = derivations.dmultirec(input_df)

    expected = [-9, -9, -9, 1, 1, 1, 1, 0]
    actual = return_df["dmultirec"].astype(int).to_list()

    assert actual == expected, f"When checking for dmultirec, expected to find {expected} but found {actual}"


def test_dmultioverlap():
    input_df = pd.DataFrame(
        {
            "cg7": [-8, -9, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2],
            "dallast5": [-8, -9, 2, 5, 1, 2, 5, 1, 2, 5, 1, 1, 2, 5],
            "ddgmonany": [-8, -9, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
        }
    )
    return_df = derivations.dmultioverlap(input_df)

    expected = [-9, -9, 1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 8]
    actual = return_df["dmultioverlap"].astype(int).to_list()

    assert actual == expected, f"When checking for dmultioverlap, expected to find {expected} but found {actual}"


def test_dmulticount():
    input_df = pd.DataFrame(
        {
            "dmultioverlap": [-9, 1, 2, 3, 4, 5, 6, 7, 8],
        }
    )
    return_df = derivations.dmulticount(input_df)

    expected = [-9, 1, 1, 1, 2, 2, 2, 3, 0]
    actual = return_df["dmulticount"].astype(int).to_list()

    assert actual == expected, f"When checking for dmulticount, expected to find {expected} but found {actual}"


def test_dlifsat():
    input_df = pd.DataFrame(
        {
            "lifesat": [0, 4, 5, 6, 7, 8, 9, 10, -9, -8],
        }
    )
    return_df = derivations.dlifsat(input_df)

    expected = [1, 1, 2, 2, 3, 3, 4, 4, -9, -8]
    actual = return_df["dlifsat"].astype(int).to_list()

    assert actual == expected, f"When checking for dlifsat, expected to find {expected} but found {actual}"


def test_dlifwor():
    input_df = pd.DataFrame(
        {
            "lifewor": [0, 4, 5, 6, 7, 8, 9, 10, -9, -8],
        }
    )
    return_df = derivations.dlifwor(input_df)

    expected = [1, 1, 2, 2, 3, 3, 4, 4, -9, -8]
    actual = return_df["dlifwor"].astype(int).to_list()

    assert actual == expected, f"When checking for dlifwor, expected to find {expected} but found {actual}"


def test_dlifhap():
    input_df = pd.DataFrame(
        {
            "lifehap": [0, 4, 5, 6, 7, 8, 9, 10, -9, -8],
        }
    )
    return_df = derivations.dlifhap(input_df)

    expected = [1, 1, 2, 2, 3, 3, 4, 4, -9, -8]
    actual = return_df["dlifhap"].astype(int).to_list()

    assert actual == expected, f"When checking for dlifhap, expected to find {expected} but found {actual}"


def test_dlifanx():
    input_df = pd.DataFrame(
        {
            "lifeanx": [0, 2, 3, 4, 5, 8, 9, -9, -8],
        }
    )
    return_df = derivations.dlifanx(input_df)

    expected = [1, 2, 2, 3, 3, 4, 4, -9, -8]
    actual = return_df["dlifanx"].astype(int).to_list()

    assert actual == expected, f"When checking for dlifanx, expected to find {expected} but found {actual}"


def test_dliflow():
    input_df = pd.DataFrame(
        {
            "dlifsat":   [-8, -9, 2, 1, 1, 2, 1, 1, -9],
            "dlifhap":   [-8, -9, 2, 2, 1, 1, 1, -9, 2],
            "dlifwor":   [-8, -9, 4, 3, 4, 1, 1, 1, 2],
            "dlifanx":   [-8, -9, 1, 1, 2, 4, 4, 1, 2],
        }
    )
    return_df = derivations.dliflow(input_df)

    expected = [-9, -9, 0, 1, 2, 3, 4, -9, -9]
    actual = return_df["dliflow"].astype(int).to_list()

    assert actual == expected, f"When checking for dliflow, expected to find {expected} but found {actual}"


def test_dfamsmok():
    input_df = pd.DataFrame({"cgwhosmo": [-9, -1, -8, 0, 1, 2, 3, 6]})
    return_df = derivations.dfamsmok(input_df)

    expected = [-9, -1, -8, 0, 1, 2, 3, 3]
    actual = return_df["dfamsmok"].astype(int).to_list()

    assert actual == expected, f"When checking for dfamsmok, expected to find {expected} but found {actual}"
    
    
def test_dmet7dysg():
    input_df = pd.DataFrame({"met7dys": [-9, 1, 2, 3, 4, 5, 6, 7, 8]})
    return_df = derivations.dmet7dysg(input_df)

    expected = [-9, 1, 2, 2, 3, 3, 4, 4, 4]
    actual = return_df["dmet7dysg"].astype(int).to_list()

    assert actual == expected, f"When checking for dmet7dysg, expected to find {expected} but found {actual}"


def test_dmultievroverlap():
    input_df = pd.DataFrame(
        {
            "dcgevr": [-8, -9, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2],
            "alevr": [-8, -9, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2],
            "ddgany": [-8, -9, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
        }
    )
    return_df = derivations.dmultievroverlap(input_df)

    expected = [-9, -9, 1, 4, 2, 3, 3, 4, 5, 7, 6, 7, 8, 8]
    actual = return_df["dmultievroverlap"].astype(int).to_list()

    assert actual == expected, f"When checking for dmultievroverlap, expected to find {expected} but found {actual}"


def test_dmultievrcount():
    input_df = pd.DataFrame(
        {
            "dmultievroverlap": [-9, 1, 2, 3, 4, 5, 6, 7, 8],
        }
    )
    return_df = derivations.dmultievrcount(input_df)

    expected = [-9, 1, 1, 1, 2, 2, 2, 3, 0]
    actual = return_df["dmultievrcount"].astype(int).to_list()

    assert actual == expected, f"When checking for dmultievrcount, expected to find {expected} but found {actual}"


def test_ddgmultirec():
    input_df = pd.DataFrame(
        {
            "ddgmonany": [-8, -9, -9, -9, 1, 1, 1, 1, 0],
            "ddgmonvs":  [-8, -9,  2,  1, 1, 2, 1, 1, 2],
            "ddgmoncan": [-8, -9,  2,  2, 1, 1, 2, 1, 2],
            "ddgmoncla": [-8, -9,  2,  2, 1, 1, 1, 2, 2]
        }
    )
    return_df = derivations.ddgmultirec(input_df)

    expected =           [-9, -9, -9,  1, 1, 1, 1, 1, 0]
    actual = return_df["ddgmultirec"].astype(int).to_list()

    assert actual == expected, f"When checking for ddgmultirec, expected to find {expected} but found {actual}"
