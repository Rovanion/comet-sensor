# -*- coding: utf-8 -*-
"""
Functions related to plotting the collected data.
"""


import comet.data as data
import comet.csvio as csvio


def plot(config, graph_type, group_by, excluded_channels=None):
    """Plot the gathered data.
    """
    # We import plotly local to the function not to slow down the rest of the program,
    # for example printing the help text. Import plotly adds 1.4s to execution time.
    import plotly

    rows = csvio.loadAll(config)
    device_name = rows[0][1]
    labels = data.get_labels(rows)
    rows = rows[data.get_first_data_point_index(rows):]

    if graph_type == 'scatter':
        columns = data.get_columns(rows)
        figure = construct_line_or_scatter(labels, columns, excluded_channels, device_name, 'markers')
    elif graph_type == 'line':
        columns = data.get_columns(rows)
        figure = construct_line_or_scatter(labels, columns, excluded_channels, device_name, 'line')
    elif graph_type == 'box':
        groups = data.group(rows, group_by)
        figure = construct_box(labels, groups, excluded_channels, device_name)

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


def construct_box(labels, groups, excluded_channels, device_name):
    """Returns a plotly box figure ready for drawing."""
    import plotly

    print(groups[0])

    color = ['hsl('+str(h)+',50%'+',50%)' for h in linspace(0, 360, len(groups))]
    data = [{'y': groups[i][0],
             'type': 'box',
             'marker': {'color': color[i]}
         } for i in range(len(groups))]
    layout = {'xaxis': {'showgrid': False, 'zeroline': False, 'tickangle': 60, 'showticklabels': False},
              'yaxis': {'zeroline': False, 'gridcolor': 'white'},
              'paper_bgcolor': 'rgb(233,233,233)',
              'plot_bgcolor': 'rgb(233,233,233)',
              'showlegend': False }

    return plotly.graph_objs.Figure(data=data, layout=layout)


def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i
