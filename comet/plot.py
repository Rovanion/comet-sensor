# -*- coding: utf-8 -*-
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
    device_name = data[0][1]
    labels = csvio.get_labels(data)
    data = data[csvio.get_first_data_point_index(data):]
    dates = [line[0] for line in data]
    columns = list()
    for i in range(4):
        columns.append([line[i+1] for line in data])

    if graph_type == 'scatter':
        mode_string = 'markers'
    else:
        mode_string = 'line'

    traces = list()
    for i in range(4):
        if labels[i+1] == 'CO2 level':
            group = 'y1'
        else:
            group = 'y2'
        traces.append(plotly.graph_objs.Scatter(
            x=dates,
            y=columns[i],
            name=labels[i+1],
            mode=mode_string,
            yaxis=group
        ))

    layout = plotly.graph_objs.Layout(
        title='Sensor data from ' + device_name,
        yaxis=dict(
            title='Particles per million of CO2'
        ),
        yaxis2=dict(
            title='Temperature °C',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        )
    )

    figure = plotly.graph_objs.Figure(data=traces, layout=layout)
    plotly.offline.plot(figure, filename=graph_type + '-plot_grouped_by_' +
                        group_by + '.html')
