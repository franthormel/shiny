from shiny.express import input, module, render, ui
from shinywidgets import render_widget
from data import df, df_all, df_yearly, df_month_year
import plotly.express as px

ui.panel_title("Philippine Total Trade, Imports, Exports, and Balance of Trade in Goods by Month and Year: 1991-2023")

@module
def cards_summary(input, output, session):
    with ui.layout_columns(fill=False):
        with ui.value_box():
            "Exports"
            
            @render.express
            def exports():
                df_all['exports']

        with ui.value_box():
            "Imports"
            
            @render.express
            def imports():
                df_all['imports']

        with ui.value_box():
            "Balance of Trade"
            
            @render.express
            def bot():
                df_all['botg']
                
        with ui.value_box():
            "Total Trade"
            
            @render.express
            def total():
                df_all['total_trade']

with ui.sidebar(position="right"):
    "Sidebar"
    
with ui.navset_card_pill(id="navset_current"):
    with ui.nav_panel("All"):
        cards_summary("cards_summary_all")
                    
    with ui.nav_panel("Yearly"):
        cards_summary("cards_summary_yearly")
        
    with ui.nav_panel("Monthly"):
        "Monthly"
