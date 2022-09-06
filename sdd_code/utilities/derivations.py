import numpy as np

from sdd_code.utilities import parameters as param


def get_derivations():
    """
    A list of the derivation functions to be run, each of which takes a
    DataFrame as its argument and returns a copy of the DataFrame with a
    derived field appended.
    Add or remove any from the list as required.

    Parameters:
        None.

    Returns: list (str)
        A list of derivations that need to be run.

    """
    # Create the list of general derivations
    general_derivations = [age1115, age1215, age1315, ethnicgp5, ethnicgp4,
                           dtruexc, dfas, dfasbands, dmet7dysg]

    # Create the list of derivations relating to alcohol use

    alcohol_derivations = [dalfrq7, dallast3, dallast5, nal7br, nal7pp, nal7sd, nal7sp,
                           nal7winsh, nal7ut, nal7utg4, nal7utg7, dalagedru,
                           daldrunk, dal4dru6, dal7beer, dal7shan, dal7winsh,
                           dal7spir, dal7pops, dal7any, dalunitsday,
                           dalshop4, dalpub4, dalgot4, dalbuyper, dalbuyret,
                           dalushmo, dagedrank, daluswho, dalusfre, dalfam,
                           dalfamknw, dfamdrin, dal4dru5, dallastwk, dlsalc]

    # Create the list of derivations relating to drugs
    drug_derivations = [dusexxx, ddgany, ddgmonany, ddgyrany, ddgdrugs, dlsdrg,
                        ddgyrty, ddgyrty5, ddganyresponse, ddganynotvs, ddgmonanynotvs,
                        ddgyranynotvs, ddganynotps, ddgmonanynotps,
                        ddgyranynotps, ddgevrcla, ddgmoncla, ddgyrcla,
                        ddgevropi, ddgmonopi, ddgyropi, ddgevrps, ddgmonps,
                        ddgyrps, ddgevrpsy, ddgmonpsy, ddgyrpsy, ddgevrstm,
                        ddgmonstm, ddgyrstm, ddgoc, ddgtypleg, ddgfq6, ddgfq8,
                        ddgofxxx, ddgofany, ddgofanyresponse, ddgofanynotps,
                        ddgofstm, ddgofpsy, ddgofps, ddgofopi, ddgfam, ddgageany,
                        ddgageany11, ddgagexxx, ddgfirst, ddgfttyp, ddgofcla,
                        ddghdnotaw, ddghdanyresponse, ddghdnotawexps, ddghdstm,
                        ddghdpsy, ddghdps, ddghdopi, ddglttyp, ddgoc4, ddgfamknw,
                        ddgfam4, ddgltwofre, ddgwho, ddgevrcan, ddgevrvs,
                        ddgmonvs, ddgmoncan, ddglast3, ddgmultirec]

    # Create the list of derivations relating to smoking
    smoking_derivations = [dcgstg2, dcgstg3, dcgstg5, dcg7tot, dcg7totg,
                           dcg7totg2, dcg7day, dcgsmk, dlssmk, dcggetp, dcggets,
                           dcgbuyp, dcgfam, dcgfam4, dcgppfr, dcglongg, dcgstopg,
                           dcgstopwg, dcgtrystp, dcgelbuy, dcggupxxx, dcggupany,
                           dcgoft, dcgsec2, dcgppfam, dcgshboth, dcgevr, dfamsmok]

    # Create the list of derivations relating to e-cigarette use
    ecig_derivations = [dcgelec, dcgelgtoth, dcgelgtppl, dcgelgtshp, dcgelgtgiv]

    # Create the list of derivations relating to wellbeing
    wellbeing_derivations = [dlifhap, dlifsat, dlifwor, dlifanx, dliflow]

    # Create the list of derivations relating to multiple behaviours
    multi_derivations = [dmultievr, dmultirec, dmultioverlap, dmulticount,
                         dmultievroverlap, dmultievrcount]

    all_derivations = (
        general_derivations
        + alcohol_derivations
        + drug_derivations
        + smoking_derivations
        + ecig_derivations
        + wellbeing_derivations
        + multi_derivations
    )

    return all_derivations


def age1115(df):
    """
    Creates the derivation age11_15 which groups anyone under 12 as 11,
    and over 14 as 15.

    """

    df.loc[df["age"] < 0, "age1115"] = df["age"]
    df.loc[(df["age"] > 0) & (df["age"] < 11), "age1115"] = 11
    df.loc[(df["age"] > 10) & (df["age"] < 16), "age1115"] = df["age"]
    df.loc[df["age"] > 14, "age1115"] = 15

    return df


def age1215(df):
    """
    Creates the derivation age1215 which groups anyone under 13 as 12
    and anyone over 14 as 15.

    """

    df.loc[df["age"] < 10, "age1215"] = df["age"]
    df.loc[(df["age"] > 0) & (df["age"] < 12), "age1215"] = 12
    df.loc[(df["age"] > 11) & (df["age"] < 16), "age1215"] = df["age"]
    df.loc[df["age"] > 15, "age1215"] = 15

    return df


def age1315(df):
    """
    Creates the derivation age13_15 which groups anyone aged 10, 11 or 12
    as 13 and anyone over 14 as 15.

    """

    df.loc[df["age"] < 10, "age1315"] = df["age"]
    df.loc[(df["age"] > 0) & (df["age"] < 13), "age1315"] = 13
    df.loc[(df["age"] > 12) & (df["age"] < 16), "age1315"] = df["age"]
    df.loc[df["age"] > 15, "age1315"] = 15

    return df


def dalfrq7(df):
    """
    Creates the derivation dalfrq7 from alevr and alfreq.
    measures the grouped usual drinking frequency of pupils (7 groups)
    Note that this replaces the old dalfrq8 derivation
    (7 required for reporting rather than 8)

    """
    df["dalfrq7"] = df["alfreq"]
    df.loc[df["alevr"] < 0, "dalfrq7"] = df["alevr"]
    df.loc[df["alevr"] == 2, "dalfrq7"] = 7

    return df


def dallast3(df):
    """
    Creates the derivation dallast3 from alevr (ever had alc drink) and
    allast (when last had alc)
    measures when pupils last drank - 3 groups (in last week, not in last week,
    never drunk alc)

    """
    df["dallast3"] = df["allast"]
    df.loc[(df["alevr"] == 1) & (df["allast"].isin([1, 2, 3])),
           "dallast3"] = 1
    df.loc[(df["alevr"] == 1) & (df["allast"].isin([4, 5, 6, 7])),
           "dallast3"] = 2
    df.loc[df["alevr"] == 2, "dallast3"] = 3
    df.loc[df["alevr"] < 0, "dallast3"] = df["alevr"]

    return df


def dallast5(df):
    """
    Creates the derivation dallast_5 from alevr and allast.
    measures when pupils last drank.

    """
    df["dallast5"] = df["allast"]
    df.loc[df["alevr"] == 2, "dallast5"] = 5
    df.loc[(df["alevr"] == 1) & (df["allast"].isin([1, 2, 3])),
           "dallast5"] = 1
    df.loc[(df["alevr"] == 1) & (df["allast"].isin([4, 5])),
           "dallast5"] = 2
    df.loc[(df["alevr"] == 1) & (df["allast"] == 6),
           "dallast5"] = 3
    df.loc[(df["alevr"] == 1) & (df["allast"] == 7),
           "dallast5"] = 4
    df.loc[df["alevr"] < 0, "dallast5"] = df["alevr"]

    return df


def nal7br(df):
    """
    Creates the derivation nal7br from the al7brxx fields.
    measures units of beer drunk in last week.
    applies unit multipliers depending on strength and type of alcohol

    """

    # Define unit multipliers for each beer strength category
    # total units will be multiplied based on beer strength
    multi_normal = 1
    multi_strong = 1.5
    multi_dk = 1.25

    # Define unit multipliers for each beer type
    # units are multiplied depending on beer type
    multi_brbt = 1.5
    multi_brlg = 2
    multi_brpt = 2
    multi_brsm = 1.5

    # Define the low consumption default units - where drank less than half a pint
    less_half_pint = 0.5

    # Create temp versions of the variables where negative values are converted to zeros
    # and type specific multipliers are applied
    # Temp versions avoid errors in multiplications / sum calculations involving negative values
    df["al7brbt_adj"] = np.where(df["al7brbt"] < 0, 0, df["al7brbt"]*multi_brbt)
    df["al7brhp_adj"] = np.where(df["al7brhp"] < 0, 0, df["al7brhp"])
    df["al7brlg_adj"] = np.where(df["al7brlg"] < 0, 0, df["al7brlg"]*multi_brlg)
    df["al7brpt_adj"] = np.where(df["al7brpt"] < 0, 0, df["al7brpt"]*multi_brpt)
    df["al7brsm_adj"] = np.where(df["al7brsm"] < 0, 0, df["al7brsm"]*multi_brsm)

    # Create a summed beer units formula
    sum_beer = (df["al7brbt_adj"] + df["al7brhp_adj"] + df["al7brlg_adj"]
                + df["al7brpt_adj"] + df["al7brsm_adj"])

    # Create a conditon where any of the beer options have units greater than 0
    units_above_zero = (
        (df["al7brbt"] > 0) |
        (df["al7brhp"] > 0) |
        (df["al7brlg"] > 0) |
        (df["al7brpt"] > 0) |
        (df["al7brsm"] > 0)
        )

    # Create the derived field
    # Where all contributing alcohol types are not answered then return not answered
    df.loc[(
        (df["al7brbt"].isin([-8, -9]))
        & (df["al7brhp"].isin([-8, -9]))
        & (df["al7brlg"].isin([-8, -9]))
        & (df["al7brpt"].isin([-8, -9]))
        & (df["al7brsm"].isin([-8, -9]))
        ), "nal7br"] = -9

    # Where any of the lead in questions are not answered then return not answered
    df.loc[(
        (df["al7beer"].isin([-8, -9])) |
        (df["alevr"].isin([-8, -9])) |
        (df["allast"].isin([-8, -9]))
        ), "nal7br"] = -9

    # If drank less than half a pint then return default low units value
    df.loc[df["al7beer"] == 2, "nal7br"] = less_half_pint
    # Else sum the units and apply the overall multipliers based on usual strenghth of beer drunk
    df.loc[units_above_zero & (~df["albrstr"].isin([2, 3])), "nal7br"] = sum_beer * multi_normal
    df.loc[units_above_zero & (df["albrstr"] == 2), "nal7br"] = sum_beer * multi_strong
    df.loc[units_above_zero & (df["albrstr"] == 3), "nal7br"] = sum_beer * multi_dk
    # All remaining records default to 0
    df.loc[df["nal7br"].isnull(), "nal7br"] = 0

    # Drop the temp variables
    df.drop(["al7brbt_adj", "al7brhp_adj", "al7brlg_adj",
             "al7brpt_adj", "al7brsm_adj"], axis=1, inplace=True)

    return df


def nal7pp(df):
    """
    Creates the derivation nal7pp from the al7ppxx fields.
    measures units of alcopops drunk in last week.
    applies unit multipliers depending on strength and type of alcohol

    """
    # Define unit multipliers for each alcopop type
    # units are multiplied depending on alcopop type
    multi_ppcn = 1.5
    multi_ppbt = 1.5

    # Define the low consumption default units - where drank less than a bottle
    less_bottle = 0.75

    # Create temp versions of the variables where negative values are converted to zeros
    # and type specific multipliers are applied
    # Temp versions avoid errors in multiplications / sum calculations involving negative values
    df["al7ppcn_adj"] = np.where(df["al7ppcn"] < 0, 0, df["al7ppcn"]*multi_ppcn)
    df["al7ppbt_adj"] = np.where(df["al7ppbt"] < 0, 0, df["al7ppbt"]*multi_ppbt)

    # Create a summed alcopop units formula
    sum_pops = df["al7ppcn_adj"] + df["al7ppbt_adj"]

    # Create a conditon where any of the alcopop options have units greater than 0
    units_above_zero = ((df["al7ppcn"] > 0) | (df["al7ppbt"] > 0))

    # Create the derived field
    # Where all contributing alcohol types are not answered then return not answered
    df.loc[
        (df["al7ppcn"].isin([-8, -9])) &
        (df["al7ppbt"].isin([-8, -9])),
        "nal7pp"] = -9

    # Where any of the lead in questions are not answered then return not answered
    df.loc[
        (df["al7pops"].isin([-8, -9])) |
        (df["alevr"].isin([-8, -9])) |
        (df["allast"].isin([-8, -9])),
        "nal7pp"] = -9

    # If drank less than a bottle then return default low unit value
    df.loc[df["al7pops"] == 2, "nal7pp"] = less_bottle
    # Else sum the units
    df.loc[units_above_zero, "nal7pp"] = sum_pops
    # All remaining records default to 0
    df.loc[df["nal7pp"].isnull(), "nal7pp"] = 0

    # Drop the temp variables
    df.drop(["al7ppcn_adj", "al7ppbt_adj"], axis=1, inplace=True)

    return df


def nal7sd(df):
    """
    Creates the derivation nal7sd from the al7sdxx fields.
    measures units of shandy drunk in last week.
    applies unit multipliers depending on strength and type of alcohol

    """
    # Define unit multiplier for pints of shandy
    # Unites for hald pints of shandy are multiplied by this
    multi_sdhp = 0.5

    # Define the low consumption default units - where drank less than half a pint
    less_half_pint = 0.25

    # Create temp versions of the variables where negative values are converted to zeros
    # and type specific multipliers are applied
    # Temp versions avoid errors in multiplications / sum calculations involving negative values
    df["al7sdpt_adj"] = np.where(df["al7sdpt"] < 0, 0, df["al7sdpt"])
    df["al7sdhp_adj"] = np.where(df["al7sdhp"] < 0, 0, df["al7sdhp"]*multi_sdhp)

    # Create a summed shandy units formula
    sum_shandy = df["al7sdpt_adj"] + df["al7sdhp_adj"]

    # Create a conditon where any of the shandy options have units greater than 0
    units_above_zero = ((df["al7sdpt"] > 0) | (df["al7sdhp"] > 0))

    # Create the derived field
    # Where all contributing alcohol types are not answered then return not answered
    df.loc[
        (df["al7sdpt"].isin([-8, -9])) &
        (df["al7sdhp"].isin([-8, -9])),
        "nal7sd"] = -9

    # Where any of the lead in questions are not answered then return not answered
    df.loc[
        (df["al7shan"].isin([-8, -9])) |
        (df["alevr"].isin([-8, -9])) |
        (df["allast"].isin([-8, -9])),
        "nal7sd"] = -9

    # If drank less than half a pint then return default low unit value
    df.loc[df["al7shan"] == 2, "nal7sd"] = less_half_pint
    # Else sum the units
    df.loc[units_above_zero, "nal7sd"] = sum_shandy
    # All remaining records default to 0
    df.loc[df["nal7sd"].isnull(), "nal7sd"] = 0

    # Drop the temp variables
    df.drop(["al7sdpt_adj", "al7sdhp_adj"], axis=1, inplace=True)

    return df


def nal7sp(df):
    """
    Creates the derivation nal7sp from the al7spgs field.
    measures units of spirits drunk in last week.

    """
    # Define the low consumption default units - where drank less than half a glass
    less_half_glass = 0.5

    # Where all contributing alcohol types are not answered then return not answered
    df.loc[df["al7spgs"].isin([-8, -9]), "nal7sp"] = -9
    # Where any of the lead in questions are not answered then return not answered
    df.loc[
        (df["al7spir"].isin([-8, -9])) |
        (df["alevr"].isin([-8, -9])) |
        (df["allast"].isin([-8, -9])),
        "nal7sp"] = -9

    # If drank less than half a glass then return default low unit value
    df.loc[df["al7spir"] == 2, "nal7sp"] = less_half_glass
    # Else sum the units
    df.loc[df["al7spgs"] > 0, "nal7sp"] = df["al7spgs"]
    # All remaining records default to 0
    df.loc[df["nal7sp"].isnull(), "nal7sp"] = 0

    return df


def nal7winsh(df):
    """
    Creates the derivation nal7winsh from the al7spgs field.
    measures units of wine/sherry drunk in last week.
    applies strength multiplier

    """
    # Define the low consumption default units - where drank less than a glass
    less_glass = 1

    # Define unit multiplier for spirits
    # Unites for spirits are multiplied by this
    multi_wnshgs = 2

    # Where all contributing alcohol types are not answered then return not answered
    df.loc[df["al7wnshgs"].isin([-8, -9]), "nal7winsh"] = -9
    # Where any of the lead in questions are not answered then return not answered
    df.loc[
        (df["al7winsh"].isin([-8, -9])) |
        (df["alevr"].isin([-8, -9])) |
        (df["allast"].isin([-8, -9])),
        "nal7winsh"] = -9

    # If drank less than a glass then return default low unit value
    df.loc[df["al7winsh"] == 2, "nal7winsh"] = less_glass
    # Else sum the units
    df.loc[df["al7wnshgs"] > 0, "nal7winsh"] = df["al7wnshgs"]*multi_wnshgs
    # All remaining records default to 0
    df.loc[df["nal7winsh"].isnull(), "nal7winsh"] = 0

    return df


def nal7ut(df):
    """
    Creates the derivation nal7ut from the individual nal7xx variables.
    measures total units drunk in last week.

    """
    # If any of the lead in questions or totals for an alcohol type are not answered
    # then return not answered
    df.loc[
        (df["alevr"].isin([-8, -9])) |
        (df["allast"].isin([-8, -9])) |
        (df["nal7br"] == -9) |
        (df["nal7pp"] == -9) |
        (df["nal7sd"] == -9) |
        (df["nal7sp"] == -9) |
        (df["nal7winsh"] == -9),
        "nal7ut"] = -9

    # Else sum the unit types for each alcohol type
    df.loc[df["nal7ut"].isnull(), "nal7ut"] = (df["nal7br"] + df["nal7pp"]
                                               + df["nal7sd"] + df["nal7sp"]
                                               + df["nal7winsh"])

    return df


def nal7utg(df):
    """
    Creates the derivation nal7utg from the variable nal7ut
    groups total units drunk in last week (4 groups)

    """

    df.loc[df["nal7ut"] < 0, "nal7utg"] = df["nal7ut"]
    df.loc[(df["nal7ut"] >= 0) & (df["nal7ut"] < 1), "nal7utg"] = 1
    df.loc[(df["nal7ut"] >= 1) & (df["nal7ut"] < 7), "nal7utg"] = 2
    df.loc[(df["nal7ut"] >= 7) & (df["nal7ut"] < 14), "nal7utg"] = 3
    df.loc[df["nal7ut"] >= 14, "nal7utg"] = 4

    return df


def nal7utg4(df):
    """
    Creates the derivation nal7utg from the variable nal7ut
    groups total units drunk in last week (4 groups)

    """

    df.loc[df["nal7ut"] < 0, "nal7utg4"] = df["nal7ut"]
    df.loc[(df["nal7ut"] >= 0) & (df["nal7ut"] < 1), "nal7utg4"] = 1
    df.loc[(df["nal7ut"] >= 1) & (df["nal7ut"] < 5), "nal7utg4"] = 2
    df.loc[(df["nal7ut"] >= 5) & (df["nal7ut"] < 10), "nal7utg4"] = 3
    df.loc[df["nal7ut"] >= 10, "nal7utg4"] = 4

    return df


def nal7utg7(df):
    """
    Creates the derivation nal7utg7 from the variable nal7ut
    groups total units drunk in last week (7 groups)
    Note that this replaces the old nal7utg8 which is no longer used

    """

    df.loc[df["nal7ut"] < 0, "nal7utg7"] = df["nal7ut"]
    df.loc[(df["nal7ut"] >= 0) & (df["nal7ut"] < 1), "nal7utg7"] = 1
    df.loc[(df["nal7ut"] >= 1) & (df["nal7ut"] < 2), "nal7utg7"] = 2
    df.loc[(df["nal7ut"] >= 2) & (df["nal7ut"] < 4), "nal7utg7"] = 3
    df.loc[(df["nal7ut"] >= 4) & (df["nal7ut"] < 6), "nal7utg7"] = 4
    df.loc[(df["nal7ut"] >= 6) & (df["nal7ut"] < 10), "nal7utg7"] = 5
    df.loc[(df["nal7ut"] >= 10) & (df["nal7ut"] < 15), "nal7utg7"] = 6
    df.loc[df["nal7ut"] >= 15, "nal7utg7"] = 7

    return df


def daldrunk(df):
    """
    Creates the derivation daldrunk from the variables alevr and alverdnk
    derived field has 3 outcomes regarding whether they have ever drank and/or been drunk
    (1 - Drank but not Drunk, 2 - Drank and been Drunk, 3 - Never Drank)
    If alevr was not answered then this will be not answered.

    """
    df["daldrunk"] = -9
    df.loc[(df["alevr"] < 0), "daldrunk"] = df["alevr"]
    df.loc[(df["alevr"] == 1) & (df["alevrdnk"] == 2), "daldrunk"] = 1
    df.loc[(df["alevr"] == 1) & (df["alevrdnk"] == 1), "daldrunk"] = 2
    df.loc[(df["alevr"] == 2), "daldrunk"] = 3

    return df


def dalagedru(df):
    """
    Creates the derivation dalagedru from the variable alagednk
    Groups all ages first drunk less than 10 together, and >15 together.

    """
    df.loc[df["alagednk"] < 0, "dalagedru"] = df["alagednk"]
    df.loc[(df["alagednk"] >= 0) & (df["alagednk"] < 11), "dalagedru"] = 10
    df.loc[(df["alagednk"] >= 11) & (df["alagednk"] < 15),
           "dalagedru"] = df["alagednk"]
    df.loc[df["alagednk"] >= 15, "dalagedru"] = 15

    return df


def dal4dru6(df):
    """
    Creates the derivation dal4dru6 from the variables alevr (ever had alc
    drink), allast (last had alc), al4wdru (drunk last 4wks),
    al4wfrq (times drunk last 4wks)

    groups on how many times been drunk in last four weeks,
    including not been drunk and not known

    """
    df["dal4dru6"] = 6

    df.loc[df["al4wfrq"] >= 3, "dal4dru6"] = 3
    df.loc[df["al4wfrq"] >= 10, "dal4dru6"] = 4
    df.loc[df["al4wfrq"].isin([1, 2]), "dal4dru6"] = 2
    df.loc[(df["al4wdru"] == 2) | (df["al4wfrq"] == 0), "dal4dru6"] = 1
    df.loc[df["al4wdru"] < 0, "dal4dru6"] = -9
    df.loc[df["allast"] < 0, "dal4dru6"] = df["allast"]
    df.loc[(df["alevr"] < 0),"dal4dru6"] = df["alevr"]
    df.loc[(df["alevr"] == 2) | (df["allast"] > 5), "dal4dru6"] = 5

    return df


def dal4dru5(df):
    """
    Creates the derivation dal4dru5, how many times been drunk in last four weeks,
    from the derivation dal4dru6, whether drunk in last 4 weeks.
    Grouped into 5 rather than 6 (3-10 times and more than 10 times combined)
    """

    df["dal4dru5"] = df["dal4dru6"]
    df.loc[df["dal4dru6"] == 4, "dal4dru5"] = 3

    return df


def dal7beer(df):
    """
    Creates the derivation dal7beer from the variable al7beer
    Combines responses 1 and 2 into a single "Yes - 1" response
    (have drunk beer in last week) and 3 into "No - 2"
    Else use the non-valid response in original variable.

    """

    df.loc[df["al7beer"].isin([1, 2]), "dal7beer"] = 1
    df.loc[df["al7beer"] == 3, "dal7beer"] = 2
    df.loc[df["dal7beer"].isnull(), "dal7beer"] = df["al7beer"]

    return df


def dal7shan(df):
    """
    Creates the derivation dal7shan from the variable al7shan
    Combines responses 1 and 2 into a single "Yes - 1" response
    (have drunk beer in last week) and 3 into "No - 2"
    Else use the non-valid response in original variable.

    """

    df.loc[df["al7shan"].isin([1, 2]), "dal7shan"] = 1
    df.loc[df["al7shan"] == 3, "dal7shan"] = 2
    df.loc[df["dal7shan"].isnull(), "dal7shan"] = df["al7shan"]

    return df


def dal7winsh(df):
    """
    Creates the derivation dal7winsh from the variable al7winsh
    Combines responses 1 and 2 into a single "Yes - 1" response
    (have drunk beer in last week) and 3 into "No - 2"
    Else use the non-valid response in original variable.

    """

    df.loc[df["al7winsh"].isin([1, 2]), "dal7winsh"] = 1
    df.loc[df["al7winsh"] == 3, "dal7winsh"] = 2
    df.loc[df["dal7winsh"].isnull(), "dal7winsh"] = df["al7winsh"]

    return df


def dal7spir(df):
    """
    Creates the derivation dal7spir from the variable al7spir
    Combines responses 1 and 2 into a single "Yes - 1" response
    (have drunk beer in last week) and 3 into "No - 2"
    Else use the non-valid response in original variable.

    """

    df.loc[df["al7spir"].isin([1, 2]), "dal7spir"] = 1
    df.loc[df["al7spir"] == 3, "dal7spir"] = 2
    df.loc[df["dal7spir"].isnull(), "dal7spir"] = df["al7spir"]

    return df


def dal7pops(df):
    """
    Creates the derivation dal7pops from the variable al7pops
    Combines responses 1 and 2 into a single "Yes - 1" response
    (have drunk beer in last week) and 3 into "No - 2"
    Else use the non-valid response in original variable.

    """

    df.loc[df["al7pops"].isin([1, 2]), "dal7pops"] = 1
    df.loc[df["al7pops"] == 3, "dal7pops"] = 2
    df.loc[df["dal7pops"].isnull(), "dal7pops"] = df["al7pops"]

    return df


def dal7any(df):
    """
    Creates the derivation dal7any from the variable dallast 5 and
    al7beer, al7shan, al7winsh, al7spir and al7pops to identify if a pupil
    has answered any of the questions about alcohol type drunk in last week.
    If pupils drank in last week (dallast5) and any one of the al7 questions
    has been answered (not negative) then is 1. Else -9 (not answered any).
    This is used for dispay in tables only. Provides an approx. overall base that
    covers the individual bases used for the dal7 precentage calculations.

    """
    # Create a temp variable that checks if any of the alcohol type questions was answered
    df["anytype"] = np.where(
        (df["dal7beer"].isin([1, 2]) |
         df["dal7shan"].isin([1, 2]) |
         df["dal7winsh"].isin([1, 2]) |
         df["dal7spir"].isin([1, 2]) |
         df["dal7pops"].isin([1, 2])), 1, 0)

    # Set derived value to 1 if pupil drank in last week and answered which type(s)
    df.loc[(df["dallast5"] == 1) & (df["anytype"] == 1), "dal7any"] = 1
    # Else set to not answered
    df.loc[(df["dal7any"].isnull()), "dal7any"] = -9

    # Drop the temp variable
    df.drop(["anytype"], axis=1, inplace=True)

    return df


def dagedrank(df):
    """
    Creates the derivation agedrank from the variable alage.
    Measures when pupils first drank.
    Groups all ages first drank less than 10 together and >15 together.

    """

    df.loc[df["alage"] < 0, "dagedrank"] = df["alage"]
    df.loc[(df["alage"] >= 0) & (df["alage"] < 11), "dagedrank"] = 10
    df.loc[(df["alage"] >= 11) & (df["alage"] < 15), "dagedrank"] = df["alage"]
    df.loc[df["alage"] >= 15, "dagedrank"] = 15

    return df


def dalunitsday(df):
    """
    Creates the derivation dalunitsday from the variables nal7ut and al7day
    which calculates the mean number of units drunk on each drinking day and
    assigns it one of four groupings (< 1 unit, 1 to < 3 units, 3 to < 5 units,
    5 units or more)

    """

    # set default value
    df["dalunitsday"] = -9

    # calculate mean using number of units drunk and days drank
    # where both are provided
    df.loc[(df["nal7ut"] >= 0) & (df["al7day"] > 0),
           "nal7ut_mean"] = df['nal7ut'] / df["al7day"]

    # assign mean to grouping
    df.loc[(df["nal7ut_mean"] >= 0) & (df["nal7ut_mean"] < 1),
           "dalunitsday"] = 1

    df.loc[(df["nal7ut_mean"] >= 1) & (df["nal7ut_mean"] < 3),
           "dalunitsday"] = 2

    df.loc[(df["nal7ut_mean"] >= 3) & (df["nal7ut_mean"] < 5),
           "dalunitsday"] = 3

    df.loc[(df["nal7ut_mean"] >= 5),
           "dalunitsday"] = 4

    # drop the temp mean variable
    df.drop(["nal7ut_mean"], axis=1, inplace=True)

    return df


def dalshop4(df):
    """
    Creates the derivation dalshop4 from the variables altryshp, alacbs4 and altry4.
    Has the pupil tried to buy alcohol in last 4 weeks from a shop
    derived field has 2 non negative outcomes (1 - Yes, 2 - No)

    """
    df["dalshop4"] = df["altryshp"]
    df.loc[(df["altry4"] < 0) | (df["altry4"] == 2),
           "dalshop4"] = df["altry4"]
    df.loc[df["altry4"] == 1 & (df["alacbs4"].isin([1, 2, -8, -9])),
           "dalshop4"] = df["alacbs4"]

    return df


def dalpub4(df):
    """
    Creates the derivation dalpub4 from the variables altrypub, alacbp4 and altry4.
    Has the pupil tried to buy alcohol in last 4 weeks from a pub.
    derived field has 2 non negative outcomes (1 - Yes, 2 - No)

    """
    df["dalpub4"] = df["altrypub"]
    df.loc[(df["altry4"] < 0) | (df["altry4"] == 2), "dalpub4"] = df["altry4"]
    df.loc[(df["altry4"] == 1) & (df["alacbp4"].isin([1, 2, -8, -9])),
           "dalpub4"] = df["alacbp4"]

    return df


def dalgot4(df):
    """
    Creates the derivation dalgot4wk, pupils who obtained alcohol in the last 4 weeks
    derived field has 2 non negative outcomes (1 - Yes, 2 - No)
    """
    # Define the list of fields that are checked for this derivation
    input_columns = [
        "dalshop4",
        "dalpub4",
        "altryels",
        "algivpar",
        "algivsib",
        "algivrel",
        "algivfre",
        "algivoth",
        "altakhom",
        "altakfre",
        "alstlhom",
        "alstlfre",
        "alstloth"]

    df["dalgot4"] = -1

    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "dalgot4"] = -9
    df.loc[df[input_columns].eq(1).any(axis=1), "dalgot4"] = 1
    df.loc[df[input_columns].eq(2).all(axis=1), "dalgot4"] = 2

    return df


def dalbuyper(df):
    """
    Creates the derivation albuyper, whether pupils usually buy alcohol from
    another person.
    derived field has 2 non negative outcomes (1 - Yes, 0 - No)
    """
    # Define the list of fields that are checked for this derivation
    input_columns = [
        "albuyels",
        "albuyfre",
        "albuystr"]

    df["dalbuyper"] = -1

    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "dalbuyper"] = -9  
    df.loc[df[input_columns].eq(1).any(axis=1), "dalbuyper"] = 1
    df.loc[df[input_columns].eq(0).all(axis=1), "dalbuyper"] = 0

    return df


def dalbuyret(df):
    """
    Creates the derivation albuyret, whether pupils usually buy alcohol from
    any retailer or licenced premises.
    derived field has 2 non negative outcomes (1 - Yes, 0 - No)
    """
    # Define the list of fields that are checked for this derivation
    input_columns = [
        "albuyoff",
        "albuyshp",
        "albuygar",
        "albuypub",
        "albuyclu"]

    df["dalbuyret"] = -1

    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "dalbuyret"] = -9      
    df.loc[df[input_columns].eq(1).any(axis=1), "dalbuyret"] = 1
    df.loc[df[input_columns].eq(0).all(axis=1), "dalbuyret"] = 0

    return df


def dalushmo(df):
    """
    Creates the derivation dalushmo from the variables alushom and alusohm
    derived field has 2 non negative outcomes (1 - Yes, 0 - No)
    """

    df["dalushmo"] = -1
    df.loc[(df["alushom"].isin([-8, -9])) | (df["alusohm"].isin([-8, -9])),
           "dalushmo"] = -9
    df.loc[(df["alushom"] == 1) | (df["alusohm"] == 1), "dalushmo"] = 1
    df.loc[(df["alushom"] == 0) & (df["alusohm"] == 0), "dalushmo"] = 0

    return df


def daluswho(df):
    """
    Creates the adjusted versions of the who does the pupil normally drink with
    questions: daluspar, dalussib, dalusfreb, dalusfreo, dalusfres, dalusgb and
    dalusoth.
    If alownoth (usually drinks alone) is 1, then all of the who
    usually drinks with questions are adjusted to 0 (No).
    derived fields have 2 non negative outcomes (1 - Yes, 0 - No)
    """

    # Define the list of fields that are checked for this derivation
    input_columns = [
        "aluspar",
        "alussib",
        "alusfreb",
        "alusfreo",
        "alusfres",
        "alusgb",
        "alusoth"]

    for column in input_columns:

        df.loc[df["alownoth"] == 1, "d"+column] = 0
        df.loc[df["alownoth"] != 1, "d"+column] = df[column]

    return df


def dalusfre(df):
    """
    Creates the derivation dalusfre, pupils who usually drink with a friend
    based on alownoth (usually drink alone) and alufreb, alusfreo, alusfres
    (usually drink with friends)
    derived field has 2 non negative outcomes (1 - Yes, 2 - No)
    """
    # Create a list of the drinking with friends fields to check
    input_columns = [
        "alusfreb",
        "alusfreo",
        "alusfres",
        "alusgb"]

    df["dalusfre"] = -1

    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "dalusfre"] = -9
    df.loc[df[input_columns].eq(1).any(axis=1), "dalusfre"] = 1
    df.loc[df[input_columns].eq(0).all(axis=1), "dalusfre"] = 0
    df.loc[df["alownoth"] == 1, "dalusfre"] = 0

    return df


def dfamdrin(df):
    """
    Creates the derivation dfamdrin from alwhodr
    measures number of people pupil lives with who drink
    4 groups (none, one, two, three or more)

    """

    df.loc[df["alwhodr"] < 3, "dfamdrin"] = df["alwhodr"]
    df.loc[df["alwhodr"] > 2, "dfamdrin"] = 3

    return df


def dallastwk(df):
    """Creates the derivation dallastwk, a binary flag for
    whether a pupil drank in the last week
    """

    df["dallastwk"] = -9
    df.loc[df["dallast5"] == 1, "dallastwk"] = 1
    df.loc[df["dallast5"].isin([2, 3, 4, 5]), "dallastwk"] = 0

    return df


def ethnicgp5(df):
    """Creates the derivation ethnicgp5, which groups ethnic into 5
    uneven bins.
    """

    df["ethnicgp5"] = df["ethnic"]
    df.loc[df["ethnic"].isin([1, 2, 3, 4]), "ethnicgp5"] = 1
    df.loc[df["ethnic"].isin([5, 6, 7, 8]), "ethnicgp5"] = 2
    df.loc[df["ethnic"].isin([9, 10, 11, 12, 13]), "ethnicgp5"] = 3
    df.loc[df["ethnic"].isin([14, 15, 16]), "ethnicgp5"] = 4
    df.loc[df["ethnic"].isin([17, 18]), "ethnicgp5"] = 5

    return df


def ethnicgp4(df):
    """Creates ethnicgp4 from ethnicgp5, which groups 4 and 5 together
    """

    df["ethnicgp4"] = df["ethnicgp5"]
    df.loc[df["ethnicgp5"] == 5, "ethnicgp4"] = 4

    return df


def dcgstg2(df):
    """Creates the derivation dcgstg2, whether the pupil is a current (1)
    or non (2) smoker from cg7, cg7XXX, cgireg, cgstat
    """

    df["dcgstg2"] = df["cgstat"]

    df.loc[df["cgstat"].isin([5, 6]), "dcgstg2"] = 1
    df.loc[df["cgstat"] == 4, "dcgstg2"] = 1
    df.loc[df["cgstat"].isin([1, 2, 3]), "dcgstg2"] = 2
    df.loc[df["cgireg"] == 2, "dcgstg2"] = 2
    df.loc[df["cgireg"] == 3, "dcgstg2"] = 1

    df.loc[
        df["cg7"] == 1
        & (
            df[[
                "cg7mon",
                "cg7tue",
                "cg7wed",
                "cg7thu",
                "cg7fri",
                "cg7sat",
                "cg7sun"]] > 0
        ).any(axis=1)
        & df["cgstat"].isin([1, 2, 3]),
        "dcgstg2"] = 1

    return df


def dcgstg3(df):
    """Creates the derivation dcgstg3, whether the pupil is a regular (1) occasional (2)
    or non (3) smoker from cg7, cg7XXX, cgireg, cgstat
    """

    df["dcgstg3"] = df["cgstat"]

    df.loc[df["cgstat"].isin([5, 6]), "dcgstg3"] = 1
    df.loc[df["cgstat"] == 4, "dcgstg3"] = 2
    df.loc[df["cgstat"].isin([1, 2, 3]), "dcgstg3"] = 3
    df.loc[df["cgireg"] == 2, "dcgstg3"] = 3
    df.loc[df["cgireg"] == 3, "dcgstg3"] = 2

    df.loc[
        df["cg7"] == 1
        & (
            df[[
                "cg7mon",
                "cg7tue",
                "cg7wed",
                "cg7thu",
                "cg7fri",
                "cg7sat",
                "cg7sun"]] > 0
        ).any(axis=1)
        & df["cgstat"].isin([1, 2, 3]),
        "dcgstg3"] = 2

    return df


def dcgstg5(df):
    """Creates the derivation dcgstg5, whether the pupil is a regular (1) occasional (2)
    ex (3) has tried (4) or non (5) smoker from cg7, cg7XXX, cgireg, cgstat
    """

    df["dcgstg5"] = df["cgstat"]

    df.loc[df["cgstat"].isin([5, 6]), "dcgstg5"] = 1
    df.loc[df["cgstat"] == 4, "dcgstg5"] = 2
    df.loc[df["cgstat"] == 3, "dcgstg5"] = 3
    df.loc[df["cgstat"] == 2, "dcgstg5"] = 4
    df.loc[df["cgstat"] == 1, "dcgstg5"] = 5
    df.loc[df["cgireg"] == 2, "dcgstg5"] = 4
    df.loc[df["cgireg"] == 3, "dcgstg5"] = 2

    df.loc[
        df["cg7"] == 1
        & (
            df[[
                "cg7mon",
                "cg7tue",
                "cg7wed",
                "cg7thu",
                "cg7fri",
                "cg7sat",
                "cg7sun"]] > 0
        ).any(axis=1)
        & df["cgstat"].isin([1, 2, 3]),
        "dcgstg5"] = 2

    return df


def ddgmonany(df, all_drugs=param.DRUGS):
    """Creates ddgmonany, whether used any drugs in the last month, from:
    duseamp, dusecan, dusecok, dusecrk,duseecs, dusegas, duseher, duseket
     duseleg, duselsd ,dusemph, dusemsh, dusemth, dusenox, duseoth, dusepop, dusetrn
    """
    input_columns = ["duse" + drug for drug in all_drugs]

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgmonany"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgmonany"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgmonany"] = 1
    df["ddgmonany"] = df["ddgmonany"].fillna(0)

    return df


def ddgyrany(df, all_drugs=param.DRUGS):
    """Creates ddgyrany, whether used any drugs in the last year, from:
    duseamp, dusecan, dusecok, dusecrk,duseecs, dusegas, duseher, duseket
    duseleg, duselsd ,dusemph, dusemsh, dusemth, dusenox, duseoth, dusepop, dusetrn
    """
    input_columns = ["duse" + drug for drug in all_drugs]

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgyrany"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgyrany"] = -8
    df.loc[df[input_columns].isin([1, 2]).any(axis=1), "ddgyrany"] = 1
    df["ddgyrany"] = df["ddgyrany"].fillna(0)

    return df


def ddgany(df, all_drugs=param.DRUGS):
    """Creates ddgany, whether used any drugs, from:
    duseamp, dusecan, dusecok, dusecrk,duseecs, dusegas, duseher, duseket
    duseleg, duselsd ,dusemph, dusemsh, dusemth, dusenox, duseoth, dusepop, dusetrn
    """
    input_columns = ["duse" + drug for drug in all_drugs]

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgany"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgany"] = -8
    df.loc[df[input_columns].isin([1, 2, 3]).any(axis=1), "ddgany"] = 1
    df["ddgany"] = df["ddgany"].fillna(0)

    return df


def ddgdrugs(df):
    """Creates the derivation drugs, defining if the pupil has ever had drugs:
    1 - Never
    2 - At some point
    3 - In the last year
    4 - In the last month
    From variables: ddgmonany, ddgyrany, ddgany
    """

    df["ddgdrugs"] = 1
    df.loc[df[["ddgmonany", "ddgyrany", "ddgany"]].eq(-8).any(axis=1), "ddgdrugs"] = -8
    df.loc[df[["ddgmonany", "ddgyrany", "ddgany"]].eq(-9).any(axis=1), "ddgdrugs"] = -9
    df.loc[df["ddgany"] == 1, "ddgdrugs"] = 2
    df.loc[df["ddgyrany"] == 1, "ddgdrugs"] = 3
    df.loc[df["ddgmonany"] == 1, "ddgdrugs"] = 4

    return df


def dalfam(df):
    """
    Creates the derivation dalfam from the variables alevr,
    alparst, alpar and alparknw.
    What is the pupils perceived parental attitude to drinking

    """
    df.loc[df["alevr"].isin([-8, -9]), "dalfam"] = -9
    df.loc[df["alparst"].isin([1, 2, 3, -8, -9]),
           "dalfam"] = df["alparst"]
    df.loc[(df["dalfam"].isnull()) &
           (df["alpar"].isin([1, 2, 3, -8, -9])),
           "dalfam"] = df["alpar"]
    df.loc[(df["dalfam"].isnull()), "dalfam"] = df["alparknw"]

    return df


def dusexxx(df, all_drugs=param.DRUGS):
    """Creates all drug use variables

     Creates:
    duseamp, dusecan, dusecok, dusecrk,duseecs, dusegas, duseher, duseket,
    duseleg, duselsd ,dusemph, dusemsh dusemth, dusenox, duseoth, dusepop,
    dusetrn

    Using the dghdXXX, dgfqXXX, and dgtdXXX variables

    """

    # Create new lists for each type of input and output
    drug_freq = ["dgfq" + drug for drug in all_drugs]
    drug_heard = ["dghd" + drug for drug in all_drugs]
    drug_tried = ["dgtd" + drug for drug in all_drugs]
    drug_use = ["duse" + drug for drug in all_drugs]

    # Create the new duseXXX column for each drug
    for dgfq, dghd, dgtd, duse in zip(drug_freq, drug_heard, drug_tried, drug_use):
        df[duse] = df[dgfq]
        df.loc[df[dgtd].isin([-8, -9]), duse] = df[dgtd]
        df.loc[df[dgtd] == 2, duse] = 4
        df.loc[df[dghd].isin([-8, -9]), duse] = df[dghd]
        df.loc[df[dghd] == 2, duse] = 4

    return df


def dalfamknw(df):
    """
    Creates the derivation dalfamknw from the variables alevr,
    alfreq, and alpar
    Are parents aware that pupil drinks
    Derived field has 2 non negative outcomes (1 - Do know, 2 - Don't know)

    """
    df.loc[df["alpar"].isin([1, 2, 3]), "dalfamknw"] = 1
    df.loc[df["alpar"] == 4, "dalfamknw"] = 2
    df.loc[(df["alevr"].isin([-8, -9])) | (df["alfreq"].isin([-8, -9])),
           "dalfamknw"] = -9
    df.loc[(df["alfreq"] == 7) | (df["alevr"] == 2), "dalfamknw"] = -1
    df.loc[(df["dalfamknw"].isnull()), "dalfamknw"] = df["alpar"]

    return df


def dfas(df):
    """
    Creates the derivation dfas from the variables ownbed, fambath, famdish,
    famhols, famcomp and famcards
    Calculates score for each variable, then overall family affluence score

    """
    # Create temporary score variables
    df["ownbedscore"] = df["ownbed"]
    df.loc[df["ownbed"] == 2, "ownbedscore"] = 0

    df["fambathscore"] = df["fambath"]
    df.loc[df["fambath"].isin([1, 2, 3, 4]), "fambathscore"] = df["fambath"]-1

    df["famdishscore"] = df["famdish"]
    df.loc[df["famdish"] == 2, "famdishscore"] = 0

    df["famholsscore"] = df["famhols"]
    df.loc[df["famhols"].isin([1, 2, 3, 4]), "famholsscore"] = df["famhols"]-1

    df["famcompscore"] = df["famcomp"]
    df.loc[df["famcomp"].isin([1, 2, 3, 4]), "famcompscore"] = df["famcomp"]-1

    df["famcarsscore"] = df["famcars"]
    df.loc[df["famcars"].isin([1, 2, 3, 4]), "famcarsscore"] = df["famcars"]-1

    # Create dfas based on temp variables
    input_columns = ["ownbedscore", "fambathscore", "famdishscore",
                     "famholsscore", "famcompscore", "famcarsscore"]

    # If any = -9, make dfas -9, then -8, -1, etc.
    df.loc[(df[input_columns] == -9).any(axis=1), "dfas"] = -9
    df.loc[(df[input_columns] == -8).any(axis=1) & (df["dfas"].isnull()),
           "dfas"] = -8
    df.loc[(df[input_columns] == -1).any(axis=1) & (df["dfas"].isnull()),
           "dfas"] = -1

    # Remaining values = sum of scores
    df.loc[df["dfas"].isnull(), "dfas"] = df[input_columns].sum(axis=1)

    # Drop the temp variables
    df.drop(["ownbedscore", "fambathscore", "famdishscore", "famholsscore",
             "famcompscore", "famcarsscore"], axis=1, inplace=True)

    return df


def dfasbands(df):
    """
    Creates the derivation dfasbands from the variable dfas created above
    Groups family affluence score into low, medium or high

    """
    df.loc[df["dfas"] < 0, "dfasbands"] = df["dfas"]
    df.loc[(df["dfas"] < 7) & (df["dfasbands"].isnull()), "dfasbands"] = 1
    df.loc[(df["dfas"] < 11) & (df["dfasbands"].isnull()), "dfasbands"] = 2
    df.loc[(df["dfas"] >= 11), "dfasbands"] = 3

    return df


def dcg7tot(df):
    """
    Creates the derivation dcg7tot (total cigarettes smoked in last week)
    from the cg7 and cg7xxx (days of week) fields.
    """
    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cg7mon",
        "cg7tue",
        "cg7wed",
        "cg7thu",
        "cg7fri",
        "cg7sat",
        "cg7sun"]

    for column in input_columns:

        df[column + "_adj"] = np.where(df[column] < 0, 0, df[column])

    df['dcg7tot'] = (df["cg7mon_adj"] + df["cg7tue_adj"] + df["cg7wed_adj"]
                    + df["cg7thu_adj"] + df["cg7fri_adj"] + df["cg7sat_adj"]
                    + df["cg7sun_adj"])
    df.loc[(df["cg7"] == 1) & (df[input_columns].isin([-1, -8, -9]).all(axis=1)),
           "dcg7tot"] = -8
    df.loc[(df["cg7"] < 0), "dcg7tot"] = df["cg7"]
    df.loc[(df["cg7"] == 2), "dcg7tot"] = 0

    # Drop the temp variables
    df.drop(["cg7mon_adj", "cg7tue_adj", "cg7wed_adj", "cg7thu_adj",
             "cg7fri_adj", "cg7sat_adj", "cg7sun_adj"], axis=1, inplace=True)

    return df


def dcg7totg(df):
    """
    Creates the derivation dcg7totg from the variable dcg7tot
    groups cigarettes smoked last week (7 groups)

    """
    df.loc[df["dcg7tot"] < 0, "dcg7totg"] = df["dcg7tot"]
    df.loc[(df["dcg7tot"] == 0), "dcg7totg"] = 1
    df.loc[(df["dcg7tot"] > 0) & (df["dcg7tot"] < 7), "dcg7totg"] = 2
    df.loc[(df["dcg7tot"] > 6) & (df["dcg7tot"] < 14), "dcg7totg"] = 3
    df.loc[(df["dcg7tot"] > 13) & (df["dcg7tot"] < 21), "dcg7totg"] = 4
    df.loc[(df["dcg7tot"] > 20) & (df["dcg7tot"] < 35), "dcg7totg"] = 5
    df.loc[(df["dcg7tot"] > 34) & (df["dcg7tot"] < 70), "dcg7totg"] = 6
    df.loc[df["dcg7tot"] > 69, "dcg7totg"] = 7

    return df


def dcg7totg2(df):
    """
    Creates the derivation dcg7totgw, cigarettes smoked last week (2 groups)
    From variable: dcg7tot
    """
    df["dcg7totg2"] = df["dcg7tot"]
    df.loc[(df["dcg7tot"] >= 0) & (df["dcg7tot"] < 21), "dcg7totg2"] = 1
    df.loc[df["dcg7tot"] > 20, "dcg7totg2"] = 2

    return df


def dcg7day(df):
    """
    Creates the adjusted versions of the 7 cigarettes smoked in the last week
    questions and the weekly total derived variable.
    Converts them from a count of cigarettes to a 1- yes or 0 - no response
    Both zero and negative values are are derived here as 0 - no, unless dcg7tot
    is a negative number (non-response).
    """

    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cg7mon",
        "cg7tue",
        "cg7wed",
        "cg7thu",
        "cg7fri",
        "cg7sat",
        "cg7sun",
        "dcg7tot"]

    for column in input_columns:

        df.loc[df[column] > 0, "d"+column] = 1
        df.loc[df[column] < 1, "d"+column] = 0
        df.loc[df['dcg7tot'] < 0, "d"+column] = df['dcg7tot']

    df.rename(columns={'ddcg7tot': 'dcg7any'}, inplace=True)    

    return df


def dcgsmk(df):
    """Creates the derivation dcgsmk, defining if the pupil is a current smoker:
    1 - Yes
    0 - No
    From variables: dcgstg3
    """

    df["dcgsmk"] = df["dcgstg3"]
    df.loc[df["dcgstg3"].isin([1, 2]), "dcgsmk"] = 1
    df.loc[df["dcgstg3"] == 3, "dcgsmk"] = 0

    return df


def dlssmk(df):
    """Creates the derivation dlssmk, defining if the pupil recalled having had
    any lessons on smoking in the last year:
    1 - Yes
    0 - No
    From variables: lssmk
    """

    df["dlssmk"] = 0
    df.loc[df["lssmk"] == 1, "dlssmk"] = 1

    return df


def dlsalc(df):
    """Creates the derivation dlsalc, defining if the pupil recalled having had
    any lessons on alcohol use in the last year:
    1 - Yes
    0 - No
    From variables: lsalc
    """

    df["dlsalc"] = 0
    df.loc[df["lsalc"] == 1, "dlsalc"] = 1

    return df


def dlsdrg(df):
    """Creates the derivation dlsdrg, defining if the pupil recalled having had
    any lessons on drug use in the last year:
    1 - Yes
    0 - No
    From variables: lsdrg
    """

    df["dlsdrg"] = 0
    df.loc[df["lsdrg"] == 1, "dlsdrg"] = 1

    return df


def dcggetp(df):
    """
    Creates the derivation dcggetp from the variables cggetgiv, cggetsib,
    cggetpar and cggetelg
    indicates pupils that were given cigarettes by people
    """

    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cggetgiv",
        "cggetsib",
        "cggetpar",
        "cggetelg"]

    df["dcggetp"] = 0

    df.loc[
        df[input_columns].isin([-9]).any(axis=1),
        "dcggetp"] = -9
    df.loc[
        df[input_columns].isin([-1]).all(axis=1),
        "dcggetp"] = -1
    df.loc[
        df[input_columns].isin([1]).any(axis=1),
        "dcggetp"] = 1

    return df


def dcggets(df):
    """
    Creates the derivation dcggets from the variables cggetnew, cggetsup,
    cggetgar and cggetsho
    indicates pupils that bought cigarettes from a shop
    """

    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cggetnew",
        "cggetsup",
        "cggetgar",
        "cggetsho"]

    df["dcggets"] = 0

    df.loc[
        df[input_columns].isin([-9]).any(axis=1),
        "dcggets"] = -9
    df.loc[
        df[input_columns].isin([-1]).all(axis=1),
        "dcggets"] = -1
    df.loc[
        df[input_columns].isin([1]).any(axis=1),
        "dcggets"] = 1

    return df


def dcgbuyp(df):
    """
    Creates the derivation dcgbuyp from the variables cggetfre and cggetels
    indicates pupils that bought cigarettes from people
    """

    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cggetfre",
        "cggetels"]

    df["dcgbuyp"] = 0

    df.loc[
        df[input_columns].isin([-9]).any(axis=1),
        "dcgbuyp"] = -9
    df.loc[
        df[input_columns].isin([-1]).all(axis=1),
        "dcgbuyp"] = -1
    df.loc[
        df[input_columns].isin([1]).any(axis=1),
        "dcgbuyp"] = 1

    return df


def dcgfam(df):
    """
    Creates the derivation family attitudes to smoking.
    From variables: cgfamn, cgfams, cgfamz, cgstat and cgireg.
    Default is -1 as not all pupils are asked this question.

    """
    df["dcgfam"] = -1
    df.loc[(df["cgireg"] == -9) | (df["cgstat"] == -9), "dcgfam"] = -9
    df.loc[(df["cgireg"] == -8) | (df["cgstat"] == -8), "dcgfam"] = -8
    df.loc[df["cgfamn"] != -1, "dcgfam"] = df["cgfamn"]
    df.loc[df["cgfams"] == 6, "dcgfam"] = 5
    df.loc[~df["cgfams"].isin([-1, 6]), "dcgfam"] = df["cgfams"]
    df.loc[df["cgfamz"] != -1, "dcgfam"] = df["cgfamz"]

    return df


def dcgfam4(df):
    """
    Creates the derivation family attitudes to smoking (grouped into 4 options)
    From variable: dcgfam
    """
    df["dcgfam4"] = df["dcgfam"]
    df.loc[df["dcgfam"] == 4, "dcgfam4"] = 3
    df.loc[df["dcgfam"] == 5, "dcgfam4"] = 4

    return df


def dcgppfr(df):
    """
    Creates the derivation if pupils have friends who smoke.
    From variables: cgppfrsa, cgppfrol, cgppfryo and cgppgb.

    """
    df["dcgppfr"] = df["cgppfrsa"]
    df.loc[(df["cgppfrol"] == 1) | (df["cgppfryo"] == 1) | (df["cgppgb"] == 1),
           "dcgppfr"] = 1

    return df


def dcglongg(df):
    """
    Creates the derivation length of time a smoker (grouped into 2)
    From variable: cglong
    """
    df["dcglongg"] = df["cglong"]
    df.loc[df["cglong"].isin([1, 2, 3]), "dcglongg"] = 1
    df.loc[df["cglong"] == 4, "dcglongg"] = 2

    return df


def dcgstopg(df):
    """
    Creates the derivation ease could give up smoking (grouped)
    From variable: cgstop
    """
    df["dcgstopg"] = df["cgstop"]
    df.loc[df["cgstop"].isin([1, 2]), "dcgstopg"] = 1
    df.loc[df["cgstop"].isin([3, 4]), "dcgstopg"] = 2

    return df


def dcgstopwg(df):
    """
    Creates the derivation ease could give up smoking for a week (grouped)
    From variable: cgstopw
    """
    df["dcgstopwg"] = df["cgstopw"]
    df.loc[df["cgstopw"].isin([1, 2]), "dcgstopwg"] = 1
    df.loc[df["cgstopw"].isin([3, 4]), "dcgstopwg"] = 2

    return df


def dcgtrystp(df):
    """
    Creates the derivation dcgtrystp from the variables cgevrstp and cglikstp
    defining whether pupil has tried to give up and if they'd still like to:
    1 - tried to give up, would still like to
    2 - not tried, would like to
    3 - tried, would not like to
    4 - not tried, would not like to
    """

    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cgevrstp",
        "cglikstp"]

    df["dcgtrystp"] = -1

    df.loc[(df["cgevrstp"] == 1) & (df["cglikstp"] == 1),
           "dcgtrystp"] = 1

    df.loc[(df["cgevrstp"] == 2) & (df["cglikstp"] == 1),
           "dcgtrystp"] = 2

    df.loc[(df["cgevrstp"] == 1) & (df["cglikstp"].isin([2, 3])),
           "dcgtrystp"] = 3

    df.loc[(df["cgevrstp"] == 2) & (df["cglikstp"].isin([2, 3])),
           "dcgtrystp"] = 4

    df.loc[
        df[input_columns].isin([-9]).any(axis=1),
        "dcgtrystp"] = -9

    df.loc[
        df[input_columns].isin([-8]).any(axis=1),
        "dcgtrystp"] = -8

    return df


def dcgelbuy(df):
    """
    Creates the derivation whether asked someone to buy cigarettes from a shop
    for them, and whether they did.
    From variables: cgshopp and cgacbsp.
    Default is -1 as not all pupils are asked this question.

    """
    df["dcgelbuy"] = -1
    df.loc[(df["cgshopp"] == -9) | (df["cgacbsp"] == -9), "dcgelbuy"] = -9
    df.loc[(df["cgshopp"] == -8) | (df["cgacbsp"] == -8), "dcgelbuy"] = -8
    df.loc[df["cgshopp"] == 2, "dcgelbuy"] = 3
    df.loc[(df["cgshopp"] == 1) & (df["cgacbsp"] == 2), "dcgelbuy"] = 2
    df.loc[(df["cgshopp"] == 1) & (df["cgacbsp"] == 1), "dcgelbuy"] = 1

    return df


def dcggupxxx(df):
    """Creates 8 derivations for resources used to help give up smoking

    Creates:
    dcgupad, dcgupecg, dcgupfa, dcgupgp, dcguphe, dcgupni, dcgupno, dcgupst
    """

    names = ["dcggupad",
             "dcggupecg",
             "dcggupfa",
             "dcggupgp",
             "dcgguphe",
             "dcggupni",
             "dcggupno",
             "dcggupst"]

    input_columns = [
        ["cggupads", "cggupadn"],
        ["cggupecg", "cggupelc"],
        ["cggupfan", "cggupfas"],
        ["cggupgpn", "cggupgps"],
        ["cgguphen", "cgguphes"],
        ["cggupnin", "cggupnis"],
        ["cggupnon", "cggupnos"],
        ["cggupstn", "cggupsts"],
        ]

    for name, input_column in zip(names, input_columns):
        df[name] = 0

        df.loc[df[input_column].eq(-1).all(axis=1),
            name] = -1

        df.loc[df[input_column].eq(-8).any(axis=1),
            name] = -8

        df.loc[df[input_column].eq(-9).any(axis=1),
            name] = -9

        df.loc[df[input_column].eq(1).any(axis=1),
            name] = 1

        df.loc[df["cgireg"].isin([-8, -9]), name] = -9
        df.loc[df["cgireg"] == 1, name] = -1
        df.loc[df["cgevrstp"].isin([-8, -9]), name] = -9
        df.loc[df["cgevrstp"] == 2, name] = -1
        df.loc[df["cgstat"].isin([-8, -9]), name] = -9

    return df


def dcggupany(df):
    """
    Creates the derivation dcggupany, have pupils used any method to help give
    up smoking.
    From variables: dcggupxxx
    """

    # Define the list of fields that are checked for this derivation
    input_columns = ["dcggupad",
                     "dcggupecg",
                     "dcggupfa",
                     "dcggupgp",
                     "dcgguphe",
                     "dcggupni",
                     "dcggupno",
                     "dcggupst"]

    df["dcggupany"] = 0

    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "dcggupany"] = -9
    df.loc[df[input_columns].eq(-1).all(axis=1), "dcggupany"] = -1
    df.loc[df[input_columns].eq(1).any(axis=1), "dcggupany"] = 1

    return df


def dcgoft(df):
    """
    Creates the derivation smoking status for giving up smoking
    From variable: dcgst5
    """
    df["dcgoft"] = df["dcgstg5"]
    df.loc[df["dcgstg5"].isin([1, 2]), "dcgoft"] = 3
    df.loc[df["dcgstg5"] == 3, "dcgoft"] = 2
    df.loc[df["dcgstg5"] == 4, "dcgoft"] = 1
    df.loc[df["dcgstg5"] == 5, "dcgoft"] = 99

    return df


def dcgsec2(df):
    """
    Creates the derivation whether family knows the pupil smokes (grouped into 2)
    From variable: cgfams
    """
    df["dcgsec2"] = df["cgfams"]
    df.loc[(df["cgfams"].isin([1, 2, 3, 4])) |
           (df["cgfams"] == 6), "dcgsec2"] = 1
    df.loc[df["cgfams"] == 5, "dcgsec2"] = 2

    return df


def dcgppfam(df):
    """
    Creates the derivation if pupils have relatives who smoke.
    From variables: cgpppar, cgppsib, cgppoth

    """
    df["dcgppfam"] = df["cgpppar"]
    df.loc[(df["cgppsib"] == 1) | (df["cgppoth"] == 1),
           "dcgppfam"] = 1

    return df


def dcgshboth(df):
    """
    Creates the derivation dcgshboth from the variables cgshin, cgshcar,
    indicates exposure to second hand smoke in a home or in a car
    """

    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cgshin",
        "cgshcar"]

    df["dcgshboth"] = 0
    df.loc[df[input_columns].eq(-1).all(axis=1), "dcgshboth"] = -1
    df.loc[df[input_columns].isin([6, -9, -8]).any(axis=1), "dcgshboth"] = -9
    df.loc[df[input_columns].isin([1, 2, 3, 4]).any(axis=1), "dcgshboth"] = 1

    return df


def dcgelec(df):
    """
    Creates the derivation dcgelec, pupil e-cig smoking status
    from the variables: cgelechd, cgelecevr

    """
    df["dcgelec"] = df["cgelecevr"]
    df.loc[df["cgelecevr"].isin([1, 2, 3, 4, 5]), "dcgelec"] = df["cgelecevr"]+1
    df.loc[df["cgelechd"] == 2, "dcgelec"] = 1

    return df


def dcgelgtoth(df):
    """
    Creates the derivation if pupils obtain e-cigarettes from other sources,
    adding pharmacy to the original other option
    From variables: cgelgtpha, cgelgtoth
    """
    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cgelgtpha",
        "cgelgtoth"]

    df["dcgelgtoth"] = 0
    df.loc[df[input_columns].eq(-1).all(axis=1), "dcgelgtoth"] = -1
    df.loc[df[input_columns].isin([-9, -8]).any(axis=1), "dcgelgtoth"] = -9
    df.loc[df[input_columns].eq(1).any(axis=1), "dcgelgtoth"] = 1

    return df


def dcgelgtgiv(df):
    """
    Creates the derivation if pupils are usually given e-cigarettes from any source,
    From variables: cgelggiv, cgelgtsib, cgelgpar, cgelgtelg
    """
    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cgelgtgiv",
        "cgelgtsib",
        "cgelgtpar",
        "cgelgtelg"]

    df["dcgelgtgiv"] = 0
    df.loc[df[input_columns].eq(-1).all(axis=1), "dcgelgtgiv"] = -1
    df.loc[df[input_columns].isin([-9, -8]).any(axis=1), "dcgelgtgiv"] = -9
    df.loc[df[input_columns].eq(1).any(axis=1), "dcgelgtgiv"] = 1

    return df


def dcgelgtshp(df):
    """
    Creates the derivation if pupils are usually given e-cigarettes from any shop
    From variables: cgelgtnew, cgelgtsho, cgelgtsup, cgelgtpha, cgelgtgar, cgelgtoth
    """
    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cgelgtnew",
        "cgelgtsho",
        "cgelgtsup",
        "cgelgtpha",
        "cgelgtgar",
        "cgelgtoth"]

    df["dcgelgtshp"] = 0
    df.loc[df[input_columns].eq(-1).all(axis=1), "dcgelgtshp"] = -1
    df.loc[df[input_columns].isin([-9, -8]).any(axis=1), "dcgelgtshp"] = -9
    df.loc[df[input_columns].eq(1).any(axis=1), "dcgelgtshp"] = 1

    return df


def dcgelgtppl(df):
    """
    Creates the derivation if pupils obtain e-cigarettes from people,
    From variables: cgelgtfre, cgelgtels
    """
    # Define the list of fields that are checked for this derivation
    input_columns = [
        "cgelgtfre",
        "cgelgtels"]

    df["dcgelgtppl"] = 0
    df.loc[df[input_columns].eq(-1).all(axis=1), "dcgelgtppl"] = -1
    df.loc[df[input_columns].isin([-9, -8]).any(axis=1), "dcgelgtppl"] = -9
    df.loc[df[input_columns].eq(1).any(axis=1), "dcgelgtppl"] = 1

    return df


def ddgyrty(df, all_drugs=param.DRUGS, a_drugs=param.DRUGS_CLASSA):
    """
    Creates the derivation summary of drugs taken in last year,
    From variables: dusexxx, dgampij and 2 temp variables that count the number
    of non-responses in the duse questions (nonresp_count), and the total count of different
    drugs taken in the last year (lastyr_count)
    """
    # Define the list of drug use fields that are checked for this derivation
    input_columns = ["duse" + drug for drug in all_drugs]

    input_columns_a = ["duse" + drug for drug in a_drugs]

    df["lastyr_count"] = df[input_columns].isin([1, 2]).sum(axis=1)
    df["nonresp_count"] = df[input_columns].isin([-8, -9]).sum(axis=1)

    df["ddgyrty"] = -9
    df.loc[df["lastyr_count"] > 1, "ddgyrty"] = 6
    df.loc[df["lastyr_count"] == 1, "ddgyrty"] = 4
    df.loc[(df["lastyr_count"] == 0) & (df["nonresp_count"] == 0),
           "ddgyrty"] = 7
    df.loc[(df["dusecan"].isin([1, 2])) & (df["lastyr_count"] == 1),
           "ddgyrty"] = 1
    df.loc[(df["dusegas"].isin([1, 2])) & (df["lastyr_count"] == 1),
           "ddgyrty"] = 2
    df.loc[(df[input_columns_a].isin([1, 2]).any(axis=1)) &
           (df["lastyr_count"] == 1),
           "ddgyrty"] = 3
    df.loc[(df["duseamp"].isin([1, 2])) & (df["dgampij"] == 1)
           & (df["lastyr_count"] == 1),
           "ddgyrty"] = 3
    df.loc[(df[input_columns_a].isin([1, 2]).any(axis=1)) &
           (df["lastyr_count"] > 1),
           "ddgyrty"] = 5
    df.loc[(df["duseamp"].isin([1, 2])) & (df["dgampij"] == 1)
           & (df["lastyr_count"] > 1),
           "ddgyrty"] = 5

    # Drop the temp variables
    df.drop(["lastyr_count", "nonresp_count"], axis=1, inplace=True)

    return df


def ddgyrty5(df, all_drugs=param.DRUGS, a_drugs=param.DRUGS_CLASSA):
    """
    Creates the derivation summary of drugs taken in last year (grouped into 5),
    From variables: dusexxx, dgampij and 2 temp variables that count the number
    of non-responses in the duse questions (nonresp_count), and the total count of different
    drugs taken in the last year (lastyr_count)
    """
    # Define the list of drug use fields that are checked for this derivation
    input_columns = ["duse" + drug for drug in all_drugs]

    input_columns_a = ["duse" + drug for drug in a_drugs]

    df["lastyr_count"] = df[input_columns].isin([1, 2]).sum(axis=1)
    df["nonresp_count"] = df[input_columns].isin([-8, -9]).sum(axis=1)

    df["ddgyrty5"] = -9
    df.loc[df["lastyr_count"] > 0, "ddgyrty5"] = 4
    df.loc[(df["lastyr_count"] == 0) & (df["nonresp_count"] == 0),
           "ddgyrty5"] = 5
    df.loc[(df["dusecan"].isin([1, 2])) & (df["lastyr_count"] == 1),
           "ddgyrty5"] = 1
    df.loc[(df["dusegas"].isin([1, 2])) & (df["lastyr_count"] == 1),
           "ddgyrty5"] = 2
    df.loc[df[input_columns_a].isin([1, 2]).any(axis=1),
           "ddgyrty5"] = 3
    df.loc[(df["duseamp"].isin([1, 2])) & (df["dgampij"] == 1),
           "ddgyrty5"] = 3

    # Drop the temp variables
    df.drop(["lastyr_count", "nonresp_count"], axis=1, inplace=True)

    return df


def ddgoc(df):
    """
    Creates the derivation number of occasions taken drugs (grouped into 6)
    from variables dgtdany, dglast, dgoc

    """
    df["ddgoc"] = -1
    df.loc[df["dgoc"].isin([-8, -9]), "ddgoc"] = df["dgoc"]
    df.loc[df["dgtdany"].isin([-8, -9]), "ddgoc"] = df["dgtdany"]
    df.loc[df["dgtdany"] == 2, "ddgoc"] = 1
    df.loc[df["dglast"] == 3, "ddgoc"] = 2
    df.loc[df["dgoc"] == 1, "ddgoc"] = 3
    df.loc[df["dgoc"] == 2, "ddgoc"] = 4
    df.loc[df["dgoc"] == 3, "ddgoc"] = 5
    df.loc[df["dgoc"] == 4, "ddgoc"] = 6

    return df


def ddgoc4(df):
    """
    Creates the derivation number of occasions taken drugs (grouped into 4)
    from derivation ddgoc
    1: never taken, 2: not taken in last year, 3: 1-5 occasions, 4: 6+ occasions

    """
    df["ddgoc4"] = df["ddgoc"]
    df.loc[df["ddgoc"].isin([3, 4]), "ddgoc4"] = 3
    df.loc[df["ddgoc"].isin([5, 6]), "ddgoc4"] = 4

    return df


def ddganyresponse(df, all_drugs=param.DRUGS):
    """
    Creates the derivation ddganyresponse indicating whether a pupil
    gave a response to any of the drug use questions:
    duseamp, dusecan, dusecok, dusecrk, duseecs, dusegas, duseher, duseket
    duseleg, duselsd ,dusemph, dusemsh, dusemth, dusenox, duseoth, dusepop,
    dusetrn

    """
    # Define the list of fields that are checked for this derivation
    input_columns = ["duse" + drug for drug in all_drugs]

    df["ddganyresponse"] = 1
    df.loc[df[input_columns].isin([-1, -8, -9]).all(axis=1),
           "ddganyresponse"] = -9

    return df


def ddganynotvs(df, all_drugs=param.DRUGS):
    """
    Creates ddganynotvs, whether ever used any drugs
    (excluding volatile substances: dusegas)
    """
    # copy list of all drugs and remove gas entry
    drugs_not_vs = all_drugs.copy()
    drugs_not_vs.remove("gas")

    # recreate column names and generate values
    input_columns = ["duse" + drug for drug in drugs_not_vs]

    df["ddganynotvs"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddganynotvs"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddganynotvs"] = -8
    df.loc[df[input_columns].isin([1, 2, 3]).any(axis=1), "ddganynotvs"] = 1

    return df


def ddgmonanynotvs(df, all_drugs=param.DRUGS):
    """
    Creates ddgmonanynotvs, whether used any drugs in last month
    (excluding volatile substances: dusegas)
    """

    # copy list of all drugs and remove gas entry
    drugs_not_vs = all_drugs.copy()
    drugs_not_vs.remove("gas")

    # recreate column names and generate values
    input_columns = ["duse" + drug for drug in drugs_not_vs]

    df["ddgmonanynotvs"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgmonanynotvs"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgmonanynotvs"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgmonanynotvs"] = 1

    return df


def ddgyranynotvs(df, all_drugs=param.DRUGS):
    """
    Creates ddgyranynotvs, whether used any drugs in last year
    (excluding volatile substances: dusegas)
    """

    # copy list of all drugs and remove gas entry
    drugs_not_vs = all_drugs.copy()
    drugs_not_vs.remove("gas")

    # recreate column names and generate values
    input_columns = ["duse" + drug for drug in drugs_not_vs]

    df["ddgyranynotvs"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgyranynotvs"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgyranynotvs"] = -8
    df.loc[df[input_columns].isin([1, 2]).any(axis=1), "ddgyranynotvs"] = 1

    return df


def ddganynotps(df, all_drugs=param.DRUGS):
    """
    Creates ddganynotps, whether ever used any drugs
    (excluding psychoactive substances: duseleg and dusenox)
    """
    # copy list of all drugs and remove psychoactive drugs
    drugs_not_ps = all_drugs.copy()

    remove_drugs = ["leg", "nox"]

    for drug in remove_drugs:
        drugs_not_ps.remove(drug)

    # recreate column names and generate values
    input_columns = ["duse" + drug for drug in drugs_not_ps]

    df["ddganynotps"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddganynotps"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddganynotps"] = -8
    df.loc[df[input_columns].isin([1, 2, 3]).any(axis=1), "ddganynotps"] = 1

    return df


def ddgmonanynotps(df, all_drugs=param.DRUGS):
    """
    Creates ddgmonanynotps, whether used any drugs in last month
    (excluding psychoactive substances: duseleg and dusenox)
    """
    # copy list of all drugs and remove psychoactive drugs
    drugs_not_ps = all_drugs.copy()

    remove_drugs = ["leg", "nox"]

    for drug in remove_drugs:
        drugs_not_ps.remove(drug)

    # recreate column names and generate values
    input_columns = ["duse" + drug for drug in drugs_not_ps]

    df["ddgmonanynotps"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgmonanynotps"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgmonanynotps"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgmonanynotps"] = 1

    return df


def ddgyranynotps(df, all_drugs=param.DRUGS):
    """
    Creates ddgyranynotps, whether used any drugs in last year
    (excluding psychoactive substances: duseleg and dusenox)
    """
    # copy list of all drugs and remove psychoactive drugs
    drugs_not_ps = all_drugs.copy()

    remove_drugs = ["leg", "nox"]

    for drug in remove_drugs:
        drugs_not_ps.remove(drug)

    # recreate column names and generate values
    input_columns = ["duse" + drug for drug in drugs_not_ps]

    df["ddgyranynotps"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgyranynotps"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgyranynotps"] = -8
    df.loc[df[input_columns].isin([1, 2]).any(axis=1), "ddgyranynotps"] = 1

    return df


def ddgevrcla(df, a_drugs=param.DRUGS_CLASSA):
    """
    Creates ddgevrcla, whether ever used Class A drugs, from:
    duseamp, dgampij, duseecs, dusecok, dusecrk, duseher, duselsd, dusemsh
    and dusemth
    """
    input_columns_a = ["duse" + drug for drug in a_drugs]

    input_columns = input_columns_a + ["duseamp", "dgampij"]

    df["ddgevrcla"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgevrcla"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgevrcla"] = -8

    df.loc[df[input_columns_a].isin([1, 2, 3]).any(axis=1), "ddgevrcla"] = 1

    df.loc[(df["duseamp"].isin([1, 2, 3]))
           & (df["dgampij"] == 1), "ddgevrcla"] = 1

    return df


def ddgmoncla(df, a_drugs=param.DRUGS_CLASSA):
    """
    Creates ddgmoncla, whether used Class A drugs in last month, from:
    duseamp, dgampij, duseecs, dusecok, dusecrk, duseher, duselsd, dusemsh
    and dusemth
    """
    input_columns_a = ["duse" + drug for drug in a_drugs]

    input_columns = input_columns_a + ["duseamp", "dgampij"]

    df["ddgmoncla"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgmoncla"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgmoncla"] = -8

    df.loc[df[input_columns_a].eq(1).any(axis=1), "ddgmoncla"] = 1

    df.loc[(df["duseamp"] == 1) & (df["dgampij"] == 1), "ddgmoncla"] = 1

    return df


def ddgyrcla(df, a_drugs=param.DRUGS_CLASSA):
    """
    Creates ddgyrcla, whether used Class A drugs in last year, from:
    duseamp, dgampij, duseecs, dusecok, dusecrk, duseher, duselsd, dusemsh
    and dusemth
    """
    input_columns_a = ["duse" + drug for drug in a_drugs]

    input_columns = input_columns_a + ["duseamp", "dgampij"]

    df["ddgyrcla"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgyrcla"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgyrcla"] = -8

    df.loc[df[input_columns_a].isin([1, 2]).any(axis=1), "ddgyrcla"] = 1

    df.loc[(df["duseamp"].isin([1, 2]))
           & (df["dgampij"] == 1), "ddgyrcla"] = 1

    return df


def ddgevropi(df):
    """
    Creates ddgevropi, whether ever used opiods, from:
    duseher and dusemth
    """
    input_columns = ["duseher", "dusemth"]

    df["ddgevropi"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgevropi"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgevropi"] = -8
    df.loc[df[input_columns].isin([1, 2, 3]).any(axis=1), "ddgevropi"] = 1

    return df


def ddgmonopi(df):
    """
    Creates ddgmonopi, whether used opiods in last month, from:
    duseher and dusemth
    """
    input_columns = ["duseher", "dusemth"]

    df["ddgmonopi"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgmonopi"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgmonopi"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgmonopi"] = 1

    return df


def ddgyropi(df):
    """
    Creates ddgyropi, whether used opiods in last year, from:
    duseher and dusemth
    """
    input_columns = ["duseher", "dusemth"]

    df["ddgyropi"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgyropi"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgyropi"] = -8
    df.loc[df[input_columns].isin([1, 2]).any(axis=1), "ddgyropi"] = 1

    return df


def ddgevrps(df):
    """
    Creates ddgevrps, whether ever used psychoactive substances, from:
    duseleg and dusenox
    """
    input_columns = ["duseleg", "dusenox"]

    df["ddgevrps"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgevrps"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgevrps"] = -8
    df.loc[df[input_columns].isin([1, 2, 3]).any(axis=1), "ddgevrps"] = 1

    return df


def ddgmonps(df):
    """
    Creates ddgmonps, whether used psychoactive substances in last month, from:
    duseleg and dusenox
    """
    input_columns = ["duseleg", "dusenox"]

    df["ddgmonps"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgmonps"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgmonps"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgmonps"] = 1

    return df


def ddgyrps(df):
    """
    Creates ddgyrps, whether used psychoactive substances in last year, from:
    duseleg and dusenox
    """
    input_columns = ["duseleg", "dusenox"]

    df["ddgyrps"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgyrps"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgyrps"] = -8
    df.loc[df[input_columns].isin([1, 2]).any(axis=1), "ddgyrps"] = 1

    return df


def ddgevrpsy(df):
    """
    Creates ddgevrpsy, whether ever used psychedelics, from:
    dusemsh, duselsd and duseket
    """
    input_columns = ["dusemsh", "duselsd", "duseket"]

    df["ddgevrpsy"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgevrpsy"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgevrpsy"] = -8
    df.loc[df[input_columns].isin([1, 2, 3]).any(axis=1), "ddgevrpsy"] = 1

    return df


def ddgmonpsy(df):
    """
    Creates ddgmonpsy, whether used psychedelics in last month, from:
    dusemsh, duselsd and duseket
    """
    input_columns = ["dusemsh", "duselsd", "duseket"]

    df["ddgmonpsy"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgmonpsy"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgmonpsy"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgmonpsy"] = 1

    return df


def ddgyrpsy(df):
    """
    Creates ddgyrpsy, whether used psychedelics in last year, from:
    dusemsh, duselsd and duseket
    """
    input_columns = ["dusemsh", "duselsd", "duseket"]

    df["ddgyrpsy"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgyrpsy"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgyrpsy"] = -8
    df.loc[df[input_columns].isin([1, 2]).any(axis=1), "ddgyrpsy"] = 1

    return df


def ddgevrstm(df):
    """
    Creates ddgevrstm, whether ever used stimulants, from:
    duseecs, dusecok, dusecrk, dusepop, dusemph and duseamp
    """
    input_columns = ["duseecs", "dusecok", "dusecrk", "dusepop", "dusemph",
                     "duseamp"]

    df["ddgevrstm"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgevrstm"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgevrstm"] = -8
    df.loc[df[input_columns].isin([1, 2, 3]).any(axis=1), "ddgevrstm"] = 1

    return df


def ddgmonstm(df):
    """
    Creates ddgmonstm, whether used stimulants in last month, from:
    duseecs, dusecok, dusecrk, dusepop, dusemph and duseamp
    """
    input_columns = ["duseecs", "dusecok", "dusecrk", "dusepop", "dusemph",
                     "duseamp"]

    df["ddgmonstm"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgmonstm"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgmonstm"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgmonstm"] = 1

    return df


def ddgyrstm(df):
    """
    Creates ddgyrstm, whether used stimulants in last year, from:
    duseecs, dusecok, dusecrk, dusepop, dusemph and duseamp
    """
    input_columns = ["duseecs", "dusecok", "dusecrk", "dusepop", "dusemph",
                     "duseamp"]

    df["ddgyrstm"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgyrstm"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgyrstm"] = -8
    df.loc[df[input_columns].isin([1, 2]).any(axis=1), "ddgyrstm"] = 1

    return df


def ddgtypleg(df):
    """
    Creates ddgtypleg, type of psychoactive substance used on most recent occasion,
    with non-responses concerted to 5 for table output
    from: dgtypleg
    """
    df["ddgtypleg"] = df["dgtypleg"]
    df.loc[df["dgtypleg"] < 0, "ddgtypleg"] = 5

    return df


def ddgfq6(df):
    """
    Creates ddgfq6, usual frequency take drugs (6 cats)
    from: dgtdany, dglast, dgoc, dgusefq

    """

    df["ddgfq6"] = -9
    df.loc[df["dgusefq"] == -8, "ddgfq6"] = -8
    df.loc[df["dgusefq"] == 5, "ddgfq6"] = 3
    df.loc[df["dgusefq"] == 4, "ddgfq6"] = 2
    df.loc[df["dgusefq"].isin([1, 2, 3]), "ddgfq6"] = 1
    df.loc[df["dgoc"].isin([-8, -9]), "ddgfq6"] = df["dgoc"]
    df.loc[df["dgoc"] == 1, "ddgfq6"] = 4
    df.loc[df["dglast"].isin([-8, -9]), "ddgfq6"] = df["dglast"]
    df.loc[df["dglast"] == 3, "ddgfq6"] = 5
    df.loc[df["dgtdany"].isin([-8, -9]), "ddgfq6"] = df["dgtdany"]
    df.loc[df["dgtdany"] == 2, "ddgfq6"] = 6

    return df


def ddgfq8(df):
    """
    Creates the derivation ddgfq8 usual frquency of drug use (8 categories)
    from: dgtdany, dglast, dgoc and dgusefq
    """
    df["ddgfq8"] = -9
    df.loc[df["dgusefq"].isin([1, 2, 3, 4, 5, -8, -9]),
           "ddgfq8"] = df["dgusefq"]
    df.loc[df["dgoc"].isin([-8, -9]), "ddgfq8"] = df["dgoc"]
    df.loc[df["dgoc"] == 1, "ddgfq8"] = 6
    df.loc[df["dglast"].isin([-8, -9]), "ddgfq8"] = df["dglast"]
    df.loc[df["dglast"] == 3, "ddgfq8"] = 7
    df.loc[df["dgtdany"].isin([-8, -9]), "ddgfq8"] = df["dgtdany"]
    df.loc[df["dgtdany"] == 2, "ddgfq8"] = 8

    return df


def dtruexc(df):
    """
    Creates the derivation dtruexc whether pupil has ever played truant or been
    expelled
    from: truant, excla
    """

    # Define the list of fields that are checked for this derivation
    input_columns = [
        "truant",
        "excla"]

    df["dtruexc"] = -9
    df.loc[df[input_columns].eq(2).all(axis=1), "dtruexc"] = 2
    df.loc[df[input_columns].eq(1).any(axis=1), "dtruexc"] = 1

    return df


def ddgofxxx(df, all_drugs=param.DRUGS):
    """Creates all variables for whether pupils have been offered individual
    drug types.

     Creates:
    ddgofamp, ddgofcan, ddgofcok, ddgofcrk,ddgofecs, ddgofgas, ddgofher, ddgofket,
    ddgofleg, ddgoflsd ,ddgofmph, ddgofmsh ddgofmth, ddgofnox, ddgofoth, ddgofpop,
    ddgoftrn

    Using the dghdXXX and dgofXXXvariables
    """

    # Create new lists for each type of input and output
    drug_heard = ["dghd" + drug for drug in all_drugs]
    drug_off = ["dgof" + drug for drug in all_drugs]
    drug_off_derived = ["ddgof" + drug for drug in all_drugs]

    # Create the new ddgofXXX column for each drug
    for dghd, dgof, ddgof in zip(drug_heard, drug_off, drug_off_derived):
        df[ddgof] = df[dgof]
        df.loc[df[dghd].isin([2, -8, -9]), ddgof] = df[dghd]

    return df


def ddgofany(df, all_drugs=param.DRUGS):
    """Creates ddgofany, whether ever offered any drugs, from:
    ddgofamp, ddgofcan, ddgofcok, ddgofcrk,ddgofecs, ddgofgas, ddgofher, ddgofket
    ddgofleg, ddgoflsd ,ddgofmph, ddgofmsh, ddgofmth, ddgofnox, ddgofoth, ddgofpop,
    ddgoftrn
    """
    input_columns = ["ddgof" + drug for drug in all_drugs]

    df["ddgofany"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgofany"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgofany"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgofany"] = 1

    return df


def ddgofanyresponse(df, all_drugs=param.DRUGS):
    """
    Creates the derivation ddgofanyresponse indicating whether a pupil
    gave a response to any of the drug offered questions:
    ddgofamp, ddgofcan, ddgofcok, ddgofcrk,ddgofecs, ddgofgas, ddgofher, ddgofket,
    ddgofleg, ddgoflsd ,ddgofmph, ddgofmsh ddgofmth, ddgofnox, ddgofoth, ddgofpop,
    ddgoftrn

    """
    # Define the list of fields that are checked for this derivation
    input_columns = ["ddgof" + drug for drug in all_drugs]

    df["ddgofanyresponse"] = 1
    df.loc[df[input_columns].isin([-1, -8, -9]).all(axis=1),
           "ddgofanyresponse"] = -9

    return df


def ddgofanynotps(df, all_drugs=param.DRUGS):
    """
    Creates ddgofanynotps, whether ever offered any drugs
    (excluding psychoactive substances: duseleg and dusenox)
    """
    # copy list of all drugs and remove psychoactive drugs
    drugs_not_ps = all_drugs.copy()

    remove_drugs = ["leg", "nox"]

    for drug in remove_drugs:
        drugs_not_ps.remove(drug)

    # recreate column names and generate values
    input_columns = ["ddgof" + drug for drug in drugs_not_ps]

    df["ddgofanynotps"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgofanynotps"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgofanynotps"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgofanynotps"] = 1

    return df


def ddgfam(df):
    """
    Creates ddgfam, categorises family attitudes to pupils taking drugs:
    5 groups - try to stop, try to persuade not to, do nothing, encourage,
    don't know
    from: dgfamst, dgfaml and dgfamkn
    """
    df["ddgfam"] = -1

    df.loc[df["dgfamst"].isin([1, 2, 3, 4, 5, -8, -9]), "ddgfam"] = df["dgfamst"]

    df.loc[df["dgfamfl"].isin([1, 2, 3, 4, -8, -9]), "ddgfam"] = df["dgfamfl"]
    df.loc[df["dgfamfl"] == 6, "ddgfam"] = 5

    df.loc[df["dgfamkn"].isin([1, 2, 3, 4, 5, -8, -9]), "ddgfam"] = df["dgfamkn"]

    return df


def ddgfam4(df):
    """
    Creates ddgfam4 from derivation ddgfam, grouping into 4 groups
    1: try to stop, 2: try to persuade not to, 3: do nothing/encourage,
    4: don't know
    """
    df["ddgfam4"] = df["ddgfam"]

    df.loc[df["ddgfam"].isin([3, 4]), "ddgfam4"] = 3
    df.loc[df["ddgfam"] == 5, "ddgfam4"] = 4

    return df


def ddgofstm(df):
    """
    Creates ddgofstm, whether ever offered stimulants, from:
    ddgofecs, ddgofcok, ddgofcrk, ddgofpop, ddgofmph and ddgofamp
    """
    input_columns = ["ddgofecs", "ddgofcok", "ddgofcrk", "ddgofpop", "ddgofmph",
                     "ddgofamp"]

    df["ddgofstm"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgofstm"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgofstm"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgofstm"] = 1

    return df


def ddgofpsy(df):
    """
    Creates ddgofpsy, whether ever offered psychedelics, from:
    ddgofmsh, ddgoflsd and ddgofket
    """
    input_columns = ["ddgofmsh", "ddgoflsd", "ddgofket"]

    df["ddgofpsy"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgofpsy"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgofpsy"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgofpsy"] = 1

    return df


def ddgofps(df):
    """
    Creates ddgofps, whether offered psychoactive substances, from:
    ddgofleg and ddgofnox
    """
    input_columns = ["ddgofleg", "ddgofnox"]

    df["ddgofps"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgofps"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgofps"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgofps"] = 1

    return df


def ddgofopi(df):
    """
    Creates ddgofopi, whether offered opiods, from:
    ddgofher and ddgofmth
    """
    input_columns = ["ddgofher", "ddgofmth"]

    df["ddgofopi"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgofopi"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgofopi"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgofopi"] = 1

    return df


def ddgofcla(df, a_drugs=param.DRUGS_CLASSA):
    """Creates ddgofcla, whether ever offered any class a drugs, from:
    ddgofamp, ddgofecs, ddgofcok, ddgofcrk, ddgofher, ddgoflsd, ddgofmsh
    and ddgofmth
    """
    input_columns_a = ["ddgof" + drug for drug in a_drugs]

    input_columns = input_columns_a + ["ddgofamp"]

    df["ddgofcla"] = 2

    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgofcla"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgofcla"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgofcla"] = 1

    return df


def ddgageany(df, all_drugs=param.DRUGS):
    """
    Creates ddgageany, age at first drug use for any drug, from:
    dgagexxx (age first tried each drug)
    """
    input_columns = ["dgage" + drug for drug in all_drugs]

    # Create names for the adjusted dage variables
    input_columns_adj = ["adj" + drug for drug in all_drugs]

    # Add adjusted dgage cols replacing -1 with 9999 so that it won't be considered
    # the min value when there are other values present in other columns)
    for col, col_adj in zip(input_columns, input_columns_adj):
        df[col_adj] = df[col]
        df[col_adj].replace({-1: 9999}, inplace=True)

    # Assign the min value across all columns to ddgage, then make adjustments
    # for non-responses
    df["ddgageany"] = df[input_columns_adj].min(axis=1)

    df.loc[df["ddgageany"].eq(9999), "ddgageany"] = -1
    df.loc[df["ddgageany"].isin([1, 2, 3, 4]), "ddgageany"] = -9
    df.loc[df[input_columns].eq(-9).any(axis=1), "ddgageany"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddgageany"] = -8

    # Drop the adjusted columns
    df.drop(input_columns_adj, axis=1, inplace=True)

    return df


def ddgageany11(df):
    """
    Creates ddgage11, age at first drug use, with ages 11 or below,
    and 15 or above grouped
    from: ddgageany
    """
    df["ddgageany11"] = df["ddgageany"]
    df.loc[df["ddgageany"].isin([5, 6, 7, 8, 9, 10]), "ddgageany11"] = 11
    df.loc[df["ddgageany"] >= 15, "ddgageany11"] = 15

    return df


def ddgagexxx(df, all_drugs=param.DRUGS):
    """
    Creates ddgagexxx, whether tried each drug at age first took drugs (yes or no)
    from: dgagexxx (age first tried each drug) and ddgadeany (age first tried any drug)
    """
    # Create new lists for the input and output variables
    input_columns = ["dgage" + drug for drug in all_drugs]
    output_columns = ["ddgage" + drug for drug in all_drugs]

    # Create the new ddgageXXX column for each drug
    for dgage, ddgage in zip(input_columns, output_columns):
        df[ddgage] = 0
        df.loc[df["ddgageany"] < 0, ddgage] = df["ddgageany"]
        df.loc[(df[dgage].eq(df["ddgageany"])) & (df[dgage] > 4),
               ddgage] = 1

    return df


def ddgfirst(df, all_drugs=param.DRUGS, a_drugs=param.DRUGS_CLASSA):
    """
    Creates ddgfirst, type of drug tried at age first took drugs, grouped.
    from: ddgagexxx (which drugs tried at age first took drugs)
    and ddgageany (age first tried any drug)
    """
    # create a list of all drugs excluding cannabis
    drugs_not_can = all_drugs.copy()
    drugs_not_can.remove("can")

    # Create a list of all drugs excluding volatile substances
    drugs_not_vs = all_drugs.copy()
    drugs_not_vs.remove("gas")

    # Create a list of non-Class A drugs
    drugs_not_a = [i for i in all_drugs if i not in a_drugs]

    # Create lists of variable names for all the required inputs
    input_columns_a = ["ddgage" + drug for drug in a_drugs] + ["ddgageamp"]
    input_columns_not_can = ["ddgage" + drug for drug in drugs_not_can]
    input_columns_not_vs = ["ddgage" + drug for drug in drugs_not_vs]
    input_columns_not_a = ["ddgage" + drug for drug in drugs_not_a]

    df["ddgfirst"] = df["ddgageany"]

    df.loc[df[input_columns_not_a].eq(1).any(axis=1), "ddgfirst"] = 4
    df.loc[df[input_columns_a].eq(1).any(axis=1), "ddgfirst"] = 3
    df.loc[(df[input_columns_not_vs].ne(1).all(axis=1)) & (df["ddgagegas"] == 1),
           "ddgfirst"] = 2
    df.loc[(df[input_columns_not_can].ne(1).all(axis=1)) & (df["ddgagecan"] == 1),
           "ddgfirst"] = 1

    return df


def ddgfttyp(df, all_drugs=param.DRUGS, a_drugs=param.DRUGS_CLASSA):
    """
    Creates ddgfttyp, drug tried at first drug use, grouped.
    from: dgfttdxxx (which drugs tried at first drug use)
    """
    # TODO Consider updating the drug field suffixes so all are vs (not gas)
    # The suffix gas is replaced by vs in these fields so the drug parameter
    # lists need adjusting to reflect this.
    all_drugs_adj = all_drugs.copy()
    all_drugs_adj.remove("gas")
    all_drugs_adj = all_drugs_adj + ["vs"]

    # create a list of all drugs excluding cannabis
    drugs_not_can = all_drugs_adj.copy()
    drugs_not_can.remove("can")

    # Create a list of all drugs excluding volatile substances
    drugs_not_vs = all_drugs_adj.copy()
    drugs_not_vs.remove("vs")

    # Create a list of non-Class A drugs
    drugs_not_a = [i for i in all_drugs_adj if i not in a_drugs]

    # Create lists of variable names for all the required inputs
    input_columns_a = ["dgfttd" + drug for drug in a_drugs] + ["dgfttdamp"]
    input_columns_not_can = ["dgfttd" + drug for drug in drugs_not_can]
    input_columns_not_vs = ["dgfttd" + drug for drug in drugs_not_vs]
    input_columns_not_a = ["dgfttd" + drug for drug in drugs_not_a]

    df["ddgfttyp"] = -1

    df.loc[df["dgfttdcan"].isin([-8, -9]), "ddgfttyp"] = df["dgfttdcan"]
    df.loc[df[input_columns_not_a].eq(1).any(axis=1), "ddgfttyp"] = 4
    df.loc[df[input_columns_a].eq(1).any(axis=1), "ddgfttyp"] = 3
    df.loc[(df[input_columns_not_vs].ne(1).all(axis=1)) & (df["dgfttdvs"] == 1),
           "ddgfttyp"] = 2
    df.loc[(df[input_columns_not_can].ne(1).all(axis=1)) & (df["dgfttdcan"] == 1),
           "ddgfttyp"] = 1

    return df


def ddghdnotaw(df, all_drugs=param.DRUGS):
    """Creates ddghdnotaw, whether not aware of any drugs, from:
    dghdcan, dghdamp, dghdlsd, dghdecs, dghdpop, dghdtrn, dghdher, dghdmsh,
    dghdmth, dghdcrk, dghdcok, dghdket, dghdmph, dghdleg, dghdnox,
    dghdoth

    """
    # Create a list of all drugs excluding volatile substances
    drugs_not_gas = all_drugs.copy()
    drugs_not_gas.remove("gas")

    input_columns = ["dghd" + drug for drug in drugs_not_gas]

    df["ddghdnotaw"] = -9

    df.loc[df[input_columns].eq(1).any(axis=1), "ddghdnotaw"] = 2
    df.loc[df[input_columns].eq(2).all(axis=1), "ddghdnotaw"] = 1

    return df


def ddghdanyresponse(df, all_drugs=param.DRUGS):
    """
    Creates the derivation ddghdanyresponse indicating whether a pupil
    gave a response to any of the drug aware questions:
    dghdcan, dghdamp, dghdlsd, dghdecs, dghdpop, dghdtrn, dghdher, dghdmsh,
    dghdmth, dghdcrk, dghdcok, dghdket, dghdmph, dghdleg, dghdnox,
    dghdoth

    """
    # Create a list of all drugs excluding volatile substances
    drugs_not_gas = all_drugs.copy()
    drugs_not_gas.remove("gas")

    # Define the list of fields that are checked for this derivation
    input_columns = ["dghd" + drug for drug in drugs_not_gas]

    df["ddghdanyresponse"] = 1
    df.loc[df[input_columns].isin([-1, -8, -9]).all(axis=1),
           "ddghdanyresponse"] = -9

    return df


def ddghdnotawexps(df, all_drugs=param.DRUGS):
    """
    Creates ddghdnotawexps, whether not aware of any drugs
    (excluding psychoactive substances: dghdleg and dghdnox)

    """

    # copy list of all drugs and remove psychoactive drugs and volatile
    # substances

    drugs_not_ps = all_drugs.copy()

    remove_drugs = ["leg", "nox", "gas"]

    for drug in remove_drugs:
        drugs_not_ps.remove(drug)

    # recreate column names and generate values
    input_columns = ["dghd" + drug for drug in drugs_not_ps]

    df["ddghdnotawexps"] = -9

    df.loc[df[input_columns].eq(1).any(axis=1), "ddghdnotawexps"] = 2
    df.loc[df[input_columns].eq(2).all(axis=1), "ddghdnotawexps"] = 1

    return df


def ddglttyp(df, all_drugs=param.DRUGS, a_drugs=param.DRUGS_CLASSA):
    """
    Creates ddglttyp, drug tried on most recent occasion, grouped.
    from: dglttdxxx (which drugs tried at last drug use)
    """
    # TODO Consider updating the drug field suffixes so all are vs (not gas)
    # The suffix gas is replaced by vs in these fields so the drug parameter
    # lists need adjusting to reflect this.
    all_drugs_adj = all_drugs.copy()
    all_drugs_adj.remove("gas")
    all_drugs_adj = all_drugs_adj + ["vs"]

    # create a list of all drugs excluding cannabis
    drugs_not_can = all_drugs_adj.copy()
    drugs_not_can.remove("can")

    # Create a list of all drugs excluding volatile substances
    drugs_not_vs = all_drugs_adj.copy()
    drugs_not_vs.remove("vs")

    # Create a list of non-Class A drugs
    drugs_not_a = [i for i in all_drugs_adj if i not in a_drugs]

    # Create lists of variable names for all the required inputs
    input_columns_a = ["dglttd" + drug for drug in a_drugs] + ["dglttdamp"]
    input_columns_not_can = ["dglttd" + drug for drug in drugs_not_can]
    input_columns_not_vs = ["dglttd" + drug for drug in drugs_not_vs]
    input_columns_not_a = ["dglttd" + drug for drug in drugs_not_a]

    df["ddglttyp"] = -1

    df.loc[df["dglttdcan"].isin([-8, -9]), "ddglttyp"] = df["dglttdcan"]
    df.loc[df[input_columns_not_a].eq(1).any(axis=1), "ddglttyp"] = 4
    df.loc[df[input_columns_a].eq(1).any(axis=1), "ddglttyp"] = 3
    df.loc[(df[input_columns_not_vs].ne(1).all(axis=1)) & (df["dglttdvs"] == 1),
           "ddglttyp"] = 2
    df.loc[(df[input_columns_not_can].ne(1).all(axis=1)) & (df["dglttdcan"] == 1),
           "ddglttyp"] = 1

    return df


def ddghdstm(df):
    """
    Creates ddghdstm, whether aware of stimulants, from:
    dghdamp, dghdecs, dghdpop, dghdcrk, dghdcok and dghdmph
    """
    input_columns = ["dghdamp", "dghdecs", "dghdpop", "dghdcrk", "dghdcok",
                     "dghdmph"]

    df["ddghdstm"] = -1

    df.loc[df[input_columns].eq(2).any(axis=1), "ddghdstm"] = 2
    df.loc[df[input_columns].eq(-9).any(axis=1), "ddghdstm"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddghdstm"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddghdstm"] = 1

    return df


def ddghdpsy(df):
    """
    Creates ddghdpsy, whether aware of psychedelics, from:
    dghdmsh, dghdlsd and dghdket
    """
    input_columns = ["dghdmsh", "dghdlsd", "dghdket"]

    df["ddghdpsy"] = -1

    df.loc[df[input_columns].eq(2).any(axis=1), "ddghdpsy"] = 2
    df.loc[df[input_columns].eq(-9).any(axis=1), "ddghdpsy"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddghdpsy"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddghdpsy"] = 1

    return df


def ddghdps(df):
    """
    Creates dghdps, whether aware of psychoactive substances, from:
    dghdleg and dghdnox
    """
    input_columns = ["dghdleg", "dghdnox"]

    df["ddghdps"] = -1

    df.loc[df[input_columns].eq(2).any(axis=1), "ddghdps"] = 2
    df.loc[df[input_columns].eq(-9).any(axis=1), "ddghdps"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddghdps"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddghdps"] = 1

    return df


def ddghdopi(df):
    """
    Creates ddghdopi, whether aware of opiods, from:
    dghdher and dghdmth
    """
    input_columns = ["dghdher", "dghdmth"]

    df["ddghdopi"] = -1

    df.loc[df[input_columns].eq(2).any(axis=1), "ddghdopi"] = 2
    df.loc[df[input_columns].eq(-9).any(axis=1), "ddghdopi"] = -9
    df.loc[df[input_columns].eq(-8).any(axis=1), "ddghdopi"] = -8
    df.loc[df[input_columns].eq(1).any(axis=1), "ddghdopi"] = 1

    return df


def ddgltwofre(df):
    """
    Creates the derivation ddgltwofre, pupils who took drugs most recently with
    any friend
    from: dgltwofro, dgltwofrb, dgltwofrs, dgltwogbf
    derived field has 2 non negative outcomes (1 - Yes, 2 - No)
    """
    # Create a list of the taking drugs with friends fields to check
    input_columns = [
        "dgltwofro",
        "dgltwofrb",
        "dgltwofrs",
        "dgltwogbf"]

    df["ddgltwofre"] = -1

    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "ddgltwofre"] = -9
    df.loc[df[input_columns].eq(1).any(axis=1), "ddgltwofre"] = 1
    df.loc[df[input_columns].eq(0).all(axis=1), "ddgltwofre"] = 0
    df.loc[df["dgltown"] == 2, "ddgltwofre"] = 0

    return df


def ddgwho(df):
    """
    Creates the adjusted versions of with whom pupil took drugs with most
    recently
    questions: dgltwogbf, dgltwofrs, dgltwofro, dgltwofrb, dgltwopar, dgltwooth,
    and dgltwoels.
    If dgltown (took drugs alone) is 2, then all of the with whom pupils took
    drugs with questions are adjusted to 0 (No).
    derived fields have 2 non negative outcomes (1 - Yes, 0 - No)
    """

    # Define the list of fields that are checked for this derivation
    input_columns = ["dgltwogbf", "dgltwofrs", "dgltwofro", "dgltwofrb",
                     "dgltwopar", "dgltwooth", "dgltwoels"]

    df["ddgltown"] = df["dgltown"]
    df.loc[df["dgltown"] == 1, "ddgltown"] = 0
    df.loc[df["dgltown"] == 2, "ddgltown"] = 1

    for column in input_columns:
        df.loc[df["dgltown"] == 2, "d"+column] = 0
        df.loc[df["dgltown"] != 2, "d"+column] = df[column]

    return df


def ddgfamknw(df):
    """
    Creates the derivation ddgfamknw, does family know that pupil takes drugs
    from: dgtdany, dgfamfl and ddgfam,
    Derived field has 2 non negative outcomes (1 - Do know, 2 - Don't know)
    """
    df["ddgfamknw"] = df["ddgfam"]
    df.loc[df["dgtdany"] == 2, "ddgfamknw"] = -1
    df.loc[df["ddgfam"].isin([1, 2, 3, 4]), "ddgfamknw"] = 1
    df.loc[df["dgfamfl"] == 5, "ddgfamknw"] = 2

    return df


def ddglast3(df):
    """
    Creates the derivation ddglast3 from ddgmonay (used drugs in the last month)
    and ddgany (ever used any drugs)
    measures when pupils last took drugs - 3 groups (in last month, before that,
    never take drugs)

    """
    df["ddglast3"] = df["ddgany"]
    df.loc[df["ddgany"] == 1, "ddglast3"] = 2
    df.loc[df["ddgany"] == 0, "ddglast3"] = 3
    df.loc[df["ddgmonany"] == 1, "ddglast3"] = 1

    return df


def dcgevr(df):
    """
    Creates the derivation dcgevr, has the pupil ever smoked
    from: dcgstg5
    """
    df["dcgevr"] = df["dcgstg5"]
    df.loc[df["dcgstg5"].isin([1, 2, 3, 4]), "dcgevr"] = 1
    df.loc[df["dcgstg5"] == 5, "dcgevr"] = 2

    return df


def ddgevrcan(df):
    """
    Creates ddgevrcan, whether ever used cannabis, from:
    dusecan
    """
    df["ddgevrcan"] = 2

    df.loc[df["dusecan"] == -9, "ddgevrcan"] = -9
    df.loc[df["dusecan"] == -8, "ddgevrcan"] = -8
    df.loc[df["dusecan"].isin([1, 2, 3]), "ddgevrcan"] = 1

    return df


def ddgevrvs(df):
    """
    Creates ddgevrvs, whether ever used volatile substances, from:
    dusegas
    """
    df["ddgevrvs"] = 2

    df.loc[df["dusegas"] == -9, "ddgevrvs"] = -9
    df.loc[df["dusegas"] == -8, "ddgevrvs"] = -8
    df.loc[df["dusegas"].isin([1, 2, 3]), "ddgevrvs"] = 1

    return df


def ddgmonvs(df):
    """
    Creates ddgmonvs, whether used volatile substances in last month, from:
    dusegas
    """
    df["ddgmonvs"] = 2

    df.loc[df["dusegas"] == -9, "ddgmonvs"] = -9
    df.loc[df["dusegas"] == -8, "ddgmonvs"] = -8
    df.loc[df["dusegas"] == 1, "ddgmonvs"] = 1

    return df


def ddgmoncan(df):
    """
    Creates ddgmoncan, whether used cannabis in last month, from:
    dusecan
    """
    df["ddgmoncan"] = 2

    df.loc[df["dusecan"] == -9, "ddgmoncan"] = -9
    df.loc[df["dusecan"] == -8, "ddgmoncan"] = -8
    df.loc[df["dusecan"] == 1, "ddgmoncan"] = 1

    return df


def dmultievr(df):
    """
<<<<<<< HEAD
    Creates dmultievr, if pupil has ever smoked, drunk or taken drugs
=======
    Creates dmultievr if pupil has ever smoked, drunk or taken drugs
>>>>>>> master
    0: No, 1: Yes
    from: alevr, ddgany and dcgevr
    """
    input_columns = ["alevr", "ddgany", "dcgevr"]

    df["check"] = 0
    # check how many of pupil smoked, drank or took drugs were true in specified period
    for col in input_columns:
        df.loc[df[col] == 1, "check"] = df["check"] + 1

    df["dmultievr"] = 0
    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "dmultievr"] = -9
    df.loc[df["check"] > 0, "dmultievr"] = 1

    # Drop the check variable
    df.drop(["check"], axis=1, inplace=True)

    return df


def dmultirec(df):
    """
    Creates dmultirec, if pupil has smoked, drunk or taken drugs in the last
    week (smoked/drunk) or month (drugs) 0: No, 1: Yes
    from: cg7, dallast5 and ddgmonany
    """
    input_columns = ["cg7", "dallast5", "ddgmonany"]

    df["check"] = 0

    # Check how many of pupil smoked, drank or took drugs were true in specified period
    for col in input_columns:
        df.loc[df[col] == 1, "check"] = df["check"] + 1

    df["dmultirec"] = 0
    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "dmultirec"] = -9
    df.loc[df["check"] > 0, "dmultirec"] = 1

    # Drop the check variable
    df.drop(["check"], axis=1, inplace=True)

    return df


def dmultioverlap(df):
    """
    Creates dmultioverlap, has pupil smoked, drunk or taken drugs in
    the last week (smoked/drunk) or month (drugs) grouped into 8 groupings
    from: cg7, dallast5, dggmonany
    1: Smoked only, 2: Drank only, 3: Drugs only, 4: Smoked and drank,
    5: Smoked and drugs, 6: Drank and drugs, 7: All three, 8: None
    """
    smk = (df["cg7"] == 1)
    nosmk = (df["cg7"] == 2)
    drnk = (df["dallast5"] == 1)
    nodrnk = (df["dallast5"].isin([2, 3, 4, 5]))
    drg = (df["ddgmonany"] == 1)
    nodrg = (df["ddgmonany"] == 0)

    df["dmultioverlap"] = -9

    df.loc[smk & nodrnk & nodrg, "dmultioverlap"] = 1
    df.loc[drnk & nosmk & nodrg, "dmultioverlap"] = 2
    df.loc[drg & nosmk & nodrnk, "dmultioverlap"] = 3
    df.loc[smk & drnk & nodrg, "dmultioverlap"] = 4
    df.loc[smk & drg & nodrnk, "dmultioverlap"] = 5
    df.loc[drnk & drg & nosmk, "dmultioverlap"] = 6
    df.loc[drnk & drg & smk, "dmultioverlap"] = 7
    df.loc[nodrnk & nodrg & nosmk, "dmultioverlap"] = 8

    return df


def dmulticount(df):
    """
    Creates dmulticount, has pupil smoked, drunk or taken drugs in
    the last week (smoked/drunk) or month (drugs) grouped into 4 groupings
    from: dmultioverlap
    0: None of these behaviours, 1: One of these behaviours, 2: Two of these
    behaviours, 3: All of these behaviours
    """
    df["dmulticount"] = df["dmultioverlap"]

    df.loc[df["dmultioverlap"] == 8, "dmulticount"] = 0
    df.loc[df["dmultioverlap"].isin([1, 2, 3]), "dmulticount"] = 1
    df.loc[df["dmultioverlap"].isin([4, 5, 6]), "dmulticount"] = 2
    df.loc[df["dmultioverlap"] == 7, "dmulticount"] = 3

    return df


def dlifhap(df):
    """
    Creates dlifhap, categorising 'how happy did you feel yesterday' response:
    4 groups - low, medium, high and very high
    from: lifehap
    """
    df["dlifhap"] = df["lifehap"]

    df.loc[df["lifehap"].isin([0, 1, 2, 3, 4]), "dlifhap"] = 1
    df.loc[df["lifehap"].isin([5, 6]), "dlifhap"] = 2
    df.loc[df["lifehap"].isin([7, 8]), "dlifhap"] = 3
    df.loc[df["lifehap"].isin([9, 10]), "dlifhap"] = 4

    return df


def dlifsat(df):
    """
    Creates dlifsat, categorising 'how satisfied are you with life nowadays' response:
    4 groups - low, medium, high and very high
    from: lifesat
    """
    df["dlifsat"] = df["lifesat"]

    df.loc[df["lifesat"].isin([0, 1, 2, 3, 4]), "dlifsat"] = 1
    df.loc[df["lifesat"].isin([5, 6]), "dlifsat"] = 2
    df.loc[df["lifesat"].isin([7, 8]), "dlifsat"] = 3
    df.loc[df["lifesat"].isin([9, 10]), "dlifsat"] = 4

    return df


def dlifwor(df):
    """
    Creates dlifwor, categorising 'To what extent do pupils feel the things
    they do in life are worthwhile' response:
    4 groups - low, medium, high and very high
    from: lifewor
    """
    df["dlifwor"] = df["lifewor"]

    df.loc[df["lifewor"].isin([0, 1, 2, 3, 4]), "dlifwor"] = 1
    df.loc[df["lifewor"].isin([5, 6]), "dlifwor"] = 2
    df.loc[df["lifewor"].isin([7, 8]), "dlifwor"] = 3
    df.loc[df["lifewor"].isin([9, 10]), "dlifwor"] = 4

    return df


def dlifanx(df):
    """
    Creates dlifanx, categorising 'How anxious felt yesterday' response:
    4 groups - low, medium, high and very high
    from: lifeanx
    """
    df["dlifanx"] = df["lifeanx"]

    df.loc[df["lifeanx"].isin([0, 1]), "dlifanx"] = 1
    df.loc[df["lifeanx"].isin([2, 3]), "dlifanx"] = 2
    df.loc[df["lifeanx"].isin([4, 5]), "dlifanx"] = 3
    df.loc[df["lifeanx"].isin([6, 7, 8, 9, 10]), "dlifanx"] = 4

    return df


def dliflow(df):
    """
    Creates dliflow, how many of the wellbeing questions had a 'low wellbeing' response
    from: dlifsat, dlifhap, dlifwor and dlifanx
    """
    # Create an adjusted dlifanx variable where the high anxiety = 1
    df["dlifanx_adj"] = df["dlifanx"]
    df.loc[df["dlifanx"] == 1, "dlifanx_adj"] = 4
    df.loc[df["dlifanx"] == 4, "dlifanx_adj"] = 1

    input_columns = ["dlifsat", "dlifhap", "dlifwor", "dlifanx_adj"]

    df["check"] = 0

    # Check how many of the input questions have a value of 1
    for col in input_columns:
        df.loc[df[col] == 1, "check"] = df["check"] + 1

    df["dliflow"] = 0
    df.loc[df["check"] > 0, "dliflow"] = df["check"]
    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "dliflow"] = -9

    # Drop the check and temp dlifanx variables
    df.drop(["check", "dlifanx_adj"], axis=1, inplace=True)

    return df


def dfamsmok(df):
    """
    Creates the derivation dfamsmok from cgwhosmo
    measures number of people pupil lives with who smoke
    4 groups (none, one, two, three or more)

    """

    df.loc[df["cgwhosmo"] < 3, "dfamsmok"] = df["cgwhosmo"]
    df.loc[df["cgwhosmo"] > 2, "dfamsmok"] = 3

    return df


def dmet7dysg(df):
    """
    Creates the derivation dmet7dysg from met7dys
    measures how often pupil met with 2 or more people
    who they don't live with in the last 7 days
    4 groups (not at all, on one or two days, three or four,
    five or more)

    """
    df["dmet7dysg"] = df["met7dys"]

    df.loc[df["dmet7dysg"].isin([2, 3]), "dmet7dysg"] = 2
    df.loc[df["dmet7dysg"].isin([4, 5]), "dmet7dysg"] = 3
    df.loc[df["dmet7dysg"] >= 6, "dmet7dysg"] = 4

    return df


def dmultievroverlap(df):
    """
    Creates dmultievroverlap, has pupil ever smoked, drunk or taken drugs
    grouped into 8 groupings
    from: dcgevr, alevr, ddgany
    1: Ever smoked only, 2: Ever drank only, 3: Ever drugs only, 4: Ever smoked
    and drank, 5: Ever smoked and drugs, 6: Ever drank and drugs, 7: All three,
    8: None
    """
    evrsmk = (df["dcgevr"] == 1)
    nosmk = (df["dcgevr"] == 2)
    evrdrnk = (df["alevr"] == 1)
    nodrnk = (df["alevr"] == 2)
    evrdrg = (df["ddgany"] == 1)
    nodrg = (df["ddgany"] == 0)

    df["dmultievroverlap"] = -9

    df.loc[evrsmk & nodrnk & nodrg, "dmultievroverlap"] = 1
    df.loc[evrdrnk & nosmk & nodrg, "dmultievroverlap"] = 2
    df.loc[evrdrg & nosmk & nodrnk, "dmultievroverlap"] = 3
    df.loc[evrsmk & evrdrnk & nodrg, "dmultievroverlap"] = 4
    df.loc[evrsmk & evrdrg & nodrnk, "dmultievroverlap"] = 5
    df.loc[evrdrnk & evrdrg & nosmk, "dmultievroverlap"] = 6
    df.loc[evrdrnk & evrdrg & evrsmk, "dmultievroverlap"] = 7
    df.loc[nodrnk & nodrg & nosmk, "dmultievroverlap"] = 8

    return df


def dmultievrcount(df):
    """
    Creates dmultievrcount, has pupil ever smoked, drunk or taken drugs
    grouped into 4 groupings
    from: dmultievroverlap
    0: None of these behaviours, 1: One of these behaviours, 2: Two of these
    behaviours, 3: All of these behaviours
    """
    df["dmultievrcount"] = df["dmultievroverlap"]

    df.loc[df["dmultievroverlap"] == 8, "dmultievrcount"] = 0
    df.loc[df["dmultievroverlap"].isin([1, 2, 3]), "dmultievrcount"] = 1
    df.loc[df["dmultievroverlap"].isin([4, 5, 6]), "dmultievrcount"] = 2
    df.loc[df["dmultievroverlap"] == 7, "dmultievrcount"] = 3

    return df


def ddgmultirec(df):
    """
    Creates ddgmultirec, if pupil has either taken any drugs, sniffed volatile
    substances, taken cannabis or taken Class A drugs; in the last month
    0: No, 1: Yes
    from: ddgmonany, ddgmonvs, ddgmoncan and ddgmoncla
    """
    input_columns = ["ddgmonany", "ddgmonvs", "ddgmoncan", "ddgmoncla"]

    df["check"] = 0

    # Check how many pupils took any drugs, sniffed volatile
    # substances, took cannabis or took Class A drugs; in the last month
    for col in input_columns:
        df.loc[df[col] == 1, "check"] = df["check"] + 1

    df["ddgmultirec"] = 0
    df.loc[df[input_columns].isin([-8, -9]).any(axis=1), "ddgmultirec"] = -9
    df.loc[df["check"] > 0, "ddgmultirec"] = 1

    # Drop the check variable
    df.drop(["check"], axis=1, inplace=True)

    return df
