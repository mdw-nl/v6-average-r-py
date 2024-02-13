import subprocess
from pathlib import Path
import pandas as pd
import csv

from vantage6.algorithm.tools.util import info, error, get_env_var
from vantage6.algorithm.tools.decorators import data

# 'vantage6-algorithm-tools' @data decorator reads the input CSV and converts
# it into a pandas dataframe. In this case, we want to feed our R script the
# path to the CSV, and we will only use the pandas dataframe to check that the
# user-provided column name exists before calling our R script.
@data(1)
def partial_average_r(pd_df: pd.DataFrame, column_name: str):
    """Compute the average partial"""
    # R script filename that will actually compute the (federated) average
    R_SCRIPT_FILENAME = 'average_r.R'

    # Due to MANIFEST.in, *.R files will be installed with python package
    r_script_path = Path(__file__).parent / R_SCRIPT_FILENAME

    # verify user input
    if not isinstance(column_name, str):
        error("Column name must be a string")
        exit(1)
    if not column_name in pd_df.columns:
        error("The column name provided via input by the user is not the dataset")
        exit(1)

    # Vantage6 node uses environment variables to pass information to the algorithm.
    # For example, and where (path) it (node) expects the output (via volume map)
    output_file = get_env_var("OUTPUT_FILE")

    # This is hacky, already done via @data decorator. But we want to feed the
    # R script the source CSV, which @data abstract us away from by only giving
    # us the resulting pandas dataframe.
    # Get dataset labels
    label = get_env_var("USER_REQUESTED_DATABASE_LABELS").split(",")[0]
    # This is how vantage6 passes database uri to the algorithm
    database_uri = get_env_var(f"{label.upper()}_DATABASE_URI")

    # sanity check
    if not Path(database_uri).exists():
        error("Expected CSV file not found")
        exit(1)

    # Execute R script
    command = [
        'Rscript',
        r_script_path,
        '--column-name', column_name,
        '--csv-input', database_uri,
        '--json-output', output_file
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors
    if result.returncode == 0:
        info("R script executed successfully.")
        if not Path(output_file).exists:
            error("R script returned 0, but output file was not created.")
    else:
        error(f"Error in executing R script: {result.stderr}")
        exit(1)

    # This is a hacky workaround! We terminate execution to avoid having
    # vantage6-algorithm-tools handle the writing of the output file.
    # See:
    # https://github.com/vantage6/vantage6/blob/version/4.2.2/vantage6-algorithm-tools/vantage6/algorithm/tools/wrap.py#L63-L69
    exit(0)
