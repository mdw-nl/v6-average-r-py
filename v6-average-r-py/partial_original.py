import pandas as pd

from vantage6.algorithm.tools.util import info
from vantage6.algorithm.tools.decorators import data

# This is the original python partial_average function:
# See: https://github.com/IKNL/v6-average-py/blob/5cad1742749de0f5c05a788c8ce3ca5b0a3965b2/v6-average-py/__init__.py#L70-L90
@data(1)
def partial_average(df: pd.DataFrame, column_name: str):
    """Compute the average partial

    The data argument contains a pandas-dataframe containing the local
    data from the node.
    """
    # extract the column_name from the dataframe.
    info(f'Extracting column {column_name}')
    numbers = df[column_name]

    # compute the sum, and count number of rows
    info('Computing partials')
    local_sum = float(numbers.sum())
    local_count = len(numbers)

    # return the values as a dict
    return {
        "sum": local_sum,
        "count": local_count
    }
