from dash import Dash, Input, Output, dcc, html
import pandas as pd
from project.dashapp.layout1 import layout1
import dash_leaflet as dl

data = (
    pd.read_csv(r"C:\Users\Tausif shaikh\Downloads\flask_authentication\project\dashapp\walmart_clean_data.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

stores = data["Store"].sort_values().unique()
departments = data["Dept"].sort_values().unique()
holiday = data["IsHoliday"].unique()

data1=data.groupby(["latitude","longitude","name"], as_index=False).agg(
    
    avg_weekly_sales = ("Weekly_Sales", "mean"),
    max_weekly_sales = ("Weekly_Sales", "max")
)

markers = [dl.Marker(children=[dl.Popup(children=["{name} ({lon}, {lat})".format(name=row["name"], lon=row["longitude"], lat=row["latitude"])])], 
position=(row["latitude"], row["longitude"])) for i, row in data1.iterrows()]

title = "Walmart Analytics: Understand the sales!"

layout = html.Div( 
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
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Store", className="menu-title"),
                        dcc.Dropdown(
                            id="Store-filter",
                            options=[
                                {"label": store, "value": store}
                                for store in stores
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Department", className="menu-title"),
                        dcc.Dropdown(
                            id="dept-filter",
                            options=[
                                {
                                    "label": dept,
                                    "value": dept,
                                }
                                for dept in departments
                            ],
                            value=1,
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Holiday", className="menu-title"),
                        dcc.Dropdown(
                            id="holiday-filter",
                            options=[
                                {
                                    "label": "Holiday",
                                    "value": True,
                                },
                                {
                                    "label": "Non-Holiday",
                                    "value": False,
                                },
                                {
                                    "label": "No-Filter",
                                    "value": "None",
                                }
                            ],
                            value=False,
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Date"].min().date(),
                            max_date_allowed=data["Date"].max().date(),
                            start_date=data["Date"].min().date(),
                            end_date=data["Date"].max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="weekly_sales-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div([
                dl.Map(children=[dl.TileLayer(url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")] + markers,
                    style={'width': "100%", 'height': "100%"}, center=[42.46902, -88.064689], zoom=7),
            ], style={"position": "relative", 'width': '1000px', 'height': '500px','left': '50%',
                    'transform': 'translateX(-50%)'},
            className="card",),
    ],
    
)