from data import *
from shared import initialize, format_currency
from shiny import reactive
from shiny.express import input, module, render, ui
from shinywidgets import render_widget
import plotly.express as px
import pandas as pd

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
def pie_chart(input, output, session, df):
    with ui.card(full_screen=True):
        with ui.card_header():
            "Trade Composition"
        
        @render_widget
        def pie_chart():
            return px.pie(
                data_frame=df, 
                values='values', 
                names='type'
            )

@module
def data_grid(input, output, session, df, title):
    with ui.card(full_screen=True):
        with ui.card_header():
            title
        
        @render.data_frame
        def datagrid():
            return render.DataGrid(df, selection_mode="rows")
      
def create_line_chart_imports_exports(df, markers, x, title, labels):
    fig = px.line(
            df,
            x=x,
            y="values",
            markers=markers,
            color='type',
            title=title,
            labels=labels
        ).update_layout(legend=dict(
            yanchor="top",
            y=0.97,
            xanchor="left",
            x=0.01
        ))
    return fig

with ui.sidebar(position="right"):  
    ui.input_checkbox("checkbox_show_line_chart_markers", "Show markers", False)

with ui.navset_card_pill(id="navset_current"):
    with ui.nav_panel("All"):
        with ui.layout_columns(fill=False, col_widths=[12]):
            cards_summary("cards_summary_all", df_all)
            
            # Trade Values (Line charts)
            with ui.card(full_screen=True):
                line_chart_all_labels={
                    "values": "Trade Value (million USD)",
                    "type": "Type",
                    "date": "Trade Month & Year",
                    "total_trade": "Total Trade Value (million USD)",
                    "balance_of_trade": "Balance of Trade Value (million USD)",
                }
                
                with ui.card_header():
                    "Trade Values"
                
                @render_widget
                def line_chart_all_import_exports():
                    fig = create_line_chart_imports_exports(
                        df=df_all_chart_import_exports,
                        markers=input.checkbox_show_line_chart_markers(),
                        x="date",
                        title="Imports, Exports from 1991 to 2023",
                        labels=line_chart_all_labels
                    )
                    return fig
                
                @render_widget
                def line_chart_all_total():
                    return px.line(
                        df,
                        x="date",
                        y="total_trade",
                        markers=input.checkbox_show_line_chart_markers(),
                        title="Total Trade Value from 1991 to 2023",
                        labels=line_chart_all_labels
                    )
                
                @render_widget
                def line_chart_all_balance():
                    return px.line(
                        df,
                        x="date",
                        y="balance_of_trade",
                        markers=input.checkbox_show_line_chart_markers(),
                        title="Balance of Trade Value from 1991 to 2023",
                        labels=line_chart_all_labels
                    )
                
            # Trade Values Growth Rates (Line charts)
            with ui.card(full_screen=True):
                line_chart_all_labels_growth_rates={
                    "values": "Trade Value Growth Rates (percentage)",
                    "type": "Type",
                    "date": "Trade Month & Year",
                    "total_trade_growth_rate": "Total Trade Value Growth Rates (percentage)",
                    "balance_of_trade_growth_rate": "Balance of Trade Value Growth Rates (percentage)",
                }
                
                with ui.card_header():
                    "Trade Values Growth Rates"
                        
                @render_widget
                def line_chart_all_import_exports_growth_rate():
                    fig = create_line_chart_imports_exports(
                        df=df_all_chart_import_exports_growth_rate,
                        markers=input.checkbox_show_line_chart_markers(),
                        x="date",
                        title="Imports, Exports Growth Rates from 1991 to 2023",
                        labels=line_chart_all_labels_growth_rates
                    )
                    return fig
                
                @render_widget
                def line_chart_all_total_growth_rate():
                    return px.line(
                        df,
                        x="date",
                        y="total_trade_growth_rate",
                        markers=input.checkbox_show_line_chart_markers(),
                        title="Total Trade Value Growth Rates from 1991 to 2023",
                        labels=line_chart_all_labels_growth_rates
                    )
                
                @render_widget
                def line_chart_all_balance_growth_rate():
                    return px.line(
                        df,
                        x="date",
                        y="balance_of_trade_growth_rate",
                        markers=input.checkbox_show_line_chart_markers(),
                        title="Balance of Trade Value Growth Rates from 1991 to 2023",
                        labels=line_chart_all_labels_growth_rates
                    )
                
            pie_chart("pie_chart_all", df_all_chart_import_exports)
            data_grid("data_grid_all", df, "Trade Data")
                    
    with ui.nav_panel("Yearly"):
        with ui.layout_columns(fill=False, col_widths=[12]):
            cards_summary("cards_summary_yearly", df_all)
            
            # Trade Values (Line charts)
            with ui.card(full_screen=True):
                line_chart_yearly_labels={
                    "values": "Trade Value (million USD)",
                    "type": "Type",
                    "year": "Trade Year",
                    "total_trade": "Total Trade Value (million USD)",
                    "balance_of_trade": "Balance of Trade Value (million USD)",
                }
                
                with ui.card_header():
                    "Trade Values"
                
                @render_widget
                def line_chart_yearly_import_exports():
                    fig = create_line_chart_imports_exports(
                        df=df_yearly_chart_import_exports,
                        markers=input.checkbox_show_line_chart_markers(),
                        x=df_yearly_chart_import_exports.index,
                        title="Imports, Exports from 1991 to 2023",
                        labels=line_chart_yearly_labels
                    )
                    return fig
                
                @render_widget
                def line_chart_yearly_total():
                    return px.line(
                        df_yearly,
                        x=df_yearly.index,
                        y="total_trade",
                        markers=input.checkbox_show_line_chart_markers(),
                        title="Total Trade Value from 1991 to 2023",
                        labels=line_chart_yearly_labels
                    )
                
                @render_widget
                def line_chart_yearly_balance():
                    return px.line(
                        df_yearly,
                        x=df_yearly.index,
                        y="balance_of_trade",
                        markers=input.checkbox_show_line_chart_markers(),
                        title="Balance of Trade Value from 1991 to 2023",
                        labels=line_chart_yearly_labels
                    )
              
            # Trade Values Growth Rates (Line charts)
            with ui.card(full_screen=True):
                line_chart_yearly_labels_growth_rates={
                    "values": "Trade Value Growth Rates (percentage)",
                    "type": "Type",
                    "year": "Trade Year",
                    "total_trade_growth_rate": "Total Trade Value Growth Rates (percentage)",
                    "balance_of_trade_growth_rate": "Balance of Trade Value Growth Rates (percentage)",
                }
                
                with ui.card_header():
                    "Trade Values Growth Rates"
                        
                @render_widget
                def line_chart_yearly_import_exports_growth_rate():
                    fig = create_line_chart_imports_exports(
                        df=df_yearly_chart_import_exports_growth_rate,
                        markers=input.checkbox_show_line_chart_markers(),
                        x=df_yearly_chart_import_exports_growth_rate.index,
                        title="Imports, Exports Growth Rates from 1991 to 2023",
                        labels=line_chart_yearly_labels_growth_rates
                    )
                    return fig
                
                @render_widget
                def line_chart_yearly_total_growth_rate():
                    return px.line(
                        df_yearly,
                        x=df_yearly.index,
                        y="total_trade_growth_rate",
                        markers=input.checkbox_show_line_chart_markers(),
                        title="Total Trade Value Growth Rates from 1991 to 2023",
                        labels=line_chart_yearly_labels_growth_rates
                    )
                
                @render_widget
                def line_chart_yearly_balance_growth_rate():
                    return px.line(
                        df_yearly,
                        x=df_yearly.index,
                        y="balance_of_trade_growth_rate",
                        markers=input.checkbox_show_line_chart_markers(),
                        title="Balance of Trade Value Growth Rates from 1991 to 2023",
                        labels=line_chart_yearly_labels_growth_rates
                    )
            
            pie_chart("pie_chart_yearly", df_yearly_chart_import_exports)
            data_grid("data_grid_yearly", df_yearly_datagrid, "Trade Data")
        
    with ui.nav_panel("Monthly"):
        with ui.layout_columns(fill=False, col_widths=[12]):
            ui.input_selectize(
                id="selectize_monthly_year",
                label="Select year",
                choices={x: x for x in range(1991, 2024)}
            )
            
            year_input = reactive.value(1991)
            
            @reactive.effect
            @reactive.event(input.selectize_monthly_year)
            def _():
                year_input.set(int(input.selectize_monthly_year()))
            
            @reactive.calc
            def choose_summary_data():
                year = int(input.selectize_monthly_year())
                return df_yearly.loc[year]
            
            @reactive.calc
            def choose_trade_values():
                year = int(input.selectize_monthly_year())
                return df_monthly_group.get_group(year)
            
            @reactive.calc
            def choose_imports_exports_data():
                year = int(input.selectize_monthly_year())
                monthly_df = df_monthly_group.get_group(year)
                monthly_df_imports_exports = pd.concat([
                    categorize_col_vals(monthly_df, "exports", "Exports"),
                    categorize_col_vals(monthly_df, "imports", "Imports")
                ])
                return monthly_df_imports_exports
            
            with ui.layout_columns(fill=False, col_widths=[12]):
                # Summary
                with ui.layout_columns(fill=False):
                    # Exports
                    with ui.value_box():
                        "Exports"
                        
                        @render.express
                        def exports():
                            format_currency(choose_summary_data()['exports'])

                    # Imports
                    with ui.value_box():
                        "Imports"
                        
                        @render.express
                        def imports():
                            format_currency(choose_summary_data()['imports'])

                    # Balance of Trade
                    with ui.value_box():
                        "Balance of Trade"
                        
                        @render.express
                        def balance_of_trade():
                            format_currency(choose_summary_data()['balance_of_trade'])
                            
                    # Total Trade
                    with ui.value_box():
                        "Total Trade"
                        
                        @render.express
                        def total():
                            format_currency(choose_summary_data()['total_trade'])

                # TODO: Trade Values Growth Rates (Line charts)
                
                
                # TODO: Trade Values Growth Rates (Line charts)
                
                
                # Pie chart
                with ui.card(full_screen=True):
                    with ui.card_header():
                        "Trade Composition"
                    
                    @render_widget
                    def pie_chart():
                        return px.pie(
                            data_frame=choose_imports_exports_data(), 
                            values='values', 
                            names='type'
                        )

                # Data Grid
                with ui.card(full_screen=True):
                    with ui.card_header():
                        "Trade Data"
                    
                    @render.data_frame
                    def datagrid():
                        return render.DataGrid(pd.DataFrame(choose_trade_values()), selection_mode="rows")