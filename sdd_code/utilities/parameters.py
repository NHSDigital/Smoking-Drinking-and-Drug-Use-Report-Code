# Set the parameters for the project
import pathlib

# Sets the file paths for the project
BASE_DIR = pathlib.Path(r"\\projectfilepath\")
INPUT_DIR = BASE_DIR / "Inputs"
OUTPUT_DIR = BASE_DIR / "Outputs"
PUPIL_DIR = INPUT_DIR / "PupilData"
TEACHER_DIR = INPUT_DIR / "TeacherData"

# Sets the filepaths for the publication outputs
PUB_DIR = OUTPUT_DIR / "PublicationFiles"
TAB_DIR = PUB_DIR / "DataTables"

# Set the location of metadata - used for testing
META_DIR = BASE_DIR / "Metadata" / "Latest"
PUPIL_META_DIR = META_DIR / "PupilData"
TEACHER_META_DIR = META_DIR / "TeacherData"

# Set the report location - for outputting test reports
REPORT_DIR = OUTPUT_DIR / "ProcessTests"

# Set the location of the previous year data files - for year on year checks
PREVYEAR_DIR = OUTPUT_DIR / "MasterFiles" / "PreviousSourceFiles"

# Set the data asset location - for outputting final survey data to csv
ASSET_DIR = OUTPUT_DIR / "DataAsset"

# Sets the name of the current sav pupil file to be imported (with extension)
PUPIL_FILE = "SDD21_pupils.sav"
PUPIL_DATA_PATH = PUPIL_DIR / PUPIL_FILE

# Sets the name of the current SAV teacher file to be imported (with extension)
TEACHER_FILE = "SDD21_teachers.sav"
TEACHER_DATA_PATH = TEACHER_DIR / TEACHER_FILE

# Sets the reporting year (calender year in format yyyy)
YEAR = "2021"

# Set the number of rows in the pupil dataset, used for checks:
NUM_PUPIL_ROWS = 9288
# Set the number of rows in the teacher dataset, used for checks:
NUM_TEACHER_ROWS = 99

# Sets whether input tests are run as part of the main pipeline
# Set to True or False
RUN_PUPIL_INPUT_TESTS = False
RUN_TEACHER_INPUT_TESTS = False
# Sets whether unit tests are run as part of the main pipeline
# Set to True or False
RUN_DERIVATION_UNIT_TESTS = False
RUN_PROCESSING_UNIT_TESTS = False

# Set which chapters should be run as part of the main pipeline (True or False)
# Can be used to run individual chapter outputs if required
# if CHAPTERS_ALL is set to TRUE then all chapters will be run regardless of other chapter settings
# CHAPTERS_ALL must be set to TRUE for CI publication outputs to be generated
CHAPTER_ALL = True
CHAPTER_SMOKING_PREVALANCE = False
CHAPTER_YOUNG_WHO_SMOKE = False
CHAPTER_SMOKING_CONTEXT = False
CHAPTER_ECIGARETTE_USE = False
CHAPTER_DRINKING_PREVALANCE = False
CHAPTER_YOUNG_WHO_DRINK = False
CHAPTER_DRINK_CONTEXT = False
CHAPTER_DRUG_PREVALENCE = False
CHAPTER_YOUNG_WHO_DRUGS = False
CHAPTER_DRUG_CONTEXT = False
CHAPTER_SCHOOL_LESSONS = False
CHAPTER_MULTI_BEHAVIOURS = False
CHAPTER_WELLBEING = False
CHAPTER_COVID_IMPACT = False
CHAPTER_SURVEY_DELIVERY = False

# Set to True to default to creating standard errors for all breakdowns,
# Must be to set to True for CI publication outputs to be generated
# False to default to not creating standard errors
CREATE_SE = True

# Set to True to check the difference between this year and the last, else leave blank
CHECK_PREV_YEAR = False
# For the year on year checks set the breach level at which a change will be flagged
BREACH_LEVEL = 15

# Set whether the final publication outputs should be written as part of the pipeline
# To produce CI publication outputs, CREATE_SE and CHAPTER_ALL above must also be set to True
RUN_PUBLICATION_OUTPUTS = True
# Set whether the updated pupil and school datasets are written to permanent outputs (csv)
WRITE_ASSET = False

# This sets the variable to be used as the pupil weighting
WEIGHTING_VAR = "pupilwt"

# Set the variable that describes the strata
STRATA = "region"

# Set the variable that describe the PSUs, or clusters
PSU = "archschn"

# Sets the code that will be allocated to the breakdown totals (e.g. all ages)
# Pick a code that is clearly not a real value
TOT_CODE = 9999

# Set the local root of the project, where this repo exists locally
LOCAL_ROOT = pathlib.Path(__file__).parents[2]

# The base shorthands for all drugs
DRUGS = [
    "amp",  # Amphetamines
    "can",  # Cannabis
    "cok",  # Coke
    "crk",  # Crack
    "ecs",  # Ecstasy
    "gas",  # Glue, gas, aerosols or solvents (volatile substances)
    "her",  # Heroin
    "ket",  # Ketamine
    "leg",  # New psychoactive substances (previously known as legal highs)
    "lsd",  # LSD
    "mph",  # Mephedrone
    "msh",  # Magic mushrooms
    "mth",  # Methadone
    "nox",  # Nitrous oxide
    "oth",  # Other drugs
    "pop",  # Poppers
    "trn"   # Tranquillisers
]

# Note that amphetamines are not included here as only Class A when injected
DRUGS_CLASSA = [
    "cok",  # Coke
    "crk",  # Crack
    "ecs",  # Ecstasy
    "her",  # Heroin
    "lsd",  # LSD
    "msh",  # Magic mushrooms
    "mth",  # Methadone
]

# Mapping of each factor, or class variable in SAS, to the
# reference level to use in the logistic model.
# If adding a new categorical effect to the variable then need
# to add it to this dict.
# To use, convert to dataframe with pd.DataFrame(**FACTOR_REF)
FACTOR_REF = {
    "columns": ["factors", "refs"],
    "data": [
        ["age1215", "12"],
        ["age1315", "13"],
        ["cgelecevr", "1"],
        ["dalfam", "1"],
        ["dallast3", "3"],
        ["dallastwk", "0"],
        ["dcgfam4", "1"],
        ["dcgppfr", "0"],
        ["dcgsmk", "0"],
        ["dcgstg3", "3"],
        ["ddgdrugs", "1"],
        ["ddgfam", "1"],
        ["ddgmonany", "0"],
        ["dalwhodr", "0"],
        ["dcgwhosmo", "0"],
        ["dfasbands", "3"],
        ["dlifanx", "1"],
        ["dlifhap", "4"],
        ["dlifsat", "4"],
        ["dlifwor", "4"],
        ["dlsalc", "1"],
        ["dlsdrg", "1"],
        ["dlssmk", "1"],
        ["ethnicgp4", "1"],
        ["excla", "2"],
        ["met4wks", "1"],
        ["region", "7"],
        ["sex", "1"],
        ["schlearn", "1"],
        ["truant", "2"],
    ],
}

# Sets the columns to be dropped from pupil import data. This is a fixed list of the old derived fields so should not require an update
DROP_COLUMNS = [
    "age1115",
    "age1215",
    "age1315",
    "cg7tot",
    "cg7totg",
    "cg7totg3",
    "cg7totg4",
    "cgbuyng",
    "cgdiffg",
    "cglongg",
    "cgstopb",
    "cgstopwb",
    "dal4dru",
    "dal4dru2",
    "dal4pub",
    "dal4shp",
    "dalfam",
    "dalfamknw",
    "dalfrq3",
    "dalfrq5",
    "dalfrq6",
    "dalfrq6x",
    "dalfrq8",
    "dalgot4w",
    "dallast3",
    "dallast5",
    "dalpub4",
    "dalshop4",
    "daltry4w",
    "dalwhodr",
    "dcgage",
    "dcgelbuy",
    "dcgelec",
    "dcgfam",
    "dcgfam4",
    "dcgget",
    "dcggeta",
    "dcggeto",
    "dcggupad",
    "dcggupecg",
    "dcggupfa",
    "dcggupgp",
    "dcgguphe",
    "dcggupni",
    "dcggupno",
    "dcggupst",
    "dcgppfam",
    "dcgppfr",
    "dcgoft",
    "dcgopen",
    "dcgsec",
    "dcgtype",
    "dcgsec2",
    "dcgsec4",
    "dcgstg3",
    "dcgstg5",
    "dcgstg6",
    "dwholiv",
    "dcgwhosmo",
    "ddgage",
    "ddgage11",
    "ddgage12",
    "ddgageamp",
    "ddgagecan",
    "ddgagecla",
    "ddgagecok",
    "ddgagecrk",
    "ddgageecs",
    "ddgagegas",
    "ddgageher",
    "ddgageket",
    "ddgageleg",
    "ddgagelsd",
    "ddgagemph",
    "ddgagemsh",
    "ddgagemth",
    "ddgagenox",
    "ddgageoth",
    "ddgagepop",
    "ddgagetrn",
    "ddgany",
    "ddgany14",
    "ddganyvs14",
    "ddganynps",
    "ddganyps",
    "ddganypsvs",
    "ddganyvs",
    "ddgfam",
    "ddgfirst",
    "ddgfq6",
    "ddgfq8",
    "ddgfttyp",
    "ddglast3",
    "ddglttyp",
    "ddgmonany",
    "ddgmonanyps",
    "ddgmonanypsvs",
    "ddgmonanyvs",
    "ddgoc",
    "ddgofamp",
    "ddgofany",
    "ddgofanyps",
    "ddgofanypsvs",
    "ddgofcan",
    "ddgofcok",
    "ddgofcrk",
    "ddgofecs",
    "ddgofgas",
    "ddgofher",
    "ddgofket",
    "ddgofleg",
    "ddgoflsd",
    "ddgofmph",
    "ddgofmsh",
    "ddgofmth",
    "ddgofnox",
    "ddgofopi",
    "ddgofoth",
    "ddgofpop",
    "ddgofps",
    "ddgofpsy",
    "ddgofstm",
    "ddgoftrn",
    "ddgyrany",
    "ddgyrany14",
    "ddgyranyvs14",
    "ddgyranynps",
    "ddgyranyps",
    "ddgyranypsvs",
    "ddgyranyvs",
    "ddgyrty",
    "ddgyrty5",
    "devrcla",
    "devropi",
    "devrnps",
    "devrps",
    "devrpsy",
    "devrstm",
    "dexcla",
    "dfas",
    "dfasbands",
    "dghdany",
    "dghdanynps",
    "dghdanyps",
    "dghdany14",
    "dghdanyvs14",
    "dghdanynps",
    "dghdnps",
    "dghdopi",
    "dghdps",
    "dghdpsy",
    "dghdstm",
    "dgsharels",
    "dgsharfrb",
    "dgsharfri",
    "dgsharfro",
    "dgsharfrs",
    "dgshargbf",
    "dgsharnoo",
    "dgsharoth",
    "dgsharpar",
    "dlifanx",
    "dlifhap",
    "dlifsat",
    "dlifwor",
    "dlsalc",
    "dlsdrg",
    "dlssmk",
    "ddgmonany14",
    "ddgmonanyvs14",
    "ddgmonanynps",
    "dmoncla",
    "dmonnps",
    "dmonopi",
    "dmonps",
    "dmonpsy",
    "dmonstm",
    "dsmfhome",
    "dtruant",
    "duseamp",
    "dusecan",
    "dusecok",
    "dusecrk",
    "duseecs",
    "dusegas",
    "duseher",
    "duseket",
    "duseleg",
    "duselsd",
    "dusemph",
    "dusemsh",
    "dusemth",
    "dusenox",
    "duseoth",
    "dusepop",
    "dusetrn",
    "dyrcla",
    "dyrnps",
    "dyropi",
    "dyrps",
    "dyrpsy",
    "dyrstm",
    "ethnicgp",
    "ethnicgp5",
    "famdrin",
    "famsmok",
    "nal7br",
    "nal7sd",
    "nal7winsh",
    "nal7sp",
    "nal7pp",
    "nal7ut",
    "nal7utg",
    "nal7utg8",
    "sdwkcigg",
    "stopsmk",
    "trystop",
    "xxagecan",
    "xxageamp",
    "xxagelsd",
    "xxageecs",
    "xxagepop",
    "xxagetrn",
    "xxageher",
    "xxagemsh",
    "xxagemth",
    "xxagecrk",
    "xxagecok",
    "xxageket",
    "xxagemph",
    "xxagegas",
    "xxagenox",
    "xxageleg",
    "xxageoth",
    "xdgofcan",
    "xdgofamp",
    "xdgoflsd",
    "xdgofecs",
    "xdgofpop",
    "xdgoftrn",
    "xdgofher",
    "xdgofmsh",
    "xdgofmth",
    "xdgofcrk",
    "xdgofcok",
    "xdgofket",
    "xdgofmph",
    "xdgofgas",
    "xdgofnox",
    "xdgofoth",
    "xdgofleg",
    "xdgofstm",
    "xdgofpsy",
    "xdgofopi",
    "xdgofnps",
    "xdgofany14",
    "xdgofany",
    "xdgofanyvs14",
    "xdgofanynps",
    "wt_sdd_new",
]

# All columns that have age responses, used to create metadata for testing
AGE_COLUMNS = [
    "age",
    "cgagen",
    "cgage",
    "alage",
    "alagednk",
    "dgagecan",
    "dgageamp",
    "dgagelsd",
    "dgageecs",
    "dgagesem",
    "dgagepop",
    "dgagetrn",
    "dgageher",
    "dgagemsh",
    "dgagemth",
    "dgagecrk",
    "dgagecok",
    "dgageket",
    "dgagemph",
    "dgagegas",
    "dgagenox",
    "dgageoth",
    "dgagecla",
    "dgageleg",
]
