from shiny import render, ui
from shiny.express import input
from shinywidgets import render_widget
from data import df
import plotly.express as px

ui.panel_title("Hello Shiny!")
ui.input_slider("n", "N", 0, 100, 20)

@render_widget
def plot():
    fig = px.line(df, x='year_month', y=['imports', 'exports'])
    return fig
