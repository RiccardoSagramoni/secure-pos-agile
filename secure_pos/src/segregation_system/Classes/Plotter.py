import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


class Plotter:
    """
    Class that generate the plots needed for the data goodness evaluation
    """

    def __init__(self):
        self.n_features = 13

    def plot_data_balancing(self, array):
        """
        function that generate the balancing histogram and saves it in the graphs folder
        :param array: data needed to obtain the plot
        :return: none
        """
        x_labels = ['Normal', 'Attack']

        plt.bar(range(len(array)), array, align='center')
        plt.xticks(range(len(x_labels)), x_labels, size='small')

        # Save the figure
        plt.savefig("./graphs/Balancing_plot.png")

    def plot_data_quality(self, df):
        return
    # df = pd.DataFrame(data=df)

    # fig = px.scatter_polar(df, r='value', theta='Feature_name')
    # fig.update_traces(fill='none')
    # fig.show()
    # return
