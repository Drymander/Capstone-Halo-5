


import plotly.graph_objects as go
# from plotly.subplots import make_subplots
from plotly.subplots import make_subplots
def compare_stat(df, column_name):
    
#     layout = go.Layout(
#         margin=go.layout.Margin(
#             l=100, #left margin
#             r=0, #right margin
#             b=0, #bottom margin
#             t=0))  #top margin
    
    df = df.round(2)
    # Separate player and enemy teams
    df_player = df.loc[df['PlayerTeam'] == 'Player']
    df_enemy = df.loc[df['PlayerTeam'] == 'Enemy']

    # Sort total time played by descending
    df_player = df_player.sort_values(by=[column_name])
    df_enemy = df_enemy.sort_values(by=[column_name])

    # Assign player / enemy colors
    if df_player['TeamColor'].iloc[0] == 'Blue':
        player_color = 'Blue'
        enemy_color = 'Red'
    else:
        player_color = 'Red'
        enemy_color = 'Blue'
    
    # Make subplot and X axis range
    fig = make_subplots(rows=2, cols=1, subplot_titles=[f'Player Team - {column_name}', 
                                                        f'Enemy Team - {column_name}'],
                       vertical_spacing = 0.12)
    x_range = df[column_name].max()
    
    # Player team sub plot
    fig.add_trace(go.Bar(
                x=df_player[column_name],
                y=df_player['Gamertag'],
                orientation='h',
                text=df_player[column_name],
                textposition='auto',
                marker_color=player_color),
                    row=1, col=1)
    fig.update_xaxes(range=[0, x_range], row=1, col=1)
    
    # Enemy team sub plot
    fig.add_trace(go.Bar(
                x=df_enemy[column_name],
                y=df_enemy['Gamertag'],
                orientation='h',
                text=df_enemy[column_name],
                textposition='auto',
                marker_color=enemy_color),
                    row=2, col=1)
    fig.update_xaxes(range=[0, x_range], row=2, col=1)
    fig.update_yaxes(automargin=True)
    fig['layout'].update(margin=dict(l=125,r=50,b=20,t=30))
    fig['layout'].update(showlegend=False)
#     fig.update_layout(title_text='test')
    return fig

# compare_stat(df, 'TotalHeadshots')
