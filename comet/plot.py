# -*- coding: utf-8 -*-
"""
Functions related to plotting the collected data.
"""


import comet.csvio as csvio


def plot(config, graph_type, group_by, excluded_channels=None):
    """Plot the gathered data.
    """
    # We import plotly local to the function not to slow down the rest of the program,
    # for example printing the help text. Import plotly adds 1.4s to execution time.
    import plotly

    data = csvio.loadAll(config)
    device_name = data[0][1]
    labels = csvio.get_labels(data)
    data = data[csvio.get_first_data_point_index(data):]
    columns = csvio.get_columns(data)

    if graph_type == 'scatter':
        figure = construct_line_or_scatter(labels, columns, excluded_channels, device_name, 'markers') 
    elif graph_type == 'line':
        figure = construct_line_or_scatter(labels, columns, excluded_channels, device_name, 'line') 
    elif graph_type == 'box':
        figure = construct_box(labels, columns)

    plotly.offline.plot(figure, filename=graph_type + '-plot_grouped_by_' +
                        group_by + '.html')



def construct_line_or_scatter(labels, columns, excluded_channels, device_name, mode_string):
    """Returns a plotly line or scatter plot figure ready for drawing."""
    import plotly

    traces = list()
    for i in range(4):
        if i+1 in excluded_channels:
            continue
        if labels[i+1] == 'CO2 level':
            group = 'y1'
        else:
            group = 'y2'
        traces.append(plotly.graph_objs.Scatter(
            x=columns[0],
            y=columns[i+1],
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

    return plotly.graph_objs.Figure(data=traces, layout=layout)


def construct_box(labels, columns, excluded_channels):
    pass
    
