import sys

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def plot_data_quality(data_frame):
    """
    Method that generate the radar diagram needed to analyse the data goodness
    :param data_frame: data to plot
    """
    new_df = pd.DataFrame(columns=['type', 'value'])

    for i in range(len(data_frame.axes[1])):
        # For each column take every value and pair with the column name
        column_name = data_frame.columns[i]
        for j in range(len(data_frame.axes[0])):
            tmp = pd.DataFrame([[column_name, data_frame.iat[j, i]]], columns=['type', 'value'])
            new_df = pd.concat([new_df, tmp], axis=0)

    fig = px.scatter_polar(new_df, r='value', theta='type')
    fig.update_traces(fill='none')

    fig.write_image("graphs/radar_diagram.png", format='png', engine='kaleido')

    # Suspension 'til evaluation completed
    sys.exit(0)


def plot_data_balancing(array):
    """
    function that generate the balancing histogram and saves it in the graphs folder
    :param array: data needed to obtain the plot
    """
    x_labels = ['Normal', 'Attack']

    plt.bar(range(len(array)), array, align='center')
    plt.xticks(range(len(x_labels)), x_labels, size='small')

    # Save the figure
    plt.savefig("./graphs/Balancing_plot.png")

    # Suspension 'til evaluation completed
    sys.exit(0)
