import sys

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


class PlotterHistogram:
    """
    Class that plot the histogram to check whether the data are balanced or not
    """

    def __init__(self, array):
        self.array = array

    def plot_data_balancing(self):
        """
        function that generate the balancing histogram and saves it in the graphs folder
        """
        x_labels = ['Normal', 'Attack']
        plt.bar(range(len(self.array)), self.array, align='center')
        plt.xticks(range(len(x_labels)), x_labels, size='small')

        # Save the figure
        plt.savefig("./graphs/Balancing_plot.png")

        # Suspension 'til evaluation completed
        sys.exit(0)


class PlotterRadarDiagram:
    """
    Class that plot the radar diagram needed for data quality check
    """

    def __init__(self, data_frame):
        self.data_frame = data_frame

    def plot_data_quality(self):
        """
        Function that generate the radar diagram needed to analyse the data goodness
        """
        new_df = pd.DataFrame(columns=['type', 'value'])

        for i in range(
                len(self.data_frame.axes[1])):
            # For each column take every value and pair with the column name
            column_name = self.data_frame.columns[i]
            for j in range(
                    len(self.data_frame.axes[0])):
                tmp = pd.DataFrame([[column_name,
                                     self.data_frame.iat[j, i]]],
                                   columns=['type', 'value'])
                new_df = pd.concat([new_df, tmp], axis=0)

        fig = px.scatter_polar(new_df, r='value', theta='type')
        fig.update_traces(fill='none')

        fig.write_image("graphs/radar_diagram.png", format='png', engine='kaleido')

        # Suspension 'til evaluation completed
        sys.exit(0)
