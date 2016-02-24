# -*- coding: utf-8 -*-
"""
Functions related to plotting the collected data.
"""

import datetime
import comet.data as data
import comet.time as time
import comet.csvio as csvio


def plot(config, graph_type, group_by, sample_width, weekends_only,
         business_days_only, no_outliers, out_file=None, included_channels=None):
    """Plot the gathered data.
    """
    # We import plotly local to the function not to slow down the rest of the program,
    # for example printing the help text. Import plotly adds 1.4s to execution time.
    import plotly

    rows = csvio.loadAll(config)
    device_name = rows[0][1]
    channel_labels = data.get_labels(rows)
    rows = rows[data.get_first_data_point_index(rows):]
    if weekends_only:
        rows = data.filter_weekends(rows, True)
    if business_days_only:
        rows = data.filter_weekends(rows, False)
    if not rows:
        raise RuntimeError("After filtering the data for weekends or weekdays "
                           "there was no data left to plot.")

    if graph_type == 'scatter':
        columns = data.get_columns(rows)
        figure = construct_line_or_scatter(channel_labels, columns, included_channels,
                                           device_name, 'markers')
    elif graph_type == 'line':
        columns = data.get_columns(rows)
        figure = construct_line_or_scatter(channel_labels, columns, included_channels,
                                           device_name, 'line')
    elif graph_type == 'box':
        groups = data.group(rows, group_by, sample_width)
        groups = data.rotate_group_with_time_to_start(groups, datetime.time(3, 0))
        figure = construct_box(channel_labels, groups, group_by, included_channels,
                               device_name, no_outliers)

    if not out_file:
        out_file = graph_type + '-plot_grouped_by_' + group_by + '.html'
    plotly.offline.plot(figure, filename=out_file)


def construct_line_or_scatter(channel_labels, columns, included_channels, device_name,
                              mode_string):
    """Returns a plotly line or scatter plot figure ready for drawing."""
    import plotly

    traces = list()
    for i in range(4):
        if i+1 not in included_channels:
            continue
        if channel_labels[i+1] == 'CO2 level':
            group = 'y1'
        else:
            group = 'y2'
        traces.append(plotly.graph_objs.Scatter(
            x=columns[0],
            y=columns[i+1],
            name=channel_labels[i+1],
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


def construct_box(channel_labels, groups, group_by, included_channels, device_name,
                  no_outliers):
    """Returns a plotly box figure ready for drawing."""
    import plotly

    colors = ['hsl(' + str(h) + ',50%' + ',50%)' for h in linspace(0, 360, len(groups))]
    if group_by == 'day':
        labels = [':'.join(groups[i][0][0].split(' ')[0].split(':')[:2])
                  for i in range(len(groups))]
    elif group_by == 'week':
        labels = [time.dow_as_string(time.datetime_from_field(groups[i][0][0])) + ' ' +
                  ':'.join(groups[i][0][0].split(' ')[0].split(':')[:2])
                  for i in range(len(groups))]
    else:
        labels = [groups[i][0][0] for i in range(len(groups))]

    traces = [{'y': groups[i][included_channels[0]],
               'type': 'box',
               'name': labels[i],
               'jitter': 0.3,
               'marker': {'color': colors[i]},
           } for i in range(len(groups))]
    if no_outliers:
        for trace in traces:
            trace.update(boxpoints=False)

    layout = {'title': channel_labels[included_channels[0]] + ' data from ' + device_name,
              'xaxis': {'showgrid': False,
                        'zeroline': False,
                        'tickangle': 60,
                        'showticklabels': True,
                        'title': 'Time'},
              'yaxis': {'zeroline': True,
                        'gridcolor': 'white',
                        'title': 'Particles per million of CO2'},
              'paper_bgcolor': 'rgb(233,233,233)',
              'plot_bgcolor': 'rgb(233,233,233)',
              'showlegend': False }

    return plotly.graph_objs.Figure(data=traces, layout=layout)


def linspace(start, stop, n):
    """Generate a linear interpolation between start and stop with n steps."""
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i
