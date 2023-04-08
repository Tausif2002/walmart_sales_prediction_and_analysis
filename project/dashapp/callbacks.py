from datetime import datetime as dt
from dash import Dash, Input, Output, State
import pandas_datareader as  pdr
from flask_login import current_user
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

data = (
    pd.read_csv(r"C:\Users\Tausif shaikh\Downloads\flask_authentication\project\dashapp\walmart_clean_data.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

def register_callbacks(dashapp):
    @dashapp.callback(
    Output("weekly_sales-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("Store-filter", "value"),
    Input("dept-filter", "value"),
    Input("holiday-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
    )
    def update_charts(store, dept,holiday, start_date, end_date):
        filtered_data = data.query(
            "Store== @store and Dept == @dept"
            " and Date >= @start_date and Date <= @end_date"
        )
        if holiday!="None":
            filtered_data = data.query(
            "Store== @store and Dept == @dept and IsHoliday==@holiday"
            " and Date >= @start_date and Date <= @end_date"
        )
        price_chart_figure = {
            "data": [
                {
                    "x": filtered_data["Date"],
                    "y": filtered_data["Weekly_Sales"],
                    "type": "lines",
                    # "hovertemplate": "$%{y:.2f}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Weekly sale of walmart",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"tickprefix": "$", "fixedrange": True},
                "colorway": ["#17B897"],
            },
        }


        price_chart_figure_bar = {
            "data": [
                {
                    "x": filtered_data["Date"],
                    "y": filtered_data["Weekly_Sales"],
                    "type": "bar",
                    # "hovertemplate": "$%{y:.2f}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Weekly sale of walmart",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"tickprefix": "$", "fixedrange": True},
                "colorway": ["#17B897"],
            },
        }


   
        return price_chart_figure ,price_chart_figure_bar