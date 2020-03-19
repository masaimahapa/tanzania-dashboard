import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

app= dash.Dash()
server= app.server
df = pd.read_csv('data/mobile_renamed_cols.csv')

all_incomes=['salaries_wages', 'selling_produce', 'selling_services',
'piece_job', 'rental_income', 'interest_earned', 'pension',
'social_grant', 'pocket_money', 'someone_pays', 'other' ]

app.layout= html.Div([
    html.Div(
        html.Div(
        html.H1('Tanzania Mobile Money',
        style={'textAlign': 'center', 
        'color':'Blue'}
        )
    )
    )
    ,
    html.Br(),
    
    #dropdown for mobel money classification
    
    html.Label('Mobile Money Class'    ),
    dcc.Dropdown(
        id='mm-class',
        options=[
            {'label': 'no mm', 'value': 'no_mm'},
            {'label': 'mm_plus', 'value':'mm_plus'},
            {'label': 'mm_only', 'value':'mm_only'},
            

        ],
        value=['mm_plus','mm_only'],
        multi= True,
        style={
            'width':'100%'
        }
    ),


    html.Br(),
    html.Label('Income Type'),
    dcc.Dropdown(
        id='income-checklist',
    options=[
        {'label': 'selling_produce', 'value': 'selling_produce'},
        {'label': 'piece_job', 'value': 'piece_job'},
        {'label': 'pocket_money', 'value': 'pocket_money'},
        {'label':  'selling_services', 'value':  'selling_services'},
        {'label': 'piece_job', 'value': 'piece_job'},
        {'label': 'rental_income', 'value': 'rental_income'},
        {'label': 'interest_earned', 'value': 'interest_earned'},
        {'label':  'pension', 'value':  'pension',},
        {'label': 'social_grant', 'value': 'social_grant'},
        {'label': 'someone_pays', 'value': 'someone_pays'},
        {'label': 'other', 'value': 'other'}
    ],
    
    value=['selling_produce', 'piece_job', 'pocket_money', 'rental_income', 'social_grant'],
    multi= True,
    style={
            'width':'100%'
        }
    )  
    ,
    html.Br(),
    html.Label('Gender')
    ,
    dcc.RadioItems(
        id='gender-radio',
    options=[
        {'label': 'All', 'value': 'all'},
        {'label': 'Female', 'value': 'female'},
        {'label': 'Male', 'value': 'male'}
    ],
    value='all'
    ) 
    ,
    html.Br(),
    dcc.Graph(
        id='ages'
    )
    ,
    dcc.Graph(
        id='pie', 
    ),

    dcc.Graph(
        id='income-types',
        
    ),
    html.H1('Where do they stay?',
        style={'textAlign': 'center', 
        'color':'Blue'}),

    html.Div(
        children= html.Iframe(
            id='map', srcDoc= open('Tanzania-cycle.html', 'r').read(),
            width='99%', height='600'
        )
    ),
    dcc.Markdown('''
**Tanzanian Mobile Money Dashboard**

Demographic information and what financial services are used by approximately 10,000 individuals across Tanzania. This data was extracted from the FSDT Finscope 2017 survey and prepared specifically for this challenge.
geospatial mapping of all cash outlets in Tanzania in 2012. Cash outlets in this case included commercial banks, community banks, ATMs, microfinance institutions, mobile money agents, bus stations and post offices. This data was collected by FSDT.
_Developed by Masai Mahapa_
''')
])

@app.callback(Output('ages', 'figure'),
[Input('mm-class', 'value'),
Input('gender-radio', 'value')])
def update_age_distribution(classification, gender):
    new_df= df[df.my_class.isin(classification)]
    
    colours=['orange', 'green', 'yellow', 'blue', 'red']

    if gender!= 'all':
        new_df= df[df.gender== gender]
    figure={

        'data': [
            go.Histogram(
                #x= x_ticks,
                x= new_df[new_df.my_class== each].age,
                name= each,
                opacity= 0.5
            ) for each in classification
        ],
        'layout': go.Layout(
            title= "Age distribution",
            xaxis={'title': 'ages'}, 
            barmode='overlay',
            
        )
    }
    return figure

@app.callback(Output('income-types', 'figure'),
[Input('income-checklist', 'value'),
Input('gender-radio', 'value')])
def update_income_type_count(income_types, gender):
    #new_df= df[df.mobile_money_classification.isin(classification)]
    new_df= df[income_types]
    x_ticks= all_incomes
    
    if gender!= 'all':
        new_df= df[df.gender== gender]

    figure={
        'data': [
            go.Bar(
                y= x_ticks,
                x= [sum(new_df[each]) for each in income_types],
                orientation='h'
            
            )
        ],
        'layout': go.Layout(
            title= "Types of income",
            xaxis={'title': 'incomes'}
            
        )
    }
    return figure


@app.callback(Output('pie', 'figure'),
[Input('gender-radio', 'value'),
Input('mm-class', 'value')])
def update_education_pie(gender, classification):
    if gender=='all':
        new_df= df
    elif gender=='male':
        new_df= df[df.gender=='male']
    else:
        new_df= df[df.gender=='female']

    new_df= new_df[new_df.my_class.isin(classification)]
    education_values= new_df.highest_education.value_counts()
    figure={

        'data': [
            go.Pie(
                values= education_values,
                labels= education_values.index
            
            )
        ],
        'layout': go.Layout(
            title= "Highest education",
            
        )
    }
    return figure


if __name__ == "__main__":
    app.run_server(debug=True)    