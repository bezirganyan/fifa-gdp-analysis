import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import markdowns

gdp_df = pd.read_csv("gdp_preprocessed.csv")
fifa_df = pd.read_csv("fifa_ranking_preprocessed.csv")
countries = fifa_df.country.unique()
print(gdp_df['year'])
app = dash.Dash()
app.layout = html.Div([
    html.H1("FIFA World ranking analysis based on country GDP",
            style={'text-align': 'center'}),
    html.Div([
        html.Div([
            dcc.Slider(
                id='year-slider',
                min=gdp_df['year'].min(),
                max=gdp_df['year'].max(),
                value=gdp_df['year'].min(),
                step=None,
                marks={str(year): str(year) for year in gdp_df['year'].unique()}
            )
        ], style={'margin-bottom': '4vh'}),
        html.Div([
            html.Div([dcc.Graph(id='graph-with-slider')], className='nine columns'),
            html.Div([dcc.Markdown(markdowns.scatter_markdown)], className='three columns')
        ], className='row')
    ]),
    html.Div([
        dcc.Dropdown(
            options=[{"value": c, "label": c} for c in countries],
            id="country_dropdown",
            value=["Armenia"],
            multi=True
        ),
        html.Div([
            html.Div([dcc.Markdown(markdowns.rank_lineplot_markdown)], className='three columns'),
            html.Div([dcc.Graph(id='country_rank_graph')], className='nine columns')
        ], className='row'),
        html.Div([
            html.Div([dcc.Markdown(markdowns.gdp_lineplot_markdown)], className='three columns'),
            html.Div([dcc.Graph(id='country_gdp_graph')], className='nine columns')
        ], className='row')
    ]),
    html.Div([
        dcc.Markdown("Created by Grigor Bezirganyan:   [github.com/bezirganyan](github.com/bezirganyan)")
    ])
],  style={'display': 'inline-block', 'width': '120vh', 'margin-left': '35vh', 'margin-right': '35vh'})


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_scatter_figure(selected_year):
    filtered_gdp = gdp_df[gdp_df.year == selected_year]
    filtered_fifa = fifa_df[fifa_df.year == selected_year]
    traces = []
    for i in filtered_fifa.country.unique():
        gdp_by_country = filtered_gdp[filtered_gdp['country'] == i]
        # gdp_by_country.gdp = functions.normalize(gdp_by_country.gdp)

        fifa_by_country = filtered_fifa[filtered_fifa['country'] == i]
        # fifa_by_country.rank = functions.normalize(fifa_by_country["rank"])

        traces.append(go.Scatter(
            x=gdp_by_country['gdp'],
            y=fifa_by_country['rank'],
            text=gdp_by_country['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            yaxis={'title': 'Rank (Inversed)', 'autorange': 'reversed'},
            xaxis={'type': 'log', 'title': 'GDP)'},
            margin={'l': 40, 'b': 40, 't': 30, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            title="Correlation of GDP and Rank based on countries in a single year"
        )
    }


@app.callback(dash.dependencies.Output('country_rank_graph', 'figure'),
              [dash.dependencies.Input('country_dropdown', 'value')])
def update_rank_plot(selected_countries):
    # filtered_gdp = gdp_df[gdp_df.year == selected_year]
    filtered_fifa = fifa_df[fifa_df.country.isin(selected_countries)]
    traces = []
    print(filtered_fifa)
    for i in filtered_fifa.country.unique():
        fifa_by_country = filtered_fifa[filtered_fifa['country'] == i]

        traces.append(go.Scatter(
            x=fifa_by_country['year'],
            y=fifa_by_country['rank'],
            text=i,
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            yaxis={'title': 'Fifa Ranking', 'autorange': 'reversed'},
            xaxis={'title': 'Year'},
            margin={'l': 40, 'b': 40, 't': 30, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            title='GDB of countries through years'
        )
    }


@app.callback(dash.dependencies.Output('country_gdp_graph', 'figure'),
              [dash.dependencies.Input('country_dropdown', 'value')])
def update_rank_plot(selected_countries):
    # filtered_gdp = gdp_df[gdp_df.year == selected_year]
    filtered_gdp = gdp_df[gdp_df.country.isin(selected_countries)]
    traces = []
    for i in filtered_gdp.country.unique():
        # gdp_by_country = filtered_gdp[filtered_gdp['country'] == i]
        # gdp_by_country.gdp = functions.normalize(gdp_by_country.gdp)

        gdp_by_country = filtered_gdp[filtered_gdp['country'] == i]
        # fifa_by_country.rank = functions.normalize(fifa_by_country["rank"])

        traces.append(go.Scatter(
            x=gdp_by_country['year'],
            y=gdp_by_country['gdp'],
            text=i,
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            yaxis={'title': 'GDP'},
            xaxis={'title': 'Year'},
            margin={'l': 40, 'b': 40, 't': 30, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            title='GDB of countries through years'
        )
    }


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server()