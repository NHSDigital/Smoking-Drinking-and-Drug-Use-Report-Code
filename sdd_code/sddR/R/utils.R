
#' Try to convert the argument to a formula
#'
#' @param x A string, character vector, or formula
#'
#' @return A formula
#'
#' @export
coerce_formula <- function(x) {
    # If x is a formula, do nothing
    if (!inherits(x, "formula")) {
        # Coerce to character if not
        x <- as.character(x)
        # If it looks like a formula, just convert
        if (all(grepl("~", x, fixed=TRUE))) {
            x <- as.formula(x)
        } else {
            # If it doesn't look like a formula, add a tilde and try to
            # sep with + in case it is a vector
            x <- as.formula(paste0("~", paste(x, collapse="+")))
        }
    }

    return(x)
}
