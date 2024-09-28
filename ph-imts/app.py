from data import *
from shared import initialize, format_currency
from shiny import reactive
from shiny.express import input, module, render, ui
from shinywidgets import render_widget
import plotly.express as px

ui.page_opts(
    title="Philippine Total Trade, Imports, Exports, and Balance of Trade in Goods by Month and Year: 1991-2023 (in million USD)",
    fillable=True,
    lang="en",
)

# Set locale so it can be used for formatting trade values
initialize()

def choose_value_box_theme(val):
    if val < 0:
        return "danger"
    else:
        return "success"

@module
def cards_summary(input, output, session, df):
    with ui.layout_columns(fill=False):
        # Exports
        with ui.value_box():
            "Exports"
            
            @render.express
            def exports():
                format_currency(df['exports'])

        # Imports
        with ui.value_box():
            "Imports"
            
            @render.express
            def imports():
                format_currency(df['imports'])

        # Balance of Trade
        with ui.value_box(theme=choose_value_box_theme(df['balance_of_trade'])):
            "Balance of Trade"
            
            @render.express
            def balance_of_trade():
                format_currency(df['balance_of_trade'])
                
        # Total TRade
        with ui.value_box():
            "Total Trade"
            
            @render.express
            def total():
                format_currency(df['total_trade'])

@module
def pie_chart(input, output, session, df, title):
    with ui.card(full_screen=True):
        with ui.card_header():
            title
        
        @render_widget
        def pie_chart():
            return px.pie(
                data_frame=df, 
                values='values', 
                names='type'
            )

@module
def data_grid(input, output, session, df, title):
    # Trade Data (DataGrid)
    with ui.card(full_screen=True):
        with ui.card_header():
            title
        
        @render.data_frame
        def datagrid():
            return render.DataGrid(df, selection_mode="rows")

def change_plotly_legend_position(fig):
    fig.update_layout(legend=dict(
                        yanchor="top",
                        y=0.97,
                        xanchor="left",
                        x=0.01
                    ))

with ui.navset_card_pill(id="navset_current"):
    with ui.nav_panel("All"):
        with ui.layout_columns(fill=False, col_widths=[12]):
            cards_summary("cards_summary_all", df_all)
            
            # Trade Values (Line charts)
            with ui.card(full_screen=True):
                chart_labels_values={
                    "values": "Trade Value (million USD)",
                    "type": "Type",
                    "date": "Trade Month & Year",
                    "total_trade": "Total Trade Value (million USD)",
                    "balance_of_trade": "Balance of Trade Value (million USD)",
                }
                
                with ui.card_header():
                    "Trade Values"
                
                ui.input_checkbox("checkbox_line_markers", "Show markers", False)
                
                @render_widget
                def line_chart_import_exports():
                    fig = px.line(
                        df_all_chart_import_exports,
                        x="date",
                        y="values",
                        markers=input.checkbox_line_markers(),
                        color='type',
                        title="Imports, Exports from 1991 to 2023",
                        labels=chart_labels_values
                    )
                    change_plotly_legend_position(fig)
                    return fig
                
                @render_widget
                def line_chart_total():
                    return px.line(
                        df,
                        x="date",
                        y="total_trade",
                        markers=input.checkbox_line_markers(),
                        title="Total Trade Value from 1991 to 2023",
                        labels=chart_labels_values
                    )
                
                @render_widget
                def line_chart_balance():
                    return px.line(
                        df,
                        x="date",
                        y="balance_of_trade",
                        markers=input.checkbox_line_markers(),
                        title="Balance of Trade Value from 1991 to 2023",
                        labels=chart_labels_values
                    )
                
            # Trade Values Growth Rates (Line charts)
            with ui.card(full_screen=True):
                chart_labels_growth_rates={
                    "values": "Trade Value Growth Rates (percentage)",
                    "type": "Type",
                    "date": "Trade Month & Year",
                    "total_trade_growth_rate": "Total Trade Value Growth Rates (percentage)",
                    "balance_of_trade_growth_rate": "Balance of Trade Value Growth Rates (percentage)",
                }
                
                with ui.card_header():
                    "Trade Values Growth Rates"
                
                ui.input_checkbox("checkbox_line_growth_rates_markers", "Show markers", False)
                        
                @render_widget
                def line_chart_import_exports_growth_rate():
                    fig = px.line(
                        df_all_chart_import_exports_growth_rate,
                        x="date",
                        y="values",
                        markers=input.checkbox_line_growth_rates_markers(),
                        color='type',
                        title="Imports, Exports Growth Rates from 1991 to 2023",
                        labels=chart_labels_growth_rates
                    )
                    change_plotly_legend_position(fig)
                    return fig
                
                @render_widget
                def line_chart_total_growth_rate():
                    return px.line(
                        df,
                        x="date",
                        y="total_trade_growth_rate",
                        markers=input.checkbox_line_growth_rates_markers(),
                        title="Total Trade Value Growth Rates from 1991 to 2023",
                        labels=chart_labels_growth_rates
                    )
                
                @render_widget
                def line_chart_balance_growth_rate():
                    return px.line(
                        df,
                        x="date",
                        y="balance_of_trade_growth_rate",
                        markers=input.checkbox_line_growth_rates_markers(),
                        title="Balance of Trade Value Growth Rates from 1991 to 2023",
                        labels=chart_labels_growth_rates
                    )
                
            pie_chart("pie_chart_all", df_all_chart_import_exports, "Trade Composition")
            data_grid("data_grid_all", df, "Trade Data")
                    
    with ui.nav_panel("Yearly"):
        with ui.layout_columns(fill=False, col_widths=[12]):
            cards_summary("cards_summary_yearly", df_all)
            
            # TODO: Trade Values (Line charts)
            # TODO: Trade Values Growth Rates (Line charts)
            
            pie_chart("pie_chart_yearly", df_all_chart_import_exports, "Trade Composition")
            data_grid("data_grid_yearly", df_yearly_datagrid, "Trade Data")
        
    with ui.nav_panel("Monthly"):
        # TODO: Get year data from input
        with ui.layout_columns(fill=False, col_widths=[12]):
            ui.input_selectize(
                id="selectize_monthly_year",
                label="Select year",
                choices={x: x for x in range(1991, 2024)}
            )
            
            @reactive.calc
            def df_monthly_year():
                year = int(input.selectize_monthly_year())
                return df_yearly.loc[year]
            
            # TODO: Make this reactive based on selectize input
            # https://shiny.posit.co/py/docs/module-communication.html#passing-reactives-to-modules
            cards_summary("cards_summary_monthly_year", df_yearly.loc[1991])
