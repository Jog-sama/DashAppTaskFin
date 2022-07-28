import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output


app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
df = pd.read_csv("intro_bees.csv")

# to only describe this particular column
print(df['Pct of Colonies Impacted'].describe())

states_df = df['State'].unique()
period_df = df['Period'].unique()
cause_df = df['Affected by'].unique()

df = df.groupby(['State', 'ANSI', 'Year', 'Period', 'Affected by', 'state_code'])[
    ['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
#print(df[:50])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash",
            style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_state",
                 options=[
                    {'label': i, 'value': i} for i in states_df],
                 multi=False,
                 value='Alabama',
                 style={'width': "40%"}
                 ),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    dcc.Dropdown(id="slct_period",
                 options=[
                     {'label': i, 'value': i} for i in period_df],
                 multi=False,
                 value="JAN THRU MAR",
                 style={'width': "40%"}
                 ),

    dcc.Dropdown(id="slct_cause",
                 options=[
                     {'label': i, 'value': i} for i in cause_df],
                 multi=False,
                 value="Varroa_mites",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container1', children=[]),
    html.Div(id='output_container2', children=[]),
    html.Div(id='output_container3', children=[]),
    html.Div(id='output_container4', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container1', component_property='children'),
     Output(component_id='output_container2', component_property='children'),
     Output(component_id='output_container3', component_property='children'),
     Output(component_id='output_container4', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_state', component_property='value'),
     Input(component_id='slct_year', component_property='value'),
     Input(component_id='slct_period', component_property='value'),
     Input(component_id='slct_cause', component_property='value')]
)
def update_graph(slctd_state, slctd_year, slctd_period, slctd_cause):
    print(slctd_state)
    print(slctd_year)
    print(slctd_period)
    print(slctd_cause)
    print(type(slctd_state))
    print(type(slctd_year))
    print(type(slctd_period))
    print(type(slctd_cause))

    container1 = "The state chosen by user was: {}".format(slctd_state)
    container2 = "The year chosen by user was: {}".format(slctd_year)
    container3 = "The period chosen by user was: {}".format(slctd_period)
    container4 = "The cause chosen by user was: {}".format(slctd_cause)

    dff = df.copy()
    dff = dff[dff["State"] == slctd_state]
    dff = dff[dff["Year"] == slctd_year]
    dff = dff[dff["Period"] == slctd_period]
    dff = dff[dff["Affected by"] == slctd_cause]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        range_color=(0, 50),
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    return container1, container2, container3, container4, fig


# ------------------------------------------------------------------------------
# Running the app in a Browser Window
if __name__ == '__main__':
    app.run_server(debug=True, port=8070)
