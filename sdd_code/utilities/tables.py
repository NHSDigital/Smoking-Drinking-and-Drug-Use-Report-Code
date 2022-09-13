from sdd_code.utilities.processing import create_breakdown_single
from sdd_code.utilities.processing import create_breakdown_single_combine
from sdd_code.utilities.processing import create_breakdown_multiple_discrete
from sdd_code.utilities.processing import create_breakdown_multiple_cont
from sdd_code.utilities.processing import create_breakdown_statistics


"""
This module contains all the user defined inputs for each data table

Parameters:
----------
    df: pandas.DataFrame
        Record-level data
    breakdowns: list[str]
        Pupil breakdowns for which data will be produced (can be empty, one or more)
        Where no breakdowns required should be empty list i.e. []
    question: str
        Single variable name that defines the question in the survey
        (e.g. dallast5, alevr)
        OR for multi-response questions, the name of the new user defined
        variable that will contain the individual response questions defined
        in the 'responses' parameter - see below.
    questions: list[str]
        One or more variable names that defines the question(s) in the survey
        (e.g. dallast5, alevr)
        Used when compiling the statistics outputs that anlayse multiple questions
    filter_condition: str
        this is an non-standard, optional dataframe filter needed for some tables.
        Default is None.
        It may consist of one or more filters of dataframe variables.
    subgroup: dictionary
        Optional input where a grouped response is reported, requiring a new
        response subgroup.
        Input requires the response code(s) that will be assigned to the new group(s),
        and the response codes that will be grouped and . e.g. {10: [1, 2, 3]}
        Default is None
    base: str
        This is the variable that needs to be used for the pupil base.
        (needed where the base question is not the same as the analysis
         question).
    bases: list[str]
        For multi-response questions where there can be multiple different bases.
        If greater than 1 base then length of bases should = length of responses.
        If the bases directly align with the responses then bases = responses
    responses: list[str]
        Multi response tables only
        List of variables that represent all the response options to the question.
        In these cases a new single varibale will be created that holds
        these multiple responses (named as per the question parameter - see above)

Returns:
-------
    Each function returns a dataframe with the Excel ready output for the table.

"""
# Drinking prevalence tables begin here


def create_breakdown_sex_age1115_region_ethnicgp5_alevr(df):
    breakdowns = ["sex", "age1115", "region", "ethnicgp5"]
    question = "alevr"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_region_ethnicgp5_dallast5(df):
    breakdowns = ["sex", "age1115", "region", "ethnicgp5"]
    question = "dallast5"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1315_daysdrank(df):
    breakdowns = ["sex", "age1315"]
    responses = ["al7dmon", "al7dtue", "al7dwed", "al7dthu",
                 "al7dfri", "al7dsat", "al7dsun"]
    question = "daysdrank"
    bases = ["al7day"]
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1315_nal7utg7(df):
    breakdowns = ["sex", "age1315"]
    question = "nal7utg7"
    filter_condition = "dallast5 == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_dalfrq7(df):
    breakdowns = ["sex", "age1115"]
    question = "dalfrq7"
    filter_condition = None
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_daldrunk(df):
    breakdowns = ['sex', 'age1115']
    question = 'daldrunk'
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_stats_sex_age1315_nal7(df):

    breakdowns = ["sex", "age1315"]
    questions = ["nal7ut", "nal7br", "nal7pp", "nal7sd", "nal7sp",
                 "nal7winsh"]
    base = "nal7ut"
    filter_condition = "dallast5 == 1"

    return create_breakdown_statistics(df, breakdowns, questions, base,
                                       filter_condition)


def create_breakdown_stats_sex_age1315_al7(df):

    breakdowns = ["sex", "age1315"]
    questions = ["al7day"]
    base = "al7day"
    filter_condition = None

    return create_breakdown_statistics(df, breakdowns, questions, base,
                                       filter_condition)


def create_breakdown_sex_dagedrank(df):
    breakdowns = ["sex"]
    question = "dagedrank"
    filter_condition = "(alevr == 1)  & (age1115 == 15)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_dalagedru(df):
    breakdowns = ["sex"]
    question = "dalagedru"
    filter_condition = "(age1115 == 15) & (alevrdnk == 1)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question,
                                   filter_condition, subgroup)


def create_breakdown_sex_age1115_dal4dru5(df):
    breakdowns = ["sex", "age1115"]
    question = "dal4dru5"
    filter_condition = None
    subgroup = {10: [2, 3, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_typedrank(df):
    breakdowns = ["sex"]
    responses = ["nal7br", "nal7sd", "nal7pp", "nal7sp",
                 "nal7winsh"]
    question = "typedrank"
    base = "nal7ut"
    filter_condition = "dallast5 == 1"

    return create_breakdown_multiple_cont(df, breakdowns, responses,
                                          question, base, filter_condition)


def create_breakdown_sex_age1315_al7day(df):
    breakdowns = ["sex", "age1315"]
    question = "al7day"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1315_dal7(df):

    breakdowns = ["sex", "age1315"]
    responses = ["dal7beer", "dal7shan", "dal7winsh", "dal7spir", "dal7pops",
                 "dal7any"]
    question = "typedrank"
    bases = responses
    filter_condition = "dallast5 == 1"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1315_dalunitsday(df):
    breakdowns = ["sex", "age1315"]
    question = "dalunitsday"
    filter_condition = "dallast5 == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


# Pupils who drink tables begin here

def create_breakdown_sex_age1315_dal4dru5(df):
    breakdowns = ["sex", "age1315"]
    question = "dal4dru5"
    filter_condition = "dal4dru5 != 5"
    subgroup = {7: [2, 3, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_alcohol_howobtain(df):

    breakdowns = ["sex", "age1215", "nal7utg4"]
    responses = ["altryels", "dalshop4", "dalpub4", "algivpar", "algivfre",
                 "algivrel", "algivsib", "algivoth", "altakhom", "altakfre",
                 "alstlhom", "alstlfre", "alstloth", "dalgot4"]
    question = "howobtain"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1215_nal7ut_howobtain(df):

    breakdowns = ["sex", "age1215", "nal7utg4"]
    responses = ["altryels", "dalshop4", "dalpub4", "algivpar", "algivfre",
                 "algivrel", "algivsib", "algivoth", "altakhom", "altakfre",
                 "alstlhom", "alstlfre", "alstloth"]
    question = "howobtain"
    bases = responses
    filter_condition = "dalgot4 == 1"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1215_nal7ut_wherebuy(df):

    breakdowns = ["sex", "age1215", "nal7utg4"]
    responses = ["albuyels", "albuyfre", "albuygar", "albuyoff", "albuypub",
                 "albuyshp", "albuystr", "albuyclu", "dalbuyper", "dalbuyret",
                 "albuynev"]
    question = "wherebuy"
    bases = responses
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1215_nal7ut_wheredrink(df):

    breakdowns = ["sex", "age1215", "nal7utg4"]
    responses = ["alushom", "alusohm", "dalushmo", "alusclu", "alusfre",
                 "aluspub", "alusstr", "alusels"]
    question = "wheredrink"
    bases = responses
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1315_al4wdedr(df):
    breakdowns = ["sex", "age1315"]
    question = "al4wdedr"
    filter_condition = "(al4wdru == 1) & (al4wfrq > -1)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_dal4dru5_drunkadverse(df):

    breakdowns = ["sex", "dal4dru5"]
    responses = ["al4warg", "al4wdam", "al4wfig", "al4whos", "al4will",
                 "al4wlst", "al4wpol", "al4wvom"]
    question = "drunkadverse"
    bases = responses
    filter_condition = "dal4dru5 in [2, 3]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1215_nal7ut_whodrink(df):

    breakdowns = ["sex", "age1215", "nal7utg4"]
    responses = ["daluspar", "dalussib", "dalusfreb", "dalusfreo", "dalusfres",
                 "dalusgb", "dalusoth", "dalusfre", "alownoth"]
    question = "whodrink"
    bases = responses
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dallast3_dalwhodr_dalfamknw(df):

    breakdowns = ["dallast3", "dalwhodr"]
    question = "dalfamknw"
    # Note: dalfamknw should not have a value 8, this filter is only needed so 2018 processing is correct
    filter_condition = "(dalfamknw != 8) & (dalfrq7 in [1, 2, 3, 4, 5, 6])"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1315_alcohol_buywherebuy(df):

    breakdowns = ["age1315"]
    responses = ["albuyfre", "albuyels", "albuystr", "albuyoff", "albuyshp",
                 "albuygar", "albuypub", "albuyclu", "dalbuyper",
                 "dalbuyret"]
    question = "buywherebuy"
    bases = responses
    filter_condition = "albuynev == 0"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


# Drinking context tables begin here

def create_breakdown_sex_age1115_dallast_nal7ut_dalwhodr_dalfam(df):
    breakdowns = ["sex", "age1115", "dallast3", "nal7utg4", "dalwhodr"]
    question = "dalfam"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dalfamknw_dalfam(df):
    breakdowns = ["dalfamknw"]
    question = "dalfam"
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dalfam_dal4dru5(df):
    breakdowns = ["dalfam"]
    question = "dal4dru5"
    filter_condition = None
    subgroup = {7: [2, 3, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_drinking_consequences(df):

    breakdowns = ["sex", "age1115"]
    responses = ["alcncr", "alhrm"]
    question = "consequences"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_dallast3_beliefs(df):

    breakdowns = ["sex", "age1115", "dallast3"]
    responses = ["alwhycoo", "alwhysoc", "alwhyrsh", "alwhypre", "alwhyfgt",
                 "alwhyliv", "alwhycon", "alwhybor", "alwhyrel"]
    question = "beliefs"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_alestim(df):
    breakdowns = ["sex", "age1115"]
    question = "alestim"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dallast3_alestim(df):
    breakdowns = ["dallast3"]
    question = "alestim"
    filter_condition = "age1115 == 15"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_dallast3_source(df):

    breakdowns = ["sex", "age1115", "dallast3"]
    responses = ["alinpar", "alintea", "alinrel", "alinpol", "alinfre",
                 "alinad", "alingp", "alinsib", "alinyou", "alinyou", "alintv",
                 "alinint", "alinnews", "alinsoc", "alinrad", "alinhelp",
                 "alinfra"]
    question = "source"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dalwhodr_dalfam_dfasbands_imdquin_dallast3(df):

    breakdowns = ["dalwhodr", "dalfam", "dfasbands", "imdquin"]
    question = "dallast3"
    filter_condition = "dallast3 in [1, 2, 3]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_dallast_attitudes(df):

    breakdowns = ["sex", "age1115", "dallast3"]
    responses = ["okal1", "okalw", "okdk1", "okdkw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dal4dru_attitudes(df):

    breakdowns = ["dal4dru5"]
    responses = ["okal1", "okalw", "okdk1", "okdkw"]
    question = "attitudes"
    bases = responses
    filter_condition = "(dallast5 in [1, 2]) & (al4wdru >= 0)"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)

# School lesson tables begin here


def create_breakdown_sex_syear_puplessons(df):

    breakdowns = ["sex", "syear"]
    responses = ["lssmk", "lsalc", "lsdrg"]
    question = "puplessons"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_syear_info(df):

    breakdowns = ["sex", "syear"]
    responses = ["einfsmk", "einfalc", "einfdrg"]
    question = "info"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_schlessons(df):

    breakdowns = []
    responses = ["lessmok", "lesalc", "lesdrg"]
    question = "schoollessons"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_contributes(df):

    breakdowns = []
    responses = ["q7teach", "q7nurse", "q7staff", "q7locdaa", "q7police",
                 "q7youth", "q7else"]
    question = "contributes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sources(df):

    breakdowns = []
    responses = ["q8adepis", "q8def", "q8else", "q8frank", "q8oteach",
                 "q8pshe", "q8search", "q8tes", "q8dfe"]
    question = "sources"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_otheradvice(df):
    breakdowns = []
    responses = ["q10assem", "q10advic", "q10leaf", "q10post", "q10speak",
                 "q10else", "edadvice"]
    question = "otheradvice"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_lessonssmoking(df):
    breakdowns = None
    questions = ["y7smok", "y8smok", "y9smok", "y10smok", "y11smok"]
    filter_condition = "{question} != 6"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_lessonsdrinking(df):
    breakdowns = None
    questions = ["y7alc", "y8alc", "y9alc", "y10alc", "y11alc"]
    filter_condition = "{question} != 6"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_lessonsdrugs(df):
    breakdowns = None
    questions = ["y7drg", "y8drg", "y9drg", "y10drg", "y11drg"]
    filter_condition = "{question} != 6"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


# Smoking prevalence tables begin here


def create_breakdown_sex_age_region_ethnicgp5_dcgstg5(df):

    breakdowns = ["sex", "age1115", "region", "ethnicgp5"]
    question = "dcgstg5"
    filter_condition = None
    subgroup = {6: [1, 2], 7: [1, 2, 3, 4]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age_cg7(df):

    breakdowns = ["sex", "age1115"]
    question = "cg7"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dcgstg5_dcg7totg(df):

    breakdowns = ["dcgstg5"]
    question = "dcg7totg"
    filter_condition = "(dcgstg5 in [1, 2]) & (dcg7tot >= 0)"
    subgroup = {8: [5, 6, 7]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_stats_sex_dcgstg3_dcg7tot(df):

    breakdowns = ["sex", "dcgstg3"]
    questions = ["dcg7tot"]
    base = "dcg7tot"
    filter_condition = "dcgstg3 in [1, 2]"

    return create_breakdown_statistics(df, breakdowns, questions, base,
                                       filter_condition)


def create_breakdown_stats_sex_dcgstg3_cg7(df):

    breakdowns = ["sex", "dcgstg3"]
    questions = ["dcg7tot", "cg7mon", "cg7tue", "cg7wed", "cg7thu",
                 "cg7fri", "cg7sat", "cg7sun"]
    base = "dcg7tot"
    filter_condition = "((dcgstg3 in [1, 2]) | (dcgstg3 < 0)) & (cg7 == 1)"

    return create_breakdown_statistics(df, breakdowns, questions, base,
                                       filter_condition)


def create_breakdown_dcgstg3_dcg7day(df):
    breakdowns = ["dcgstg3"]
    responses = ["dcg7mon", "dcg7tue", "dcg7wed", "dcg7thu", "dcg7fri",
                 "dcg7sat", "dcg7sun", "dcg7any"]
    question = "dcg7day"
    bases = responses
    filter_condition = "dcgstg3 in [1, 2]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)

# Pupils who smoke tables begin here


def create_breakdown_shops_wherebuy(df):

    breakdowns = []
    responses = ["cggetnew", "cggetgar", "cggetsup", "cggetsho", "cggetgiv"]
    question = "wherebuy"
    bases = responses
    filter_condition = "dcgstg3 == 1"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_age1315_cgdiff(df):

    breakdowns = ["age1315"]
    question = "cgdiff"
    filter_condition = "(dcgstg5 in [1, 2]) & (cgdiff > 0)"
    subgroup = {6: [1, 2]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_age1115_cgshop(df):

    breakdowns = ["age1115"]
    question = "cgshop"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1115_cgshopp(df):

    breakdowns = ["sex", "age1115"]
    question = "cgshopp"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dcgstg3_cgshopp(df):

    breakdowns = ["dcgstg3"]
    question = "cgshopp"
    filter_condition = "dcgstg3 in [1, 2]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_age1315_cgref(df):

    breakdowns = ["age1315"]
    question = "cgref"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_age1315_cglast(df):

    breakdowns = ["age1315"]
    question = "cglast"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dcgstg3_sex_age1315_cgsourcecurr(df):
    breakdowns = ["dcgstg3", "sex", "age1315"]
    responses = ["dcggetp", "dcggets", "dcgbuyp", "cggetelg",
                 "cggetels", "cggetfre", "cggetgar", "cggetgiv", "cggetint",
                 "cggetmac", "cggetmar", "cggetnew", "cggetoth", "cggetpar",
                 "cggetsho", "cggetsib", "cggetsup", "cggettak"]
    question = "sourcecurrent"
    bases = ["cggetgiv"]
    filter_condition = "dcgstg3 in [1, 2]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_cgsourcereg(df):
    breakdowns = []
    responses = ["dcggets", "cggetelg", "cggetels", "cggetfre", "cggetgar",
                 "cggetgiv", "cggetint", "cggetmac", "cggetmar", "cggetnew",
                 "cggetoth", "cggetpar", "cggetsho", "cggetsib", "cggetsup",
                 "cggettak"]
    question = "sourceregular"
    bases = ["cggetgiv"]
    filter_condition = "dcgstg3 == 1"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_cgbuyf(df):

    breakdowns = []
    question = "cgbuyf"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_cgstopdif(df):

    breakdowns = None
    questions = ["cgstopw", "cgstop"]
    filter_condition = "dcgstg3 == 1"
    subgroup = {10: [1, 2], 11: [3, 4]}

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_cgstoplik(df):
    breakdowns = None
    questions = ["cglikstp", "cgevrstp"]
    filter_condition = "dcgstg3 == 1"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_sex_cglong(df):

    breakdowns = ["sex"]
    question = "cglong"
    filter_condition = "dcgstg3 == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dcglongg_dcg7totg2_depend(df):
    breakdowns = ["dcglongg", "dcg7totg2"]
    questions = ["dcgstopwg", "dcgstopg", "cglikstp", "cgevrstp"]
    filter_condition = "dcgstg3 == 1"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_sex_dcgtrystp(df):

    breakdowns = ["sex"]
    question = "dcgtrystp"
    filter_condition = "dcgstg3 == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dcgstg3_dcgelbuy(df):

    breakdowns = ["dcgstg3"]
    question = "dcgelbuy"
    filter_condition = "(dcgstg3 in [1, 2]) & (dcgelbuy in [1, 2])"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_age1215_dcgoft_method(df):
    breakdowns = ["age1215", "dcgoft"]
    responses = ["dcggupno", "dcggupfa", "dcggupni", "dcggupad", "dcggupgp",
                 "dcggupst", "dcgguphe", "dcggupecg", "dcggupany"]
    question = "method"
    bases = responses
    filter_condition = "dcgstg5 in [1, 2, 3, 4]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dcgstg3_dcgwhosmo_dcgsec2(df):

    breakdowns = ["dcgstg3", "dcgwhosmo"]
    question = "dcgsec2"
    filter_condition = "dcgstg3 in [1, 2]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1315_dcgstg3_dcgelbuy(df):

    breakdowns = ["sex", "age1315", "dcgstg3"]
    question = "dcgelbuy"
    filter_condition = "dcgelbuy in [1, 2]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


# Smoking context tables begin here


def create_breakdown_dcgwhosmo_dfasbands_imdquin_dcgstg3(df):

    breakdowns = ["dcgwhosmo", "dfasbands", "imdquin"]
    question = "dcgstg3"
    filter_condition = None
    subgroup = {6: [1, 2]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_age1115_dcgstg3_frfamsmoke(df):
    breakdowns = ["age1115", "dcgstg3"]
    responses = ["dcgppfr", "dcgppfam", "cgppgb", "cgppfrsa", "cgppfrol",
                 "cgppfryo", "cgpppar", "cgppsib", "cgppoth", "cgppno"]
    question = "frfamsmoke"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_age1115_dcgstg2_frfamsmoke(df):
    breakdowns = ["age1115", "dcgstg2"]
    responses = ["dcgppfr", "dcgppfam", "cgppgb", "cgppfrsa", "cgppfrol",
                 "cgppfryo", "cgpppar", "cgppsib", "cgppoth", "cgppno"]
    question = "frfamsmoke"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1315_dcgstg3_dcgwhosmo_dcgfam(df):

    breakdowns = ["sex", "age1115", "dcgstg3", "dcgwhosmo"]
    question = "dcgfam"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1315_dcgstg2_dcgwhosmo_dcgfam(df):

    breakdowns = ["sex", "age1115", "dcgstg2", "dcgwhosmo"]
    question = "dcgfam"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dcgsec2_dcgfam(df):

    breakdowns = ["dcgsec2"]
    question = "dcgfam"
    filter_condition = "dcgstg3 in [1, 2]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_age1115_dcgstg3_cgsmkexp(df):
    breakdowns = ["age1115", "dcgstg3"]
    questions = ["cgshin", "cgshcar", "dcgshboth"]
    filter_condition = "{question} != 6"
    subgroup = {9: [1, 2, 3, 4]}

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_age1115_dcgstg2_cgsmkexp(df):
    breakdowns = ["age1115", "dcgstg2"]
    questions = ["cgshin", "cgshcar", "dcgshboth"]
    filter_condition = "{question} != 6"
    subgroup = {9: [1, 2, 3, 4]}

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_sex_age1115_dcgstg3_attitudes(df):
    breakdowns = ["sex", "age1115", "dcgstg3"]
    responses = ["okcg1", "okcgw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_dcgstg2_attitudes(df):
    breakdowns = ["sex", "age1115", "dcgstg2"]
    responses = ["okcg1", "okcgw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_dcgstg3_beliefs(df):
    breakdowns = ["sex", "age1115", "dcgstg3"]
    responses = ["cgwhycoo", "cgwhypre", "cgwhyadd", "cgwhyexc", "cgwhystr",
                 "cgwhyliv", "cgwhygdf", "cgwhyrel", "cgwhyslm"]
    question = "beliefs"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_dcgstg2_beliefs(df):
    breakdowns = ["sex", "age1115", "dcgstg2"]
    responses = ["cgwhycoo", "cgwhypre", "cgwhyadd", "cgwhyexc", "cgwhystr",
                 "cgwhyliv", "cgwhygdf", "cgwhyrel", "cgwhyslm"]
    question = "beliefs"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1315_cgppfrsa_cgestim(df):

    breakdowns = ["sex", "age1115", "cgppfrsa"]
    question = "cgestim"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dcgstg3_cgestim(df):

    breakdowns = ["dcgstg3"]
    question = "cgestim"
    filter_condition = "age1115 == 15"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dcgstg2_cgestim(df):

    breakdowns = ["dcgstg2"]
    question = "cgestim"
    filter_condition = "age1115 == 15"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1115_dcgstg3_sources(df):
    breakdowns = ["sex", "age1115", "dcgstg3"]
    responses = ["cginpar", "cgintea", "cginrel", "cginpol", "cginfre",
                 "cginad", "cgingp", "cginsib", "cginyou", "cgintv", "cginint",
                 "cginnews", "cginsoc", "cginrad", "cginhelp", "cginfra"]
    question = "sources"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_dcgstg2_sources(df):
    breakdowns = ["sex", "age1115", "dcgstg2"]
    responses = ["cginpar", "cgintea", "cginrel", "cginpol", "cginfre",
                 "cginad", "cgingp", "cginsib", "cginyou", "cgintv", "cginint",
                 "cginnews", "cginsoc", "cginrad", "cginhelp", "cginfra"]
    question = "sources"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_age1115_wheredisplay(df):
    breakdowns = ["age1115"]
    responses = ["cgpdsup", "cgpdnew", "cgpdgar", "cgpdoth", "cgpdnone"]
    question = "wheredisplay"
    bases = ["cgpdsup"]
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


# E cigarette use tables begin here


def create_breakdown_sex_age1315_cgelechd(df):

    breakdowns = ["sex", "age1115"]
    question = "cgelechd"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1315_ecig_sources(df):
    breakdowns = ["sex", "age1315"]
    responses = ["dcgelgtoth", "dcgelgtgiv", "dcgelgtshp", "dcgelgtppl", "cgelgtgiv",
                 "cgelgtsib", "cgelgtpar", "cgelgtelg", "cgelgtnew", "cgelgtsho",
                 "cgelgtsup", "cgelgtpha", "cgelgtgar", "cgelgtgot", "cgelgtfre",
                 "cgelgtels", "cgelgtmar", "cgelgtint", "cgelgttak"]
    question = "sources"
    bases = responses
    filter_condition = "dcgelec == 6"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_dcgstg5_dcgelec(df):

    breakdowns = ["sex", "age1115", "dcgstg5"]
    question = "dcgelec"
    filter_condition = None
    subgroup = {7: [1, 2], 8: [5, 6], 9: [3, 4, 5, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1115_ecig_attitudes(df):
    breakdowns = ["sex", "age1115"]
    responses = ["okec1", "okecw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_cgelshopp(df):

    breakdowns = ["sex", "age1115"]
    question = "cgelshopp"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dcgelec_cgelshopp(df):

    breakdowns = ["dcgelec"]
    question = "cgelshopp"
    filter_condition = "dcgelec in [5, 6]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1215_cgelacbshp(df):

    breakdowns = ["sex", "age1215"]
    question = "cgelacbsp"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dcgelec_cgelacbshp(df):

    breakdowns = ["dcgelec"]
    question = "cgelacbsp"
    filter_condition = "dcgelec in [5, 6]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_cgellong(df):

    breakdowns = ["sex"]
    question = "cgellong"
    filter_condition = "dcgelec == 6"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


# Drug prevalence tables begin here


def create_breakdown_sex_age1115_region_ethnicgp5_druguse(df):
    breakdowns = ["sex", "age1115", "region", "ethnicgp5"]
    responses = ["ddgany", "ddgyrany", "ddgmonany", "ddganynotvs",
                 "ddgyranynotvs", "ddgmonanynotvs"]
    question = "druguse"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1315_ddgyrty(df):

    breakdowns = ["sex", "age1315"]
    question = "ddgyrty"
    filter_condition = "ddgyrty != 7"
    subgroup = {10: [1, 2, 3, 4], 11: [5, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1115_ddgoc(df):

    breakdowns = ["sex", "age1115"]
    question = "ddgoc"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1115_drugusetype(df):
    breakdowns = ["sex", "age1115"]
    questions = ["dusecan", "dusecok", "dusecrk", "duseecs", "duseamp",
                 "dusepop", "dusemph", "duselsd", "dusemsh", "duseket",
                 "dusenox", "duseleg", "duseher", "dusemth", "dusegas",
                 "dusetrn", "duseoth", "ddgany", "ddganynotps", "ddganynotvs",
                 "ddgyrany", "ddgyranynotvs", "ddgyranynotps", "ddgmonany",
                 "ddgmonanynotvs", "ddgmonanynotps", "ddganyresponse",
                 "ddgevrcla", "ddgmoncla", "ddgyrcla", "ddgevropi", "ddgmonopi",
                 "ddgyropi", "ddgevrps", "ddgmonps", "ddgyrps", "ddgevrpsy",
                 "ddgmonpsy", "ddgyrpsy", "ddgevrstm", "ddgmonstm", "ddgyrstm"]
    filter_condition = None
    subgroup = {10: [1, 2, 3], 11: [1, 2]}

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_sex_age1315_dgocleg(df):

    breakdowns = ["sex", "age1315"]
    question = "dgocleg"
    filter_condition = "dgocleg in [1, 2, 3, 4]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_age1315_ddgyrty5_ddgoc(df):

    breakdowns = ["age1315", "ddgyrty5"]
    question = "ddgoc"
    filter_condition = "ddgoc >= 3"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1315_ddgtypleg(df):

    breakdowns = ["sex", "age1315"]
    question = "ddgtypleg"
    filter_condition = "dgocleg in [1, 2, 3, 4]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1215_ddgfq6(df):

    breakdowns = ["sex", "age1215"]
    question = "ddgfq6"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1215_ddgfq8(df):

    breakdowns = ["sex", "age1215"]
    question = "ddgfq8"
    filter_condition = None
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1315_ddgfq8_lastyr(df):

    breakdowns = ["sex", "age1315"]
    question = "ddgfq8"
    filter_condition = "ddgfq8 in [1, 2, 3, 4, 5, 6]"
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_ddgyrty5_ddgfq8_lastyr(df):

    breakdowns = ["ddgyrty5"]
    question = "ddgfq8"
    filter_condition = "(ddgfq8 in [1, 2, 3, 4, 5, 6]) & (ddgyrty5 in [1, 2, 3, 4])"
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dtruexc_ddgyrcla(df):

    breakdowns = ["dtruexc"]
    question = "ddgyrcla"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dtruexc_ddgfq6(df):

    breakdowns = ["dtruexc"]
    question = 'ddgfq6'
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1115_drugoff(df):
    breakdowns = ["sex", "age1115"]
    responses = ["ddgofcan", "ddgofcok", "ddgofcrk", "ddgofecs", "ddgofamp",
                 "ddgofpop", "ddgofmph", "ddgoflsd", "ddgofmsh", "ddgofket",
                 "ddgofnox", "ddgofleg", "ddgofher", "ddgofmth", "ddgofgas",
                 "ddgoftrn", "ddgofoth", "ddgofany", "ddgofanynotps",
                 "ddgofanyresponse", "ddgofstm", "ddgofpsy", "ddgofps", "ddgofopi"]
    question = "drugoff"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age15_anydrugofftaken(df):
    breakdowns = ["sex"]
    question = "ddgany"
    filter_condition = "(age1115 == 15) & (ddgofany == 1)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_age1115_drugaware(df):
    breakdowns = ["age1115"]
    responses = ["dghdcan", "dghdcok", "dghdcrk", "dghdecs", "dghdamp",
                 "dghdpop", "dghdmph", "dghdlsd", "dghdmsh", "dghdket",
                 "dghdnox", "dghdleg", "dghdher", "dghdmth",
                 "dghdtrn", "dghdoth", "ddghdnotaw", "ddghdnotawexps",
                 "ddghdanyresponse", "ddghdstm", "ddghdpsy", "ddghdps", "ddghdopi"]
    question = "drugaware"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_ddgageany11_ddgagexxx(df):
    breakdowns = ["ddgageany11"]
    responses = ["ddgagecan", "ddgagecok", "ddgagecrk", "ddgageecs", "ddgageamp",
                 "ddgagepop", "ddgagemph", "ddgagelsd", "ddgagemsh", "ddgageket",
                 "ddgagenox", "ddgageleg", "ddgageher", "ddgagemth", "ddgagegas",
                 "ddgagetrn", "ddgageoth"]
    question = "ddgagexxx"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_ddgageany11_ddgfirst(df):
    breakdowns = ["ddgageany11"]
    question = "ddgfirst"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age15_canofftaken(df):
    breakdowns = ["sex"]
    question = "dgtdcan"
    filter_condition = "(age1115 == 15) & (ddgofcan == 1) & (dusecan > 0)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age15_claofftaken(df):
    breakdowns = ["sex"]
    question = "ddgevrcla"
    filter_condition = "(age1115 == 15) & (ddgofcla == 1)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_ddgageany11_ddgfttyp(df):
    breakdowns = ["ddgageany11"]
    question = "ddgfttyp"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1315_ddglttyp(df):
    breakdowns = ["sex", "age1315"]
    question = "ddglttyp"
    filter_condition = "ddgoc in [4, 5, 6]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


# Pupils who take drugs tables begin here

def create_breakdown_sex_ddgageany11_ddgfttyp_dgftwh(df):
    breakdowns = ["sex", "ddgageany11", "ddgfttyp"]
    question = "dgftwh"
    filter_condition = "dgtdany == 1"
    subgroup = {20: [2, 3, 4, 5]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1315_ddglttyp_dgltwh(df):
    breakdowns = ["sex", "age1315", "ddglttyp"]
    question = "dgltwh"
    filter_condition = "ddgoc in [4, 5, 6]"
    subgroup = {20: [2, 3, 4, 5]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1315_ddglttyp_dgltwhr(df):
    breakdowns = ["sex", "age1315", "ddglttyp"]
    question = "dgltwhr"
    filter_condition = "ddgoc in [4, 5, 6]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age_ddgofany_dgget(df):
    breakdowns = ["sex", "age1115", "age1315", "ddgofany"]
    question = "dgget"
    filter_condition = None
    subgroup = {10: [1, 2], 11: [3, 4]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1315_ddglttyp_whowith(df):
    breakdowns = ["sex", "age1315", "ddglttyp"]
    responses = ["ddgltwogbf", "ddgltwofrs", "ddgltwofro", "ddgltwofrb", "ddgltwopar",
                 "ddgltwooth", "ddgltwoels", "ddgltown", "ddgltwofre"]
    question = "whowith"
    bases = responses
    filter_condition = "dgoc in [2, 3, 4]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_dgbuy(df):
    breakdowns = ["sex", "age1115"]
    questions = ["dgbuyint", "dgbuyshp"]
    filter_condition = None
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_ddgyrty5_dgbuy(df):
    breakdowns = ["ddgyrty5"]
    questions = ["dgbuyint", "dgbuyshp"]
    filter_condition = "ddgyrty5 in [1, 2, 3, 4]"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


# Drug context tables begin here

def create_breakdown_sex_ddgageany11_ddgfttyp_ddgftwy(df):
    breakdowns = ["sex", "ddgageany11", "ddgfttyp"]
    responses = ["dgftwylke", "dgftwyhig", "dgftwyfri", "dgftwynbt", "dgftwyfor",
                 "dgftwyoff", "dgftwydar", "dgftwycoo", "dgftwyoth", "dgftwynkn",
                 "dgftwynre"]
    question = "ddgftwy"
    bases = responses
    filter_condition = "dgtdany == 1"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1315_ddglttyp_ddgoc_ddgltwy(df):
    breakdowns = ["sex", "age1315", "ddglttyp", "ddgoc"]
    responses = ["dgltwycoo", "dgltwydar", "dgltwyfor", "dgltwyfri",
                 "dgltwyhig", "dgltwylke", "dgltwynbt", "dgltwynkn",
                 "dgltwynre", "dgltwyoff", "dgltwyoth"]
    question = "ddgltwy"
    bases = responses
    filter_condition = "ddgoc in [4, 5, 6]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_ddgoc4_dgestim(df):
    breakdowns = ["sex", "age1115", "ddgoc4"]
    question = "dgestim"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1115_drugattitudes(df):
    breakdowns = ["sex", "age1115"]
    responses = ["okcan1", "okvs1", "okcoc1", "okcanw", "okvsw", "okcocw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sex_age1115_ddgfam(df):
    breakdowns = ["sex", "age1115"]
    question = "ddgfam"
    filter_condition = "ddgfam in [1, 2, 3, 4]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_ddgfamknw_ddgfam(df):
    breakdowns = ["ddgfamknw"]
    question = "ddgfam"
    filter_condition = "(ddgoc in [4, 5, 6]) & (ddgfam in [1, 2, 3, 4])"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_ddgfam4_ddgoc(df):
    breakdowns = ["ddgfam4"]
    question = "ddgoc"
    filter_condition = "ddgfam4 in [1, 2, 3]"
    subgroup = {10: [1, 2]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_age1115_ddglast3_sources(df):
    breakdowns = ["sex", "age1115", "ddglast3"]
    responses = ["dginpar", "dginsib", "dginrel", "dginfre", "dgingp",
                 "dgintea", "dginad", "dginpol", "dgintv", "dginrad",
                 "dginnews", "dginint", "dginfra", "dginhelp", "dginsoc"]
    question = "sources"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dfasbands_imdquin_ddglast3(df):
    breakdowns = ["dfasbands", "imdquin"]
    question = "ddglast3"
    filter_condition = "ddglast3 in [1, 2, 3]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)

# Multiple behaviour tables begin here


def create_breakdown_age1115_behavevr(df):
    breakdowns = ["age1115"]
    responses = ["dcgevr", "alevr", "ddgany", "ddgevrcan", "ddgevrvs",
                 "ddgevrcla", "dmultievr"]
    question = "behavevr"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_age1115_behavrec(df):
    breakdowns = ["age1115"]
    responses = ["cg7", "dallast5", "ddgmonany", "ddgmonvs", "ddgmoncan",
                 "ddgmoncla", "dmultirec"]
    question = "behavrec"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_age1115_behavoverlap(df):
    breakdowns = ["age1115"]
    question = "dmultioverlap"
    filter_condition = None
    subgroup = {10: [1, 2, 3], 11: [4, 5, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_age1115_attitudes(df):
    breakdowns = ["age1115"]
    responses = ["okcg1", "okal1", "okdk1", "okcan1", "okvs1", "okcoc1", "okec1",
                 "okcgw", "okalw", "okdkw", "okcanw", "okvsw", "okcocw", "okecw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


# Wellbeing tables begin here

def create_breakdown_sex_age1115_region_dlifsat(df):
    breakdowns = ["sex", "age1115", "region"]
    question = "dlifsat"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dlifsat(df):
    breakdowns = ["cg7", "dallast5", "ddgmonany", "dmulticount"]
    question = "dlifsat"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_region_dlifwor(df):
    breakdowns = ["sex", "age1115", "region"]
    question = "dlifwor"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dlifwor(df):
    breakdowns = ["cg7", "dallast5", "ddgmonany", "dmulticount"]
    question = "dlifwor"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_region_dlifhap(df):
    breakdowns = ["sex", "age1115", "region"]
    question = "dlifhap"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dlifhap(df):
    breakdowns = ["cg7", "dallast5", "ddgmonany", "dmulticount"]
    question = "dlifhap"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_region_dlifanx(df):
    breakdowns = ["sex", "age1115", "region"]
    question = "dlifanx"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dlifanx(df):
    breakdowns = ["cg7", "dallast5", "ddgmonany", "dmulticount"]
    question = "dlifanx"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_age1115_dliflow(df):
    breakdowns = ["sex", "age1115"]
    question = "dliflow"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


# Covid impact tables begin here

def create_breakdown_sex_schlearn_dcgstg5(df):
    breakdowns = ["sex", "schlearn"]
    question = "dcgstg5"
    filter_condition = None
    subgroup = {6: [1, 2], 7: [1, 2, 3, 4]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_schlearn_dcgelec(df):
    breakdowns = ["sex", "schlearn"]
    question = "dcgelec"
    filter_condition = None
    subgroup = {7: [1, 2], 8: [5, 6], 9: [3, 4, 5, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_schlearn_dallast3(df):
    breakdowns = ["sex", "schlearn"]
    question = "dallast3"
    filter_condition = None
    subgroup = {10: [1, 2]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_dmet7dysg_cg7(df):
    breakdowns = ["sex", "dmet7dysg"]
    question = "cg7"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dmet7dysg_dcg7totg(df):
    breakdowns = ["dmet7dysg"]
    question = "dcg7totg"
    filter_condition = "dcgsmk == 1"
    subgroup = {10: [5, 6, 7]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dmet7dysg_nal7utg7(df):
    breakdowns = ["dmet7dysg"]
    question = "nal7utg7"
    filter_condition = "dallast3 == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_met4wks_schlearn_dalfrq7(df):
    breakdowns = ["sex", "met4wks", "schlearn"]
    question = "dalfrq7"
    filter_condition = None
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_met4wks_dal4dru5(df):
    breakdowns = ["sex", "met4wks"]
    question = "dal4dru5"
    filter_condition = None
    subgroup = {10: [2, 3, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_sex_met4wks_schlearn_druguse(df):
    breakdowns = ["sex", "schlearn", "met4wks"]
    questions = ["ddgmonany", "ddgyrany", "ddgany"]
    filter_condition = None
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions, filter_condition, subgroup)


def create_breakdown_sex_schlearn_ddgfq8_lastyr(df):
    breakdowns = ["sex", "schlearn"]
    question = "ddgfq8"
    filter_condition = "ddgfq8 in [1, 2, 3, 4, 5, 6]"
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_met4wks_behavrec(df):
    breakdowns = ["sex", "met4wks"]
    questions = ["cg7", "dallast5", "ddgmonany", "dmulticount"]
    filter_condition = None
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_sex_schlearn_lifebehav(df):
    breakdowns = ["sex", "schlearn"]
    questions = ["dcgevr", "alevr", "ddgany", "dmultievrcount"]
    filter_condition = None
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_sex_schlearn_met4wks_drugslastmth(df):
    breakdowns = ["sex", "schlearn", "met4wks"]
    questions = ["ddgmonany", "ddgmonvs", "ddgmoncan", "ddgmoncla", "ddgmultirec"]
    filter_condition = None
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions, filter_condition, subgroup)


def create_breakdown_met4wks_behavoverlap(df):
    breakdowns = ["met4wks"]
    question = "dmultioverlap"
    filter_condition = None
    subgroup = {10: [1, 2, 3], 11: [4, 5, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_met4wks_dlifsat(df):
    breakdowns = ["met4wks"]
    question = "dlifsat"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_met4wks_dlifwor(df):
    breakdowns = ["met4wks"]
    question = "dlifwor"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_met4wks_dlifhap(df):
    breakdowns = ["met4wks"]
    question = "dlifhap"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_met4wks_dlifanx(df):
    breakdowns = ["met4wks"]
    question = "dlifanx"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dmet7dysg_dlifsat(df):
    breakdowns = ["dmet7dysg"]
    question = "dlifsat"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dmet7dysg_dlifwor(df):
    breakdowns = ["dmet7dysg"]
    question = "dlifwor"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dmet7dysg_dlifhap(df):
    breakdowns = ["dmet7dysg"]
    question = "dlifhap"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dmet7dysg_dlifanx(df):
    breakdowns = ["dmet7dysg"]
    question = "dlifanx"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)



# Survey delivery tables begin here

def create_breakdown_sex_appointflag_dcgstg5(df):
    breakdowns = ["sex", "appointflag"]
    question = "dcgstg5"
    filter_condition = None
    subgroup = {6: [1, 2], 7: [1, 2, 3, 4]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_appointflag_cg7(df):
    breakdowns = ["sex", "appointflag"]
    question = "cg7"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_appointflag_dcg7totg(df):
    breakdowns = ["appointflag"]
    question = "dcg7totg"
    filter_condition = "dcgsmk == 1"
    subgroup = {10: [5, 6, 7]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_appointflag_dcgelec(df):
    breakdowns = ["sex", "appointflag"]
    question = "dcgelec"
    filter_condition = None
    subgroup = {7: [1, 2], 8: [5, 6], 9: [3, 4, 5, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_appointflag_dallast3(df):
    breakdowns = ["sex", "appointflag"]
    question = "dallast3"
    filter_condition = None
    subgroup = {10: [1, 2]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_appointflag_nal7utg7(df):
    breakdowns = ["appointflag"]
    question = "nal7utg7"
    filter_condition = "dallast3 == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_appointflag_dalfrq7(df):
    breakdowns = ["sex", "appointflag"]
    question = "dalfrq7"
    filter_condition = None
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_appointflag_ddgfq8_lastyr(df):

    breakdowns = ["sex", "appointflag"]
    question = "ddgfq8"
    filter_condition = "ddgfq8 in [1, 2, 3, 4, 5, 6]"
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_appointflag_ddglast3(df):
    breakdowns = ["sex", "appointflag"]
    question = "ddglast3"
    filter_condition = None
    subgroup = {4: [1, 2]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_sex_appointflag_drugslastmth(df):

    breakdowns = ["sex", "appointflag"]
    questions = ["ddgmonany", "ddgmonvs", "ddgmoncan", "ddgmoncla", "ddgmultirec"]
    filter_condition = None
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions, filter_condition, subgroup)
