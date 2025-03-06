from sdd_code.utilities.processing.processing import create_breakdown_single
from sdd_code.utilities.processing.processing import create_breakdown_single_combine
from sdd_code.utilities.processing.processing import create_breakdown_multiple_discrete
from sdd_code.utilities.processing.processing import create_breakdown_multiple_cont
from sdd_code.utilities.processing.processing import create_breakdown_statistics


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
        Used when compiling the statistics outputs that analyse multiple questions
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
        In these cases a new single variable will be created that holds
        these multiple responses (named as per the question parameter - see above)

Returns:
-------
    Each function returns a dataframe with the Excel ready output for the table.

"""
# Drinking prevalence tables begin here


def create_breakdown_dgender_age1115_region_ethnicgp5_alevr(df):
    breakdowns = ["dgender", "age1115", "region", "ethnicgp5"]
    question = "alevr"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_age1115_region_ethnicgp5_dallast5(df):
    breakdowns = ["dgender", "age1115", "region", "ethnicgp5"]
    question = "dallast5"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_age1315_daysdrank(df):
    breakdowns = ["dgender", "age1315"]
    responses = ["al7dmon", "al7dtue", "al7dwed", "al7dthu",
                 "al7dfri", "al7dsat", "al7dsun"]
    question = "daysdrank"
    bases = ["dal7day"]
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1315_nal7utg7(df):
    breakdowns = ["dgender", "age1315"]
    question = "nal7utg7"
    filter_condition = "dallast5 == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_age1115_dalfrq7(df):
    breakdowns = ["dgender", "age1115"]
    question = "dalfrq7"
    filter_condition = None
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_age1115_daldrunk(df):
    breakdowns = ['dgender', 'age1115']
    question = 'daldrunk'
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_stats_dgender_age1315_nal7(df):

    breakdowns = ["dgender", "age1315"]
    questions = ["nal7ut", "nal7br", "nal7cd", "nal7pp", "nal7sp",
                 "nal7winsh"]
    base = "nal7ut"
    filter_condition = "dallast5 == 1"

    return create_breakdown_statistics(df, breakdowns, questions, base,
                                       filter_condition)


def create_breakdown_stats_dgender_age1315_al7(df):

    breakdowns = ["dgender", "age1315"]
    questions = ["dal7day"]
    base = "dal7day"
    filter_condition = None

    return create_breakdown_statistics(df, breakdowns, questions, base,
                                       filter_condition)


def create_breakdown_dgender_dagedrank(df):
    breakdowns = ["dgender"]
    question = "dagedrank"
    filter_condition = "(alevr == 1)  & (age1115 == 15)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_dalagedru(df):
    breakdowns = ["dgender"]
    question = "dalagedru"
    filter_condition = "(age1115 == 15) & (alevrdnk == 1)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question,
                                   filter_condition, subgroup)


def create_breakdown_dgender_age1115_dal4dru5(df):
    breakdowns = ["dgender", "age1115"]
    question = "dal4dru5"
    filter_condition = None
    subgroup = {10: [2, 3, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_typedrank(df):
    breakdowns = ["dgender"]
    responses = ["nal7br", "nal7cd", "nal7pp", "nal7sp", "nal7winsh"]
    question = "typedrank"
    base = "nal7ut"
    filter_condition = "dallast5 == 1"

    return create_breakdown_multiple_cont(df, breakdowns, responses,
                                          question, base, filter_condition)


def create_breakdown_dgender_age1315_dal7day(df):
    breakdowns = ["dgender", "age1315"]
    question = "dal7day"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_age1315_dal7(df):

    breakdowns = ["dgender", "age1315"]
    responses = ["dal7beerlg", "dal7cidn", "dal7winsh", "dal7spir", "dal7pops",
                 "dal7any"]
    question = "typedrank"
    bases = responses
    filter_condition = "dallast5 == 1"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1315_dalunitsday(df):
    breakdowns = ["dgender", "age1315"]
    question = "dalunitsday"
    filter_condition = "dallast5 == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


# Pupils who drink tables begin here

def create_breakdown_dgender_age1315_dal4dru5(df):
    breakdowns = ["dgender", "age1315"]
    question = "dal4dru5"
    filter_condition = "dal4dru5 != 5"
    subgroup = {7: [2, 3, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_alcohol_howobtain_all(df):

    breakdowns = ["dgender", "age1215", "nal7utg4"]
    responses = ["dalshop4", "dalpub4", "algivpar", "algivfre",
                 "algivrel", "algivsib", "algivoth", "altakhom", "altakfre",
                 "alstlhom", "alstlfre", "alstloth", "dalgot4"]
    question = "howobtain"
    bases = responses
    filter_condition = "alevr in [1, -7]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_alcohol_howobtain(df):

    breakdowns = ["dgender", "age1215", "nal7utg4"]
    responses = ["dalshop4evr", "dalpub4evr", "algivpar", "algivfre",
                 "algivrel", "algivsib", "algivoth", "altakhom", "altakfre",
                 "alstlhom", "alstlfre", "alstloth", "dalgot4evr"]
    question = "howobtain"
    bases = responses
    filter_condition = "dalgot4evr == 1"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1215_nal7ut_wherebuy(df):

    breakdowns = ["dgender", "age1215", "nal7utg4"]
    responses = ["albuyels", "albuyfre", "albuygar", "albuyoff", "albuypub",
                 "albuyshp", "albuystr", "albuyclu", "dalbuyper", "dalbuyret",
                 "albuynev"]
    question = "wherebuy"
    bases = responses
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1215_nal7ut_wheredrink(df):

    breakdowns = ["dgender", "age1215", "nal7utg4"]
    responses = ["alushom", "alusohm", "dalushmo", "alusclu", "alusfre",
                 "aluspub", "alusstr", "alusels"]
    question = "wheredrink"
    bases = responses
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1315_al4wdedr(df):
    breakdowns = ["dgender", "age1315"]
    question = "al4wdedr"
    filter_condition = "(al4wdru == 1) & (al4wfrq > -1)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_dal4dru5_drunkadverse(df):

    breakdowns = ["dgender", "dal4dru5"]
    responses = ["dal4warg", "dal4wdam", "dal4wfig", "dal4whos", "dal4will",
                 "dal4wlst", "dal4wpol", "dal4wvom"]
    question = "drunkadverse"
    bases = responses
    filter_condition = "dal4dru5 in [2, 3]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1215_nal7ut_whodrink(df):

    breakdowns = ["dgender", "age1215", "nal7utg4"]
    responses = ["daluspar", "dalussib", "dalusfreb", "dalusfreo", "dalusfres",
                 "dalusgb", "dalusoth", "dalusfre", "alownoth"]
    question = "whodrink"
    bases = responses
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dallast3_dalfamknw(df):

    breakdowns = ["dallast3"]
    question = "dalfamknw"
    # Note: dalfamknw should not have a value 8, this filter is only needed so 2018 processing is correct
    filter_condition = "(dalfamknw != 8) & (dalfrq7 in [1, 2, 3, 4, 5, 6])"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_age1315_alcohol_buywherebuy(df):

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

def create_breakdown_dgender_age1115_dallast_nal7ut_dalfam(df):
    breakdowns = ["dgender", "age1115", "dallast3", "nal7utg4"]
    question = "dalfam"
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dalfamknw_dalfam(df):
    breakdowns = ["dalfamknw"]
    question = "dalfam"
    filter_condition = "(dalfrq7 in [1, 2, 3, 4, 5, 6]) & (dalfamknw == 1)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dalfam_dal4dru5(df):
    breakdowns = ["dalfam"]
    question = "dal4dru5"
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"
    subgroup = {7: [2, 3, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dalfam_dfasbands_imdquin_dallast3(df):

    breakdowns = ["dalfam", "dfasbands", "imdquin"]
    question = "dallast3"
    filter_condition = "dalfrq7 in [1, 2, 3, 4, 5, 6]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_age1115_dallast_attitudes(df):

    breakdowns = ["dgender", "age1115", "dallast3"]
    responses = ["dokal1", "dokalw", "dokdk1", "dokdkw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dal4dru_attitudes(df):

    breakdowns = ["dal4dru5"]
    responses = ["dokal1", "dokalw", "dokdk1", "dokdkw"]
    question = "attitudes"
    bases = responses
    filter_condition = "(dallast5 in [1, 2]) & (al4wdru >= 0)"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dfasbands_imdquin_dallast3(df):

    breakdowns = ["dfasbands", "imdquin"]
    question = "dallast3"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)

# School lesson tables begin here


def create_breakdown_dgender_syear_puplessons(df):

    breakdowns = ["dgender", "syear"]
    responses = ["dlssmk", "dlsalc", "dlsdrg"]
    question = "puplessons"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_syear_info(df):

    breakdowns = ["dgender", "syear"]
    responses = ["deinfsmk", "deinfalc", "deinfdrg"]
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
                 "q7youth", "q7agen", "q7pshe"]
    question = "contributes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_sources(df):

    breakdowns = []
    responses = ["q8frank", "q8pshe", "q8search", "q8tes", "q8oteach",
                 "q8dfe"]
    question = "sources"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_otheradvice(df):
    breakdowns = []
    responses = ["q10assem", "q10advic", "q10leaf", "q10post", "q10speak",
                 "edadvice"]
    question = "otheradvice"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_lessonssmoking(df):
    breakdowns = None
    questions = ["y7smok", "y8smok", "y9smok",
                 "y10smok", "y11smok"]
    filter_condition = "{question} != 6"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_lessonsdrinking(df):
    breakdowns = None
    questions = ["y7alc", "y8alc", "y9alc",
                 "y10alc", "y11alc"]
    filter_condition = "{question} != 6"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_lessonsdrugs(df):
    breakdowns = None
    questions = ["y7drg", "y8drg", "y9drg",
                 "y10drg", "y11drg"]
    filter_condition = "{question} != 6"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


# Smoking prevalence tables begin here


def create_breakdown_dgender_age_region_ethnicgp5_dcgstg5(df):

    breakdowns = ["dgender", "age1115", "region", "ethnicgp5"]
    question = "dcgstg5"
    filter_condition = None
    subgroup = {6: [1, 2], 7: [1, 2, 3, 4]}

    return create_breakdown_single(df, breakdowns, question, filter_condition,
                                   subgroup)


def create_breakdown_dgender_age_cg7(df):

    breakdowns = ["dgender", "age1115"]
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


def create_breakdown_stats_dgender_dcgstg3_dcg7tot(df):

    breakdowns = ["dgender", "dcgstg3"]
    questions = ["dcg7tot"]
    base = "dcg7tot"
    filter_condition = "dcgstg3 in [1, 2]"

    return create_breakdown_statistics(df, breakdowns, questions, base,
                                       filter_condition)


def create_breakdown_stats_dgender_dcgstg3_cg7(df):

    breakdowns = ["dgender", "dcgstg3"]
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


def create_breakdown_dcgstg3_dgender_age1315_cgsourcecurr(df):
    breakdowns = ["dcgstg3", "dgender", "age1315"]
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


def create_breakdown_dgender_cglong(df):

    breakdowns = ["dgender"]
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


def create_breakdown_dgender_dcgtrystp(df):

    breakdowns = ["dgender"]
    question = "dcgtrystp"
    filter_condition = "dcgstg3 == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_age1215_dcgoft_methodv2(df):
    breakdowns = ["dcgoft"]
    responses = ["dcggupno", "dcggupfa", "dcggupni", "dcggupad", "dcggupgp",
                 "dcggupst", "dcgguphe", "dcggupev", "dcggupany"]
    question = "method"
    bases = responses
    filter_condition = "dcgoft == 3"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dcgstg3_dcgsec2(df):

    breakdowns = ["dcgstg3"]
    question = "dcgsec2"
    filter_condition = "dcgstg3 in [1, 2]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


# Smoking context tables begin here


def create_breakdown_dfasbands_imdquin_dcgstg3(df):

    breakdowns = ["dfasbands", "imdquin"]
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


def create_breakdown_dgender_age1315_dcgstg3_dcgfam(df):

    breakdowns = ["dgender", "dcgstg3"]
    question = "dcgfam"
    filter_condition = "dcgstg3 in [1, 2]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1315_dcgstg2_dcgfam(df):

    breakdowns = ["dgender", "age1115", "dcgstg2"]
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


def create_breakdown_dgender_age1115_dcgstg3_attitudes(df):
    breakdowns = ["dgender", "age1115", "dcgstg3"]
    responses = ["dokcg1", "dokcgw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1115_dcgstg2_attitudes(df):
    breakdowns = ["dgender", "age1115", "dcgstg2"]
    responses = ["dokcg1", "dokcgw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


# E cigarette use tables begin here


def create_breakdown_dgender_age1315_cgelechd(df):

    breakdowns = ["dgender", "age1115"]
    question = "cgelechd"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1315_ecig_sources(df):
    breakdowns = ["dgender", "age1315"]
    responses = ["dcgelgtoth", "dcgelgtgiv", "dcgelgtshp", "dcgelgtppl", "cgelgtgiv",
                 "cgelgtsib", "cgelgtpar", "cgelgtelg", "cgelgtnew", "cgelgtsho",
                 "cgelgtsup", "cgelgtpha", "cgelgtgar", "cgelgtgot", "cgelgtfre",
                 "cgelgtels", "cgelgtmar", "cgelgtint", "cgelgttak"]
    question = "sources"
    bases = responses
    filter_condition = "dcgelec == 6"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1115_region_dcgstg5_dcgelec(df):

    breakdowns = ["dgender", "age1115", "region", "dcgstg5"]
    question = "dcgelec"
    filter_condition = None
    subgroup = {7: [1, 2], 8: [5, 6], 9: [3, 4, 5, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1115_ecig_attitudes(df):
    breakdowns = ["dgender", "age1115"]
    responses = ["dokec1", "dokecw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_cgellong(df):

    breakdowns = ["dgender"]
    question = "cgellong"
    filter_condition = "dcgelec == 6"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_cgnbavap(df):

    breakdowns = ["dgender"]
    question = "cgnbavap"
    filter_condition = "dcgelec in [3, 4, 5, 6]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


# Drug prevalence tables begin here


def create_breakdown_dgender_age1115_region_ethnicgp5_druguse(df):
    breakdowns = ["dgender", "age1115", "region", "ethnicgp5"]
    responses = ["ddgany", "ddgyrany", "ddgmonany", "ddganynotvs",
                 "ddgyranynotvs", "ddgmonanynotvs"]
    question = "druguse"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1315_ddgyrty(df):

    breakdowns = ["dgender", "age1315"]
    question = "ddgyrty"
    filter_condition = "ddgyrty != 7"
    subgroup = {10: [1, 2, 3, 4], 11: [5, 6]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1115_ddgoc(df):

    breakdowns = ["dgender", "age1115"]
    question = "ddgoc"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1115_drugusetype(df):
    breakdowns = ["dgender", "age1115"]
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


def create_breakdown_dgender_age1315_dgocleg(df):

    breakdowns = ["dgender", "age1315"]
    question = "dgocleg"
    filter_condition = "dgocleg in [1, 2, 3, 4]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1315_drugoccasion(df):

    breakdowns = ["dgender"]
    questions = ["dgocamp", "dgoccan", "dgoccok", "dgoccrk", "dgocecs", "dgocgas",
                 "dgocher", "dgocket", "dgocleg", "dgoclsd", "dgocmph", "dgocmsh",
                 "dgocmth", "dgocnox", "dgocoth", "dgocpop", "dgoctrn"]
    filter_condition = "ddgany == 1"
    subgroup = None

    return create_breakdown_single_combine(df, breakdowns, questions,
                                           filter_condition, subgroup)


def create_breakdown_age1315_ddgyrty5_ddgoc(df):

    breakdowns = ["age1315", "ddgyrty5"]
    question = "ddgoc"
    filter_condition = "ddgyrany == 1"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1315_ddgtypleg(df):

    breakdowns = ["dgender", "age1315"]
    question = "ddgtypleg"
    filter_condition = "dgocleg in [1, 2, 3, 4]"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1215_ddgfq6(df):

    breakdowns = ["dgender", "age1215"]
    question = "ddgfq6"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1215_ddgfq8(df):

    breakdowns = ["dgender", "age1215"]
    question = "ddgfq8"
    filter_condition = None
    subgroup = {10: [1, 2, 3]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1315_ddgfq8_lastyr(df):

    breakdowns = ["dgender", "age1315"]
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


def create_breakdown_dgender_age1115_drugoff(df):
    breakdowns = ["dgender", "age1115"]
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


def create_breakdown_dgender_age15_anydrugofftaken(df):
    breakdowns = ["dgender"]
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


def create_breakdown_dgender_age15_canofftaken(df):
    breakdowns = ["dgender"]
    question = "dgtdcan"
    filter_condition = "(age1115 == 15) & (ddgofcan == 1) & (dusecan > 0)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age15_claofftaken(df):
    breakdowns = ["dgender"]
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


def create_breakdown_dgender_age1315_ddglttyp(df):
    breakdowns = ["dgender", "age1315"]
    question = "ddglttyp"
    filter_condition = "ddgoc == 3"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


# Pupils who take drugs tables begin here

def create_breakdown_dgender_ddgageany11_ddgfttyp_dgftwh(df):
    breakdowns = ["dgender", "ddgageany11", "ddgfttyp"]
    question = "dgftwh"
    filter_condition = "ddgany == 1"
    subgroup = {20: [2, 3, 4, 5]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1315_ddglttyp_dgltwh(df):
    breakdowns = ["dgender", "age1315", "ddglttyp"]
    question = "dgltwh"
    filter_condition = "ddgoc == 3"
    subgroup = {20: [2, 3, 4, 5]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1315_ddglttyp_dgltwhr(df):
    breakdowns = ["dgender", "age1315", "ddglttyp"]
    question = "dgltwhr"
    filter_condition = "ddgoc == 3"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age_ddgofany_ddgget(df):
    breakdowns = ["dgender", "age1115", "age1315", "ddgofany"]
    question = "ddgget"
    filter_condition = None
    subgroup = {10: [3, 4], 11: [1, 2]}

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1315_ddglttyp_whowith(df):
    breakdowns = ["dgender", "age1315", "ddglttyp"]
    responses = ["ddgltwogbf", "ddgltwofrs", "ddgltwofro", "ddgltwofrb", "ddgltwopar",
                 "ddgltwooth", "ddgltwoels", "ddgltown", "ddgltwofre"]
    question = "whowith"
    bases = responses
    filter_condition = "ddgoc == 3"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1115_dgbuy(df):
    breakdowns = ["dgender", "age1115"]
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

def create_breakdown_dgender_ddgageany11_ddgfttyp_ddgftwy(df):
    breakdowns = ["dgender", "ddgageany11", "ddgfttyp"]
    responses = ["dgftwylke", "dgftwyhig", "dgftwyfri", "dgftwynbt", "dgftwyfor",
                 "dgftwyoff", "dgftwydar", "dgftwycoo", "dgftwyoth", "dgftwynkn",
                 "dgftwynre"]
    question = "ddgftwy"
    bases = responses
    filter_condition = "ddgany == 1"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1315_ddglttyp_ddgoc_ddgltwy(df):
    breakdowns = ["dgender", "age1315", "ddglttyp", "ddgoc"]
    responses = ["dgltwycoo", "dgltwydar", "dgltwyfor", "dgltwyfri",
                 "dgltwyhig", "dgltwylke", "dgltwynbt", "dgltwynkn",
                 "dgltwynre", "dgltwyoff", "dgltwyoth"]
    question = "ddgltwy"
    bases = responses
    filter_condition = "ddgoc == 3"

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1115_drugattitudes(df):
    breakdowns = ["dgender", "age1115"]
    responses = ["dokcan1", "dokvs1", "dokcoc1", "dokcanw", "dokvsw", "dokcocw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


def create_breakdown_dgender_age1115_ddgfam(df):
    breakdowns = ["dgender", "age1115"]
    question = "ddgfam"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_ddgfamknw_ddgfam(df):
    breakdowns = ["ddgfamknw"]
    question = "ddgfam"
    filter_condition = "(ddgany == 1) & (ddgfamknw == 1)"
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


# TODO review when table are produced
def create_breakdown_ddgfam5_ddgoc(df):
    breakdowns = ["ddgfam5"]
    question = "ddgoc"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dfasbands_imdquin_ddglast3(df):
    breakdowns = ["dfasbands", "imdquin"]
    question = "ddglast3"
    filter_condition = "ddglast3 in [1, 2, 3, 4]"
    subgroup = {5: [2, 3]}

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
    responses = ["dokcg1", "dokal1", "dokdk1", "dokcan1", "dokvs1", "dokcoc1",
                 "dokec1", "dokcgw", "dokalw", "dokdkw", "dokcanw", "dokvsw",
                 "dokcocw", "dokecw"]
    question = "attitudes"
    bases = responses
    filter_condition = None

    return create_breakdown_multiple_discrete(df, breakdowns, responses,
                                              question, bases, filter_condition)


# Wellbeing tables begin here

def create_breakdown_dgender_age1115_region_dlifsat(df):
    breakdowns = ["dgender", "age1115", "region"]
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


def create_breakdown_dgender_age1115_region_dlifwor(df):
    breakdowns = ["dgender", "age1115", "region"]
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


def create_breakdown_dgender_age1115_region_dlifhap(df):
    breakdowns = ["dgender", "age1115", "region"]
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


def create_breakdown_dgender_age1115_region_dlifanx(df):
    breakdowns = ["dgender", "age1115", "region"]
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


def create_breakdown_dgender_age1115_dliflow(df):
    breakdowns = ["dgender", "age1115"]
    question = "dliflow"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1115_region_dloncomp(df):
    breakdowns = ["dgender", "age1115", "region"]
    question = "dloncomp"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dloncomp(df):
    breakdowns = ["cg7", "dallast5", "ddgmonany", "dmulticount"]
    question = "dloncomp"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1115_region_lonlonely(df):
    breakdowns = ["dgender", "age1115", "region"]
    question = "lonlonely"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_cg7_dallast5_ddgmonany_dmulticount_lonlonely(df):
    breakdowns = ["cg7", "dallast5", "ddgmonany", "dmulticount"]
    question = "lonlonely"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1115_lontalk(df):
    breakdowns = ["dgender", "age1115"]
    question = "lontalk"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1115_lonout(df):
    breakdowns = ["dgender", "age1115"]
    question = "lonout"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)


def create_breakdown_dgender_age1115_lonalone(df):
    breakdowns = ["dgender", "age1115"]
    question = "lonalone"
    filter_condition = None
    subgroup = None

    return create_breakdown_single(df, breakdowns, question, filter_condition, subgroup)
