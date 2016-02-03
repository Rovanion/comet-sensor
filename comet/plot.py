"""
Functions related to plotting the collected data.
"""


import comet.csvio as csvio


def plot(config, graph_type, group_by):
    """Plot the gathered data.
    """
    # We import plotly local to the function not to slow down the rest of the program,
    # for example printing the help. Import plotly adds 1.4s to execution time.
    import plotly

    data = csvio.loadAll(config)
    labels = csvio.get_labels(data)
    data = data[csvio.get_first_data_point_index(data):]
    dates = [line[0] for line in data]
    temperatures = [line[1] for line in data]
    carbon_dioxide_values = [line[4] for line in data]

    if graph_type == 'scatter':
        mode_string = 'markers'
    else:
        mode_string = 'line'
    trace = [plotly.graph_objs.Scatter(
        x = dates,
        y = carbon_dioxide_values,
        mode = mode_string
    )]

    plotly.offline.plot(trace, filename=graph_type + '-plot_grouped_by_' + group_by + '.html')
