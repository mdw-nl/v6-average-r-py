compute_average_partial <- function(df, column_name) {
  if (!is.data.frame(df)) {
    stop("The provided object is not a dataframe.")
  }

  if (!column_name %in% names(df)) {
    stop("The specified column does not exist in the dataframe.")
  }

  total_sum <- sum(df[[column_name]])
  count <- nrow(df)

  return(data.frame(
    sum = total_sum,
    count = count
  ))
}

# Input variables that Python wrapper should have set via rpy2
df <- pyin_df
column_name <- pyin_column_name

# Compute partial average
result <- compute_average_partial(df, column_name)

# Python wrapper expects result in 'pyout_result' variable as a dataframe
pyout_result <- result

