from vantage6.algorithm.tools.util import info
from vantage6.algorithm.tools.decorators import data

import pandas as pd
import json
from pathlib import Path

# high-level interface
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
# low-level interface
import rpy2.rinterface as rinterface

@data(1)
def partial_average_rpy2(pd_df: pd.DataFrame, column_name: str):
    """Compute the average partial

    The data argument contains a pandas-dataframe containing the local
    data from the node.
    """
    # R script filename that will actually compute the average
    R_SCRIPT_FILENAME = 'average_rpy2.R'

    # We will feed an R dataframe to the script, so we must convert our pandas
    # dataframe (loaded from the csv via vantage6-algorithn-tools's @data
    # decorator) first
    info('Converting pandas dataframe to R dataframe')
    with (ro.default_converter + pandas2ri.converter).context():
        r_from_pd_df = ro.conversion.get_conversion().py2rpy(pd_df)


    # Read into memory actual R script
    current_dir = Path(__file__).parent
    with open(current_dir / R_SCRIPT_FILENAME, 'r') as file:
        r_script_content = file.read()

    # Within the namespace of the R script, we set some variables. This is the
    # way we pass input into the R script.
    info('Setting variables in R')
    ro.globalenv['pyin_column_name'] = column_name
    ro.globalenv['pyin_df'] = r_from_pd_df

    # Actually execute R script
    info('Executing R script')
    ro.r(r_script_content)

    # We want to extract the R dataframe into python. We convert it to panda's.
    info('Converting R dataframe to pandas dataframe')
    df_from_r = ro.r['pyout_result']
    with (ro.default_converter + ro.pandas2ri.converter).context():
        pd_from_r_df = ro.conversion.get_conversion().rpy2py(df_from_r)


    # vantage6-algorithm-tools python wrapper's @data decorator (used for this
    # function) will call json.dumps() on whatever we return from this
    # function.  As a hacky temporary workaround, we must convert our dataframe
    # with results to a dictionary -- which is an object json.dumps() will be
    # able to take in (serializable)
    json_str = pd_from_r_df.to_json(orient='records')
    # When converting to 'records' we get a list. But v6-average-py expects
    # just a dict
    return json.loads(json_str)[0]
