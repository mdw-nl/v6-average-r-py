import pandas as pd

from vantage6.algorithm.tools.util import info
from vantage6.algorithm.client import AlgorithmClient
from vantage6.algorithm.tools.decorators import algorithm_client, data

# high-level interface
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
# low-level interface
import rpy2.rinterface as rinterface


import json
from pathlib import Path

@algorithm_client
def central_average(client: AlgorithmClient, column_name: str):
    """Combine partials to global model

    First we collect the parties that participate in the collaboration.
    Then we send a task to all the parties to compute their partial (the
    row count and the column sum). Then we wait for the results to be
    ready. Finally when the results are ready, we combine them to a
    global average.

    Note that the master method also receives the (local) data of the
    node. In most use cases this data argument is not used.

    The client, provided in the first argument, gives an interface to
    the central server. This is needed to create tasks (for the partial
    results) and collect their results later on. Note that this client
    is a different client than the client you use as a user.
    """
    # Info messages can help you when an algorithm crashes. These info
    # messages are stored in a log file which is send to the server when
    # either a task finished or crashes.
    info('Collecting participating organizations')

    # Collect all organization that participate in this collaboration.
    # These organizations will receive the task to compute the partial.
    organizations = client.organization.list()
    ids = [organization.get("id") for organization in organizations]

    # Request all participating parties to compute their partial. This
    # will create a new task at the central server for them to pick up.
    # We've used a kwarg but is is also possible to use `args`. Although
    # we prefer kwargs as it is clearer.
    info('Requesting partial computation')
    task = client.task.create(
        input_={
            'method': 'partial_average',
            'kwargs': {
                'column_name': column_name
            }
        },
        organizations=ids
    )

    # Now we need to wait until all organizations(/nodes) finished
    # their partial. We do this by polling the server for results. It is
    # also possible to subscribe to a websocket channel to get status
    # updates.
    info("Waiting for results")
    results = client.wait_for_results(task_id=task.get("id"))
    info("Partial results are in!")

    # Now we can combine the partials to a global average.
    info("Computing global average")
    global_sum = 0
    global_count = 0
    for output in results:
        global_sum += output["sum"]
        global_count += output["count"]

    return {"average": global_sum / global_count}


@data(1)
def partial_average(pd_df: pd.DataFrame, column_name: str):
    """Compute the average partial

    The data argument contains a pandas-dataframe containing the local
    data from the node.
    """
    info('Converting pandas dataframe to R dataframe')
    with (ro.default_converter + pandas2ri.converter).context():
        r_from_pd_df = ro.conversion.get_conversion().py2rpy(pd_df)


    current_dir = Path(__file__).parent
    with open(current_dir / 'average.R', 'r') as file:
        r_script_content = file.read()

    info('Setting variables in R')
    ro.globalenv['pyin_column_name'] = column_name
    ro.globalenv['pyin_df'] = r_from_pd_df

    # execute R script
    info('Executing R script')
    ro.r(r_script_content)

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
