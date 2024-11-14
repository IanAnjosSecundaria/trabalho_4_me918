import numpy as np
from numpy import random
from matplotlib import pyplot as plt


def t_test(sample1, sample2):
    # this is a t-test assuming equal sample sizes
    assert len(sample1) == len(sample2)
    difference = sample2.mean() - sample1.mean()
    n_1 = len(sample1)
    n_2 = len(sample2)
    mu_measure_var1 = sample1.var(ddof=1) / len(sample1)
    mu_measure_var2 = sample2.var(ddof=1) / len(sample2)
    mu_std_err = np.sqrt(mu_measure_var1 + mu_measure_var2)
    dof = mu_std_err**4 / (
        mu_measure_var1**2 / (n_1 - 1) + mu_measure_var2**2 / (n_2 - 1)
    )
    t_val = difference / mu_std_err
    t_null_dist = np.random.standard_t(dof, 100_000)
    p_val = np.mean(np.abs(t_val) > t_null_dist) / 2
    return f"""\
t-value: {t_val}
degrees of freedom: {dof}
p-value: {p_val}"""


def freqpoly(x1, x2, binwidth, xlim):
    all_data = np.concatenate([x1, x2])
    x_low = min([all_data.min(), xlim[0]])
    x_high = max([all_data.max(), xlim[1]])
    bins = np.arange(x_low, x_high + binwidth, binwidth)
    fig, ax = plt.subplots()
    ax.hist(x1, bins, density=True, range=xlim, alpha=0.5)
    ax.hist(x2, bins, density=True, range=xlim, alpha=0.5)
    return fig

# This app is translated from Mastering Shinywidgets
# https://mastering-shiny.org/basic-reactivity.html#reactive-expressions-1
from shiny import App, render, ui
from numpy import random

app_ui = ui.page_fluid(
    ui.row(
        ui.column(
            4,
            "Distribution 1",
            ui.input_numeric("n1", label="n", value=1000, min=1),
            ui.input_numeric("mean1", label="µ", value=0, step=0.1),
            ui.input_numeric("sd1", label="σ", value=0.5, min=0.1, step=0.1),
        ),
        ui.column(
            4,
            "Distribution 2",
            ui.input_numeric("n2", label="n", value=1000, min=1),
            ui.input_numeric("mean2", label="µ", value=0, step=0.1),
            ui.input_numeric("sd2", label="σ", value=0.5, min=0.1, step=0.1),
        ),
        ui.column(
            4,
            "Frequency polygon",
            ui.input_numeric("binwidth", label="Bin width", value=0.1, step=0.1),
            ui.input_slider("range", label="range", value=[-3, 3], min=-5, max=5),
        ),
    ),
    ui.row(
        ui.column(9, ui.output_plot("hist")),
        ui.column(3, ui.output_text_verbatim("ttest")),
    ),
)


def server(input, output, session):
    @output
    @render.plot
    def hist():
        print(input.range())
        x1 = random.normal(input.mean1(), input.sd1(), input.n1())
        x2 = random.normal(input.mean2(), input.sd2(), input.n2())
        return freqpoly(x1, x2, input.binwidth(), input.range())

    @output
    @render.text
    def ttest():
        x1 = random.normal(0, 1, 100)
        x2 = random.normal(0, 1, 100)
        return t_test(x1, x2)


app = App(app_ui, server)
