library(argparse)
library(readr)
library(jsonlite)


compute_average_partial <- function(df, column_name) {
  if (!is.data.frame(df)) {
    stop("The provided object is not a dataframe.")
  }

  if (!column_name %in% names(df)) {
    stop("The specified column does not exist in the dataframe.")
  }

  total_sum <- sum(df[[column_name]])
  count <- nrow(df)

  # a json like this is expected by central function: {"sum": "123", "count": "42"}
  # (or {"sum": 123, "count": 42}?)
  # In R, list can hold key-value pairs
  return(list(
    sum = total_sum,
    count = count
  ))
}


parser <- ArgumentParser()
parser$add_argument("--column-name", default="", help="Name of the column in csv file to sum and count")
parser$add_argument("--csv-input", default="", help="Path to file for input")
parser$add_argument("--json-output", default="", help="Path to file for output")
args <- parser$parse_args()

# set input variables
df <- read_csv(args$csv_input)
column_name <- args$column_name

# compute partial average
result <- compute_average_partial(df, column_name)

# write json at specified path via args
# auto_unbox=TRUE means it won't produce {"sum": [123], "count": [42]}
write_json(result, args$json_output, auto_unbox=TRUE)
