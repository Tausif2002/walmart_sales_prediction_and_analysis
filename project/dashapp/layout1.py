from dash import Dash, Input, Output, dcc, html
import pandas as pd


data = (
    pd.read_csv(r"C:\Users\Tausif shaikh\Downloads\flask_authentication\project\dashapp\walmart_eda.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)
stores = data["Store"].sort_values().unique()
departments = data["Dept"].sort_values().unique()
holiday = data["IsHoliday"].unique()

layout1 = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Walmart Analytics", className="header-title"
                ),
                html.P(
                    children=(
                        "analayze the weekly sales of walemart"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),  
    ],
    
)