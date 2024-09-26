from data import df, df_all, df_year, df_chart_all_import_exports
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

initialize()

@module
def cards_summary(input, output, session, df):
    with ui.layout_columns(fill=False):
        with ui.value_box():
            "Exports"
            
            @render.express
            def exports():
                format_currency(df['exports'])

        with ui.value_box():
            "Imports"
            
            @render.express
            def imports():
                format_currency(df['imports'])

        with ui.value_box():
            "Balance of Trade"
            
            @render.express
            def balance_of_trade():
                format_currency(df['balance_of_trade'])
                
        with ui.value_box():
            "Total Trade"
            
            @render.express
            def total():
                format_currency(df['total_trade'])

with ui.navset_card_pill(id="navset_current"):
    with ui.nav_panel("All"):
        with ui.layout_columns(fill=False, col_widths=[12, 12, 6, 6, 12]):
            cards_summary("cards_summary_all", df_all)
                
            
            with ui.card(full_screen=True):
                with ui.card_header():
                    "Trade Values"
                
                ui.input_checkbox("checkbox_line_markers", "Show markers", False)
                
                # TODO: Add charts for growth rates                    
                @render_widget
                def line_chart_import_exports():
                    fig = px.line(
                        df_chart_all_import_exports,
                        x="date",
                        y="values",
                        markers=input.checkbox_line_markers(),
                        color='type',
                        title="Philippines Imports, Exports from 1991 to 2023",
                        labels={
                            "values": "Trade Value (million USD)",
                            "type": "Type",
                            "date": "Trade Month & Year",
                        }
                    )
                    fig.update_layout(legend=dict(
                        yanchor="top",
                        y=0.97,
                        xanchor="left",
                        x=0.01
                    ))
                    return fig
                
                @render_widget
                def line_chart_balance():
                    return px.line(
                        df,
                        x="date",
                        y="balance_of_trade",
                        markers=input.checkbox_line_markers(),
                        title="Philippines Balance of Trade Value from 1991 to 2023",
                        labels={
                            "balance_of_trade": "Balance of Trade Value (million USD)",
                            "date": "Trade Month & Year",
                        }
                    )
                
                @render_widget
                def line_chart_total():
                    return px.line(
                        df,
                        x="date",
                        y="total_trade",
                        markers=input.checkbox_line_markers(),
                        title="Philippines Total Trade Value from 1991 to 2023",
                        labels={
                            "total_trade": "Total Trade Value (million USD)",
                            "date": "Trade Month & Year",
                        }
                    )
                
            with ui.card():
                with ui.card_header():
                    "Summary"
                # TODO: Add                    
                "Put summary here"
                
            with ui.card(full_screen=True):
                with ui.card_header():
                    "Trade Composition"
                
                @render_widget
                def pie_chart():
                    return px.pie(data_frame=df_chart_all_import_exports, values='values', names='type')
                
            with ui.card(full_screen=True):
                with ui.card_header():
                    "Trade Data"
                
                @render.data_frame
                def datagrid():
                    return render.DataGrid(df, selection_mode="rows")
                    
    with ui.nav_panel("Yearly"):
        cards_summary("cards_summary_yearly", df_all)
        
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
                return df_year.loc[year]
            
            # TODO: Make this reactive based on selectize input
            # https://shiny.posit.co/py/docs/module-communication.html#passing-reactives-to-modules
            cards_summary("cards_summary_monthly_year", df_year.loc[1991])
