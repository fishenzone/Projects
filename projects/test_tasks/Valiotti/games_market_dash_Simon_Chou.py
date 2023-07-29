import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

def read_url(url):
  url='https://drive.google.com/uc?id=' + url.split('/')[-2]
  df = pd.read_csv(url)
  return df

def clean_df(df, col):
  df.dropna(inplace=True)
  df = df[(df != 'tbd').all(axis=1)]
  df = df[df[col] >= 2000]
  return df

def change_type(df, col1, col2):
  df[col1] = df[col1].astype(int)
  df[col2] = df[col2].astype(int)
  return df

df = read_url('https://drive.google.com/file/d/1QXvqgwjo_PJixFRcapKhjyca_Cd-58pr/view?usp=sharing')
df = clean_df(df, 'Year_of_Release')
df = change_type(df, 'Year_of_Release', 'Critic_Score')

app = dash.Dash(__name__)

genre_options = [{'label': i, 'value': i} for i in df['Genre'].unique()]
rating_options = [{'label': i, 'value': i} for i in df['Rating'].unique()]

app.layout = html.Div([
    html.H1('Games Dashboard'),
    dcc.Dropdown(
        id='genre-filter',
        options=genre_options,
        value=[],
        multi=True,
        placeholder='Select Genre(s)'
    ),
    dcc.Dropdown(
        id='rating-filter',
        options=rating_options,
        value=[],
        multi=True,
        placeholder='Select Rating(s)'
    ),
    dcc.RangeSlider(
        id='year-slider',
        min=df['Year_of_Release'].min(),
        max=df['Year_of_Release'].max(),
        value=[df['Year_of_Release'].min(), df['Year_of_Release'].max()],
        marks={str(year): str(year) for year in range(df['Year_of_Release'].min(), df['Year_of_Release'].max()+1)},
    ),
    html.H3(id='game-count'),
    dcc.Graph(id='area-plot'),
    dcc.Graph(id='scatter-plot')
])

@app.callback(
    [Output('game-count', 'children'),
     Output('area-plot', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('genre-filter', 'value'),
     Input('rating-filter', 'value'),
     Input('year-slider', 'value')]
)
def update_dashboard(genres, ratings, years):
    dff = df[(df['Genre'].isin(genres)) & (df['Rating'].isin(ratings)) & (df['Year_of_Release'] >= years[0]) & (df['Year_of_Release'] <= years[1])]
    
    game_count = f"Number of Selected Games: {len(dff)}"
    
    area_plot = px.area(dff, x="Year_of_Release", y="Name", color="Platform")
    
    scatter_plot = px.scatter(dff, x="User_Score", y="Critic_Score", color="Genre")
    
    return game_count, area_plot, scatter_plot

if __name__ == '__main__':
    app.run_server(debug=True)