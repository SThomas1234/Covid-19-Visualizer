import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
import functions
from urllib.request import urlopen
import requests, json
import numpy as np

import dash 
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output



covid_requests = requests.get("https://finnhub.io/api/v1/covid19/us?token=btcrspf48v6s23u166pg")
json_data = covid_requests.json()
df = pd.DataFrame(json_data)
df = df.drop(df.index[47])
df = df[:52]

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'
df2 = pd.read_csv(url, error_bad_lines=False, dtype={"fips":str})
df2 = df2[df2.county != 'Unknown'] # error for missouri

df2['fips'].replace('', np.nan, inplace=True)
df2.dropna(subset=['fips'], inplace=True)

url2 = requests.get('https://api.covidtracking.com/v1/states/current.json')
json_data_2 = url2.json()
df3 = pd.DataFrame(json_data_2)

val = df3['date'][2]
df3 = df3[df3.date == val]

url3 = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
df4 = pd.read_csv(url3, error_bad_lines=False)

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

state_names = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

state_codes = ["NY", "NJ", "CA", "MI", "FL", "MA", "WA", "LA", "IL", "PA", "GA", 
          "TX", "CO", "CT", "OH", "IN", "TN", "MD", "NC", "WI", "AZ", 
          "VA", "MO", "NV", "AL", "MS", "SC", "UT", "MN", "OR", "OK", 
          "AR", "IA", "DC", "KY", "ID", "RI", "KS", "NH", "ME", "VT", 
          "NM", "DE", "PR", "HI", "MT", "NE", "WV", "ND", "AK", "WY", "SD"]

df['state code'] = state_codes          

options = ["Choropleth of All U.S. States", "Choropleth of All U.S. Counties"]

options_dropdown_2 = ['Hospitalization Statistics', 
'ICU admission Statistics', 
'Ventilator Statistics',
'Recovery Statistics']     


app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://codepen.io/chriddyp/pen/brPBPO.css"])
server = app.server
app.layout = html.Div([
    html.H1(html.B("COVID-19 Tracker"), style={"text-align":"center"}),
    dbc.Row([
        dbc.Col(html.Div([
            html.Center(html.Big(dcc.Markdown("""
            This dropdown generates a live choropleth map highlighting COVID-19 cases and deaths across the U.S.
            Please select if you would like the map to display all U.S. states or all U.S. counties.
            """))),
            dcc.Dropdown(
                id = 'slct_option',
                options = [{"label":i, "value":i} for i in options],
                value = options[0],
                searchable = True,
                clearable = False
                ),

            html.Br(),

            dcc.Interval(
                id='my_interval',
                disabled=False,
                interval = 3*12000,
                n_intervals = 0,
                max_intervals = -1
                ),
            
            dcc.Graph(id='live_covid_map', style = {"margin-left": "auto",
            "margin-right": "auto"}, figure={}),
            ])
        ),
   
]),
    dbc.Row([
        
        dbc.Col(html.Div([
            html.Center(html.Big(dcc.Markdown("""
            This dropdown presents visualizations of other key information about COVID-19
            other than case and death numbers, such as recovery numbers across the U.S.
            Please select an option.
            """))),
            dcc.Dropdown(id='dropdown_2',
            options = [{"label":i, "value":i} for i in options_dropdown_2],
            value = options_dropdown_2[0],
            searchable =True, 
            clearable = False
            ),

            html.Br(),

            dcc.Interval(
                id='my_interval_2',
                disabled=False,
                interval = 3*12000,
                n_intervals = 0,
                max_intervals = -1
                ),

            dcc.Graph(id='chart_2', figure={}),
            ]), width={'size':6}  # this column is 3 units of the page width
        ),

        dbc.Col(html.Div([
            html.Center(html.Big(dcc.Markdown("""
            This dropdown presents visualizations comparing the case and death numbers for U.S. states
            and territories from the virus' inception to the present. Please select a state.
            """))),

            dcc.Dropdown(id='dropdown_3', 
            options = [{"label":i, "value":i} for i in state_names],
            value = 'Alaska',
            searchable= True,
            clearable= False
        ),

            html.Br(),

            dcc.Interval(
                id='my_interval_3',
                disabled=False,
                interval = 3*12000,
                n_intervals = 0,
                max_intervals = -1
                ),

            dcc.Graph('chart_3', figure={}),

            ]), width={'size':6}
        ),
    ]),
    html.Br(),

    html.H1(html.B("Sources"), style={"text-align":"center"}),
    html.Br(),
     dbc.CardDeck(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(html.Center("Finnhub API"), className="card-title"),
                    html.P(
                        """
                        The Finnhub COVID-19 API provides live updates regarding
                        COVID-19 data in the United States, including case and death numbers
                        on a state-wide level. Their data was used to create the choropleth map of all U.S. States
                        """,
                        className="card-text",
                    ),
                    html.Center(dbc.Button(
                        "Link", color="success", className="mt-auto", href="https://finnhub.io/docs/api"
                    )),
                ]
            ),
            color='success',
            outline=True,
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(html.Center("New York Times"), className="card-title"),
                    html.P(
                         """
                            NYT's COVID-19 data repository on GitHub presents a live look at COVID-19 data,
                            including case and death numbers, for all U.S. counties and states. This data was used to create
                            the choropleth map of all U.S. counties, as well as the cases vs. deaths chart for all U.S. states and territories.
                            """,
                        className="card-text",
                    ),
                    html.Center(dbc.Button(
                        "Link", color="warning", className="mt-auto", href='https://github.com/nytimes/covid-19-data/tree/master/live'
                    )),
                    
                ]
            ),
            color='warning',
            outline=True,
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(html.Center("The COVID Tracking Project"), className="card-title"),
                    html.P(
                         """
                            The COVID Tracking Project is a volunteer organization that collects COVID-19 testing and patient outcomes from all U.S. states and territories, as 
                            well as Washington, D.C. These statistics range from hospitalization rates to data regaring race and ethnicity.
                            Their data was used to construct the second chart on the site.
                            """,
                        className="card-text",
                    ),
                    html.Center(dbc.Button(
                        "Link", color="danger", className="mt-auto", href="https://covidtracking.com/"
                    )),
                    
                ]
            ),
            color='danger',
            outline=True,
        ),

    ],
 ),
    html.Br(),
    html.H1(html.B("Additional Resources"), style={"text-align":"center"}),
    dbc.CardDeck([
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(html.Center("Johns Hopkins University"), className="card-title"),
                    html.P(
                          """
                            Johns Hopkins University's COVID-19 Dashboard displays a map of COVID-19 information across the globe, and documents statistics such as global case, death, and 
                            recovery numbers. It also has sections for categories like active and cumulative cases, so users can see how the virus has progressed since its inception.
                            """,
                        className="card-text",
                    ),
                    html.Center(dbc.Button(
                        "Link", color="primary", className="mt-auto", href="https://coronavirus.jhu.edu/map.html"
                    )),
                ]
            ),
            color='primary',
            outline=True,
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(html.Center("Centers for Disease Control and Prevention (CDC)"), className="card-title"),
                    html.P(
                          """
                            The CDC is the primary source for COVID-19 data across the U.S., and is used by many organizations,
                            including The COVID Tracking Project, to help construct their datasets. In addtion to data,
                            the CDC also provides information about COVID-19, including symptoms and prevention methods.
                            """,
                        className="card-text",
                    ),
                     html.Center(dbc.Button(
                        "Link", color="secondary", className="mt-auto", href="https://www.cdc.gov/coronavirus/2019-nCoV/index.html"
                    )),
                    
                ]
            ),
            color='secondary',
            outline=True,
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(html.Center("Broadstreet's COVID-19 Data Project"), className="card-title"),
                    html.P(
                          """
                            The COVID-19 Data Project is a volunteer-based organization dedicated to bringing the public 
                            helping provide research-ready datasets to the public, as well as creating visualizations that 
                            help users see the impact of the virus on a state and county-wide level here in the U.S.
                            """,
                        className="card-text",
                    ),
                    html.Center(dbc.Button(
                        "Link", color="info", className="mt-auto", href="https://covid19dataproject.org/"
                    )),
                    
                ]
            ),
            color='info',
            outline=True,
        ),
    ]),

])

@app.callback(
    Output('live_covid_map', 'figure'),
    [Input('slct_option', 'value'),
     Input('my_interval', 'n_intervals')]
)
def update_chart_1(val, n):
    df, df2 = functions.chart_1_data()

    if val == 'Choropleth of All U.S. States':
        fig1 = px.choropleth(
        data_frame=df,
        locationmode='USA-states',
        locations='state code',
        scope="usa",
        color='case',
        hover_data=['state', 'case', 'death'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'state':'State', 'case':'Cases', 'death':'Deaths', 'state code':'State Code'}
    )

    elif val == 'Choropleth of All U.S. Counties':
        fig1 = px.choropleth(df2, geojson=counties, locations='fips', color='cases',
                           color_continuous_scale="Viridis",
                           scope="usa", 
                           hover_data=['county', 'state', 'cases', 'deaths'],
                           labels={'state':'State', 'cases':'Cases (Confirmed+Probable)', 
                            'deaths':'Deaths (Confimed+Probable)'}
                          )
        fig1.update_traces(marker_line_width=0, marker_opacity=0.8)
        fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig1.update_geos(
        showsubunits=True, subunitcolor="black"
        )

    return fig1

@app.callback(
     Output('chart_2', 'figure'),
    [Input('dropdown_2', 'value'),
    Input('my_interval_2', 'n_intervals')]
)

def update_chart_2(val_2, n):
    df3 = functions.chart_2_data()

    if val_2 == 'Hospitalization Statistics':
        fig2 = px.bar(df3, x='state', y='hospitalizedCurrently', color='state',
        labels={"state":"State", "hospitalizedCurrently":"Patients Hospitalized"})
        functions.update_chart_layout(figure=fig2, title='U.S. Hospitalization Data')

    elif val_2 == 'ICU admission Statistics':
        fig2 = px.bar(df3, x='state', y='inIcuCurrently', color='state', 
        labels={"state":"State", "inIcuCurrently":"Patients in ICU"})
        functions.update_chart_layout(figure=fig2, title='U.S. ICU Data')

    elif val_2 == 'Ventilator Statistics':
        fig2 = px.bar(df3, x='state', y='onVentilatorCurrently', color='state',
        labels={'state':'State', 'onVentilatorCurrently':'Patients on Ventilators'})
        functions.update_chart_layout(figure=fig2, title='U.S. Ventilator Data')
        
    elif val_2 == 'Recovery Statistics':
        fig2 = px.bar(df3, x='state', y='recovered', color='state',
        labels={"state":"State", "recovered": "Patients Recovered"})
        functions.update_chart_layout(figure=fig2, title='COVID-19 Recoveries Across the U.S.')

    return fig2


@app.callback(
     Output('chart_3', 'figure'),
     [Input('dropdown_3', 'value'),
      Input('my_interval_3', 'n_intervals')]
)
def update_chart_3(val_3, n):
    df4 = functions.chart_3_data()

    dff = df4.copy()

    dff = dff[dff['state'] == val_3]
    fig4 = go.Figure(data=[
        go.Scatter(name='Cases', x=dff['date'], y=dff['cases']),
        go.Scatter(name='Deaths', x=dff['date'], y=dff['deaths'])
    ]
    )
    fig4.update_layout(xaxis_title="Date",
    yaxis_title="Cases/Deaths",)
    functions.update_chart_layout(figure=fig4, title='Cases vs Deaths Over Time: {}'.format(val_3))

    return fig4

if __name__ == '__main__':
    app.run_server(debug=True)
