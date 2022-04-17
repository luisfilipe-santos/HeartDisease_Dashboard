from pydoc import classname
from turtle import width
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import datetime

############ DATASET ##################

df = pd.read_csv('strokes_data.csv')

df.sort_values(by=['AgeCategory'], inplace=True)
df.Race.replace('American Indian/Alaskan Native', 'Other', inplace=True)

fighistini = px.histogram(df, x="AgeCategory", color="Race", color_discrete_sequence=px.colors.sequential.Aggrnyl)
fighistini.update_layout(
        plot_bgcolor='white',
    )


###### Interactive Components ########

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

############# App Layout #############

app.layout = dbc.Container([
    
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H1("What Influences Heart Disease?", className='text-center my-3'),
            html.H4("Quick exploration on what types of variables might contribute to the appearance of Heart Diseases", className='text-center card-title my-3'),
        ], width =12),
    ]),

    html.Br(),
    html.Hr(),
    html.Br(),

    dbc.Row([
        html.H2("1. Quick look at our Dataset")
    ]),
    html.Br(),
    
    dbc.Row([
        html.Br(),
        dbc.Col([
            html.H5('Gender distribution'),
            dcc.Graph(id="demopie", figure = px.pie(df, values=df['Sex'].value_counts().values, 
                names=df['Sex'].value_counts().index, 
                hole=.3,
                color_discrete_sequence=px.colors.sequential.Aggrnyl,
                ),
            )
        ], width =5),
        dbc.Col([
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H4('This Dataset', className='text-center'),
            html.H6('contains', className='text-center'),
            html.H2(str(len(df)), className='text-center'),
            html.H4('Individuals', className='text-center'),
        ], width =2),
        dbc.Col([
            html.H5('Demographics'),
            dcc.Graph(id="histage", figure = fighistini),
        ], width =5),
    ]),

    html.Br(),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Br(),

    dbc.Row([
        html.H2("2. How are these variables associated with Heart Diseases", className="text-md-end")
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H5("Which variables are more correlated with Heart Diseases?"),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'DiffWalking', 'value': 'DiffWalking'},
                    {'label': 'Stroke', 'value': 'Stroke'},
                    {'label': 'Physical Health', 'value': 'PhysicalHealth'},
                    {'label': 'PhysicalHealth', 'value': 'PhysicalHealth'},
                    {'label': 'Kidney Disease', 'value': 'KidneyDisease'},
                    {'label': 'Smoking', 'value': 'Smoking'},
                    {'label': 'Skin Cancer', 'value': 'SkinCancer'},
                    {'label': 'BMI', 'value': 'BMI'},
                    {'label': 'Asthma', 'value': 'Asthma'},
                    {'label': 'Mental Health', 'value': 'MentalHealth'},
                    {'label': 'Sleep Time', 'value': 'SleepTime'},
                    {'label': 'Alcohol Drinking', 'value': 'AlcoholDrinking'},
                    {'label': 'Physical Activity', 'value': 'PhysicalActivity'},
                ],
                value=['BMI', 'PhysicalHealth', 'Smoking'],
                multi=True,
                id="dropdown-input",
            ),
            dcc.Graph(id="barplot")
        ], width = 4),
        
        dbc.Col([
            html.Br(),
            html.H5("What about Diabetes?"),
            html.Br(),
            html.Br(),
            dbc.Checklist(
                options=[
                    {"label": "Heart Disease Switch", "value": 1},
                ],
                id="switches-input",
                value=[],
                switch=True,
            ),
            dcc.Graph(id="stpie"),
        ], width = 4),
        dbc.Col([
            html.Br(),
            html.H5('Would you say your general health is...'),
            dcc.Graph(id="sndpie"),
        ], width = 4)
    ]),

    html.Br(),
    html.Hr(),
    html.Br(),
    html.Br(),

    dbc.Row([
        html.H2("3. Age and BMI on Heart Diseases")
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col ([
            html.Br(),
            html.Br(),
            html.H5("Heart Disease distribution on BMI and Age Group", className="text-md-start"),
            html.Br(),
            dbc.RadioItems(
            options=[
                {"label": "% of Heart Diseases per BMI", "value": 1},
                {"label": "Sum of Heart Diseases per Age group", "value": 2},
            ],
            value=1,
            id="radioitems-input-bmi-age",
        ),
        ], width = 2),
        dbc.Col ([
            dcc.Graph(id='line', figure={})
        ], width=5),
        dbc.Col ([
            html.H5("Where do you land..?"),
            
            html.Br(),
            html.Label('Gender?'),
            dbc.RadioItems(
            options=[
                {"label": "Male", "value": 'Male'},
                {"label": "Female", "value": 'Female'},
            ],
            id="radioitems-input",
            ),

            html.Br(),
            html.Label('Whats your age?'),
            dbc.Select(
            id="select",
            placeholder='Select your Age',
            options=[
                {"label": "18-24"},
                {"label": "25-29"},
                {"label": "30-34"},
                {"label": "35-39"},
                {"label": "40-44"},
                {"label": "45-49"},
                {"label": "50-54"},
                {"label": "55-59"},
                {"label": "60-64"},
                {"label": "65-69"},
                {"label": "70-74"},
                {"label": "75-79"},
                {"label": "80 or older"},
            ],      
            ),
            html.Label('Whats your BMI?'),
            dbc.Input(type="number", placeholder="Write down your BMI", id='bminput'),
            html.Br(),
            html.Br(),
            dbc.Button("Submit", id='my-button', n_clicks=0, color="primary", className="me-1")

        ], width=2),
        dbc.Col ([
            html.H5("Sum of Heart Diseases", className='text-end'),
            dcc.Graph(id="pie"),
        ], width=3)
    ]),

    html.Br(),
    html.Hr(),
    html.Br(),

    dbc.Row([
        dbc.Col([
            html.H6('Dashboard made by Group 24', className='text-center'),
            html.H6('Luís Santos', className='text-center'),
            html.H6('Maria Pedrosa', className='text-center'),
            html.H6('Maria Inês Silva', className='text-center'),
            html.Br(),
        ], width={'size':12}),
    ]),

], fluid=True)


# Callback section: connecting the components
# ************************************************************************
@app.callback(
    Output('sndpie', 'figure'),
    [Input('switches-input', 'value')],
)
def update_stpie(switch):
    dfstpie = df.copy()

    dfstpie.HeartDisease.replace(('Yes', 'No'), (1, 0), inplace=True)

    if len(switch) > 0:
        dfstpie = dfstpie.loc[dfstpie['HeartDisease'] == 1]
    
    figst = px.pie(dfstpie, values=dfstpie['GenHealth'].value_counts().values, 
        names=dfstpie['GenHealth'].value_counts().index, 
        hole=.3,
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
    )
    return figst


@app.callback(
    Output('stpie', 'figure'),
    [Input('switches-input', 'value')],
)
def update_sndpie(switch):
    dfsndpie = df.copy()

    dfsndpie.HeartDisease.replace(('Yes', 'No'), (1, 0), inplace=True)

    if len(switch) > 0:
        dfsndpie = dfsndpie.loc[dfsndpie['HeartDisease'] == 1]
    
    figsnd = px.pie(dfsndpie, values=dfsndpie['Diabetic'].value_counts().values, 
        names=dfsndpie['Diabetic'].value_counts().index, 
        hole=.3,
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
    )
    
    #figsnd.update_layout(paper_bgcolor="rgb(0,0,0,0)")
    #figsnd.update_layout(paper_bgcolor="#000000")

    return figsnd

@app.callback(
    Output('barplot', 'figure'),
    [Input('dropdown-input', 'value')],
)
def update_bar(drop):
    data = df.copy()

    data['HeartDisease'] = data['HeartDisease'].replace({'No': 0, 'Yes': 1})
    data['Smoking'] = data['Smoking'].replace({'No': 0, 'Yes': 1})
    data['AlcoholDrinking'] = data['AlcoholDrinking'].replace({'No': 0, 'Yes': 1})
    data['Stroke'] = data['Stroke'].replace({'No': 0, 'Yes': 1})
    data['DiffWalking'] = data['DiffWalking'].replace({'No': 0, 'Yes': 1})
    data['PhysicalActivity'] = data['PhysicalActivity'].replace({'No': 0, 'Yes': 1})
    data['Asthma'] = data['Asthma'].replace({'No': 0, 'Yes': 1})
    data['KidneyDisease'] = data['KidneyDisease'].replace({'No': 0, 'Yes': 1})
    data['SkinCancer'] = data['SkinCancer'].replace({'No': 0, 'Yes': 1})

    c = data.corr()[['HeartDisease']].sort_values('HeartDisease', ascending=False)
    Features = ["HeartDisease", "DiffWalking", "Stroke", "PhysicalHealth", "KidneyDisease", "Smoking", "SkinCancer",
                    "BMI", "Asthma", "MentalHealth", "SleepTime", "AlcoholDrinking", "PhysicalActivity"]
    c['Features'] = Features

    c = c[c['Features'].isin(drop)]

    figbar = px.bar(c, x='HeartDisease', y='Features', color_discrete_sequence=px.colors.sequential.Aggrnyl)

    figbar.update_layout(
        plot_bgcolor='white',
    )

    return figbar



@app.callback(
    Output('line', 'figure'),
    [Input('radioitems-input-bmi-age', 'value')],
)
def update_line(radio):
    if (radio == 1):
        dffl = df.copy()

        dffl['BMI'] = dffl['BMI'].astype(int)

        dffl.sort_values(by=['BMI'], inplace=True)
        array = []

        for i in dffl['BMI'].unique():
            tempdf = dffl.loc[dffl['BMI'] == i]
            tempdf['HeartDisease'] = tempdf.HeartDisease.replace(('Yes', 'No'), (1, 0))
        
            if round((tempdf['HeartDisease'].sum()*100) /len(tempdf)) != 0:
                array.append([tempdf['BMI'].unique()[0] , round((tempdf['HeartDisease'].sum()*100) /len(tempdf), 2)])

        xax = [16,18,20,22,24,26,28,30,32,34,36]
        yax = []

        counter = 0
        for i in xax:
            num = 1
            avg = 0
            while i >= array[counter][0]:
                avg += array[counter][1]
                num += 1
                counter += 1
        
        
            yax.append(round(avg/(num-1) , 2))

        
        figline = px.line(x=xax, y=yax, 
            labels={'x': 'BMI', 'y':'Percentage of Heart Diseases'},
            markers=True,
            color_discrete_sequence=px.colors.sequential.Aggrnyl,
        )

        figline.update_layout(
            plot_bgcolor="white",
        )
        

    else:
        dff = df.copy()
        dff.sort_values(by=['AgeCategory'], inplace=True)
        dff['HeartDisease'] = dff.HeartDisease.replace(('Yes', 'No'), (1, 0))
        

        figline = px.histogram(dff, x="AgeCategory" , y="HeartDisease", labels={'AgeCategory': 'Age Categories', 'HeartDisease':'Heart Diseases'}, 
                        color_discrete_sequence=px.colors.sequential.Aggrnyl)

        figline.update_layout(
            autosize=False,
            margin=dict(
                autoexpand=False,
                l=100,
                r=20,
                t=110,
            ),
            showlegend=True,
            plot_bgcolor='white',
        )

    return figline

# Pie
@app.callback(   
    Output("pie", "figure"),
    [
        Input('my-button', 'n_clicks')
    ],
    [
        State('radioitems-input','value'),
        State('select','value'),
        State('bminput','value'),
    ]
)
def update_pie(n_clicks, gender, age, bmi):
    dff = df.copy()

    age_labeldict = {
    '18-24':'18-39',
    '25-29':'18-39',
    '30-34':'18-39',
    '35-39':'18-39',
    '40-44':'40-64',
    '45-49':'40-64',
    '50-54':'40-64',
    '55-59':'40-64',
    '60-64':'40-64',
    '65-69':'65 or older',
    '70-74':'65 or older',
    '75-79':'65 or older',
    '80 or older':'65 or older'
    }

    dff['AgeCategory'] = dff.AgeCategory.replace(age_labeldict)

    replace_dict = {
        '18.5': 18.5, 
        '24.9': 24.9, 
        '29.9': 29.9, 
        '30.0': 200.0,
    }

    dff['BMI'] = pd.cut(dff['BMI'],
                      bins=[1]+list(replace_dict.values()),
                      labels=list(replace_dict.keys()))

    if gender != None:
        dff = dff.loc[dff['Sex'] == gender]

    if  age != None:
        age = age_labeldict[str(age)]
        dff = dff.loc[dff['AgeCategory'] == age]

    if bmi != None:
        if float(bmi) < 18.5:
            bmi = '18.5'
        elif float(bmi) >= 18.5 and float(bmi) <24.9:
            bmi = '24.9'
        elif float(bmi) >= 24.9 and float(bmi) <30.0:
            bmi = '29.9'
        elif float(bmi) >= 30.0:
            bmi = '30.0'

        dff = dff.loc[dff['BMI'] == bmi]

    
    figPie = px.pie(dff, values=dff['Stroke'].value_counts().values, 
            names=dff['Stroke'].value_counts().index,
            hole=.3,
            color_discrete_sequence=px.colors.sequential.Aggrnyl,
            )

    return figPie


if __name__ == "__main__":
    app.run_server(debug=True)