Warning - this repository is a snapshot of a repository internal to NHS Digital. This means that links to videos and some URLs may not work.***

***Repository owner: Analytical Services: Population Health, Clinical Audit and Specialist Care***

***Email: lifestyles@nhs.net***

***To contact us raise an issue on Github or via email and we will respond promptly.***

# Smoking, drinking and drug use amongst young people (SDD) survey background

This repository contains the code used by NHS England to create publication outputs from the 2021 SDD survey. 

***Results from the 2023 survey were published on 17th October 2024.
The updated version of the repository used to create the 2023 outputs will be published to GitHub later in 2024.***

The SDD dataset contains results from a biennial survey of secondary school pupils 
in England in years 7 to 11 (mostly aged 11 to 15), focusing on smoking, drinking
and drug use. It covers a range of topics including prevalence, habits, attitudes, 
and wellbeing.

The dataset is compiled by IPSOS MORI and provided as 2 SPSS (.sav) files: one pupil
file containing pupil details and question responses, and one school file containing
teacher responses.

This project produces the required publication outputs: Data tables, charts, raw
data file for the UK data archive.

# Getting Started

## Clone repository
To clone respositary, please see our [community of practice page](https://github.com/NHSDigital/rap-community-of-practice/blob/main/development-approach/02_using-git-collaboratively.md).

## Set up environment
There are two options to set up the python enviroment:
1. Pip using `requirements.txt`.
2. Conda using `environment.yml`.

Users would need to delete as appropriate which set they do not need. For details, please see our [virtual environments in the community of practice page](https://github.com/NHSDigital/rap-community-of-practice/blob/main/python/virtual-environments.md).


Run the following command in Terminal or VScode to set up the packages:
```
pip install --user -r requirements.txt
```

or if using conda environments:
```
conda env create -f environment.yml
```
Then follow the instructions in [sdd_code/sddR/README.md](sdd_code/sddR/README.md) to setup the R packages.

# Directory structure:
```
smoking-drinking-and-drug-use-rap
│   .gitignore                              - Used to prevent files from being committed to this repo
│   conftest.py                             - Defines custom functions used when testing the code
│   environment.yml                         - Used to install the conda environment
│   LICENSE
│   pytest.ini                              - Defines the default options when running pytest
│   README.md
│   requirements.txt                        - Used to install the python dependencies
│   setup.py                                - Used to install this pipeline as a package, not yet in use
│
├───sdd_code                                - This is the main code directory
│   │   create_models.py                    - This script generates the logistic regression models
│   │   create_publication.py               - This script runs the entire publication except for the models
│   │   __init__.py
│   │
│   ├───models                              - Contains the Python modelling code, see the README within for details
│   │
│   ├───sddR                                - Contains all the R code used in the package, see the README within for details
│   │
│   ├───utilities                           - This module contains all the main modules used to create the publication
│   │   │   chapters.py                     - Defines the output excel files, which tables are in each and their names
│   │   │   data_import.py                  - Contains functions for reading in the .SAV files
│   │   │   derivations.py                  - Contains every derived field in the publication as a function
│   │   │   difference.py                   - Contains functions used to check the difference between tables
│   │   │   logger_config.py                - The configuration functions for the publication logger
│   │   │   metadata.py                     - Functions used to save and manipulate the metadata of the .SAV files
│   │   │   parameters.py                   - Contains parameters that define the how the publication will run
│   │   │   processing.py                   - Defines the main functions used to manipulate data and produce outputs
│   │   │   publication.py                  - Contains functions used to create publication ready outputs
│   │   │   stats.py                        - Contains the Python statistical functions
│   │   │   stats_R.py                      - Contains the Python functions that call R statistical functions
│   │   │   tables.py                       - Contains every output table defined as a function
│   │   │   __init__.py
│
├───tests                               
│   │   run_import_validation.py            - Runs the pytest tests that check input .SAV files
│   │   run_unittests.py                    - Runs all unit tests
│   │   __init__.py 
│   │
│   ├───backtests                           - Testing against previous years data, currently not done in Python
│   │
│   ├───data                                - Dummy data used in some tests
│   │       test_data.sav
│   │
│   ├───datatests                           - The input data tests, check the README within for more
│   │
│   ├───Rtests                              - Tests for all Python functions that call R under the hood
│   │   │   test_logit_model_R.py
│   │   │   test_logit_model_rpy2.py
│   │   │   test_R.py
│   │   │   test_r_integration.py
│   │   │   test_stats_R.py
│   │
│   ├───unittests                           - Unit tests for all Python functions/modules
│   │   │   test_data_import.py
│   │   │   test_derivations.py
│   │   │   test_metadata.py
│   │   │   test_processing.py
│   │   │   test_stats.py
│   │   │   __init__.py
```

# Runing the publication process

There are three main files that users running the process will need to interact with:

- [parameters.py](sdd_code/utilities/parameters.py)

- [create_publication.py](sdd_code/create_publication.py)

- [create_models.py](sdd_code/create_models.py)

The file parameters.py contains all of the things that we expect to change from one publication
to the next. Indeed, if the methodology has not changed, then this should be the only file you need
to modify. This file specifies the input and output folder locations, the survey year,
what questions to drop on import etc., and also allows the user to control which chapters
of the report they want to run (all, single or multiple). It also allows the user to control
if the input tests are run as part of the main process (see the README file under the tests folder
for details of that process).

The publication process is run using the top-level script, create_publication.py. 
This script imports and runs all the required functions and from the sub-modules.

The models are ran using the top level script create_models.py, which uses R and rpy2 to create the models in Python. For more info, check the [README](sdd_code/models/README.md).

# Link to the publication
https://digital.nhs.uk/data-and-information/publications/statistical/smoking-drinking-and-drug-use-among-young-people-in-england

# License
The SDD publication codebase is released under the MIT License.

Copyright © 2022, Health and Social Care Information Centre. The Health and Social Care Information Centre is a non-departmental body created by statute, also known as NHS Digital.
________________________________________
You may re-use this document/publication (not including logos) free of charge in any format or medium, under the terms of the Open Government Licence v3.0.
Information Policy Team, The National Archives, Kew, Richmond, Surrey, TW9 4DU;
email: psi@nationalarchives.gsi.gov.uk


