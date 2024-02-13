import pandas as pd

from vantage6.algorithm.tools.util import info, error
from vantage6.algorithm.client import AlgorithmClient
from vantage6.algorithm.tools.decorators import algorithm_client

@algorithm_client
def central_average(client: AlgorithmClient, column_name: str, partial_method: str = 'partial_average_rpy2'):
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

    # check user input
    avail_methods = {
        'partial_average_r',
        'partial_average_rpy2',
        'partial_average_original'
    }
    if not partial_method in avail_methods:
        error("Unrecognized partial average method")
        exit(1)

    # Request all participating parties to compute their partial. This
    # will create a new task at the central server for them to pick up.
    # We've used a kwarg but is is also possible to use `args`. Although
    # we prefer kwargs as it is clearer.
    info('Requesting partial computation')
    task = client.task.create(
        input_={
            'method': partial_method,
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
