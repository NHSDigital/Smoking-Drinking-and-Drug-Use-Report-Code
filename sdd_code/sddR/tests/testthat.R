# Clean environment
rm(list=ls())

library(testthat)
library(survey)

if (file.exists(here::here("R", "model_functions.R"))) {
    source(here::here("R", "model_functions.R"))
    source(here::here("R", "stats_functions.R"))
    path <- here::here("tests", "testthat")
} else {
    source(here::here("sdd_code", "sddR", "R", "model_functions.R"))
    source(here::here("sdd_code", "sddR", "R", "stats_functions.R"))
    path <- here::here("sdd_code", "sddR", "tests", "testthat")
}

test_dir(path=path)

# Clean environment
rm(list=ls())
