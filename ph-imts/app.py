from shiny.express import input, module, render, ui
from shinywidgets import render_widget
from data import df, df_all, df_yearly, df_month_year
import plotly.express as px

ui.page_opts(
    title="Philippine Total Trade, Imports, Exports, and Balance of Trade in Goods by Month and Year: 1991-2023",
    fillable=True,
    lang="en",
)

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

with ui.navset_card_pill(id="navset_current"):
    with ui.nav_panel("All"):
        with ui.layout_columns(fill=False, col_widths=[12, 12, 6, 6, 12]):
            cards_summary("cards_summary_all")
                
            with ui.card():
                with ui.card_header():
                    "Summary"
                "Put summary here"
            
            with ui.card(full_screen=True):
                with ui.card_header():
                    "Timeline"
                "Put line chart here"
                
            with ui.card(full_screen=True):
                with ui.card_header():
                    "Trade Composition"
                "Put pie chart here"
                
            with ui.card(full_screen=True):
                with ui.card_header():
                    "Data Table"
                "Put DataGrid chart here"
                    
    with ui.nav_panel("Yearly"):
        cards_summary("cards_summary_yearly")
        
    with ui.nav_panel("Monthly"):
        cards_summary("cards_summary_monthly")
