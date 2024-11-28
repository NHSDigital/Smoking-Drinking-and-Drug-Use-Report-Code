# Package names, these will need to be manually updated
packages <- c("survey", "data.table", "ModelMetrics", "here", "getopt", "testthat")

print("Setting up packages")

# Install packages not yet installed
installed_packages <- packages %in% rownames(utils::installed.packages())
if (any(installed_packages == FALSE)) {
    cat("Install SDD R dependencies? (Y/[N]): ")
    cont <- readLines(stdin(), n=1)
    cat(cont, "\n")
    if (is.na(cont)) cont <- "N"

    if (toupper(cont) == "Y") {
        utils::install.packages(
            packages[!installed_packages],
            repos="https://cran.rstudio.com/"
        )
    }
}

rm(list=ls())
