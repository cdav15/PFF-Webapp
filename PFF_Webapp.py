# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 21:13:58 2023

@author: cadgo
"""

# PFF DV Webapp code
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from highlight_text import fig_text
from mplsoccer import PyPizza, add_image, FontManager
import numpy as np
from scipy import stats
import math
import io



def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/cdav15/Portfolio/main/PFF_Pass.csv?token=GHSAT0AAAAAACMXXWBZGM3TWWPOD3QOYI6KZNASTQQ')
    df = df[df['attempts'] >= 100]
    df.rename(columns={df.columns[0]: 'Player'}, inplace=True)
    return df.set_index("Player")

def receiving_data():
    dfwr = pd.read_csv('https://raw.githubusercontent.com/cdav15/Portfolio/main/PFF_Receiving.csv?token=GHSAT0AAAAAACMXXWBYIV43RIX52XS632K6ZNASUXA')
    dfwr = dfwr[dfwr['targets'] >= 25]
    dfwr.rename(columns={dfwr.columns[0]: 'Player'}, inplace=True)
    return dfwr.set_index("Player")

def rushing_data():
    dfrb = pd.read_csv('https://raw.githubusercontent.com/cdav15/Portfolio/main/PFF_Rushing.csv?token=GHSAT0AAAAAACMXXWBZMBFTCXP5JNUJD5FWZNASVDA')
    dfrb = dfrb[dfrb['attempts'] >= 25]
    dfrb.rename(columns={dfrb.columns[0]: 'Player'}, inplace=True)
    return dfrb.set_index("Player")

def single_graph(params, player, values):
    baker = PyPizza(
    params=params,                  # list of parameters
    straight_line_color="#000000",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    other_circle_lw=1,              # linewidth for other circles
    other_circle_ls="-."            # linestyle for other circles
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values,              # list of values
        figsize=(12, 12),      # adjust figsize according to your need
        param_location=110,  # where the parameters will be added
        kwargs_slices=dict(
            facecolor="cornflowerblue", edgecolor="#000000",
            zorder=2, linewidth=1
        ),                   # values to be used when plotting slices
        kwargs_params=dict(
            color="#000000", fontsize=10,
            va="center"
        ),                   # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=12,  
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                    # values to be used when adding parameter-values
    )

    # add title
    fig.text(
        0.515, 0.97, player, size=18,
        ha="center",   color="#000000"
    )

    # add subtitle
    fig.text(
        0.515, 0.942,
        "Percentile Ranks",
        size=15,
        ha="center",  color="#000000"
    )

    # add credits
    CREDIT_1 = "Data: Pro Football Focus"
    CREDIT_2 = "Webapp developed by Chandler Davis"
    CREDIT_3 = 'https://www.linkedin.com/in/chandler-a-davis/'

    fig.text(
        0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=9,
        color="#000000",
        ha="right"
    )

    st.pyplot(fig)
    
    st.write('#### Download Graph as Image Below:')
    download_filename = st.text_input('Choose File Name:', value=player)
    
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    
    file_name1 = download_filename + '.jpg'
    
    st.download_button(
        label="Download Graph as PNG",
        data=img_bytes,
        file_name=file_name1,
        mime='image/png',
    )
    
def comparison_graph(params, player1, values1, player2, values2):
    baker3 = PyPizza(
        params=params,                 
        background_color="#EBEBE9",     
        straight_line_color="#222222",
        straight_line_lw=1,             
        last_circle_lw=1,               
        last_circle_color="#222222",    
        other_circle_ls="-.",           
        other_circle_lw=1               
    )


    fig3, ax3 = baker3.make_pizza(
        values1,                     
        compare_values=values2,    
        figsize=(12, 12),             
        kwargs_slices=dict(
            facecolor="#1A78CF", edgecolor="#222222",
            zorder=2, linewidth=1
        ),                          
        kwargs_compare=dict(
            facecolor="#FF9300", edgecolor="#222222",
            zorder=2, linewidth=1,
        ),
        kwargs_params=dict(
            color="#000000", fontsize=10,
            va="center"
        ),                          
        kwargs_values=dict(
            color="#000000", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        ),                          
        kwargs_compare_values=dict(
            color="#000000", fontsize=12, zorder=3,
            bbox=dict(edgecolor="#000000", facecolor="#FF9300", boxstyle="round,pad=0.2", lw=1)
        ),                          
    )

    fig_text(
        0.515, 0.99, f"<{player1}> vs <{player2}>", size=17, fig=fig3,
        highlight_textprops=[{"color": '#1A78CF'}, {"color": '#EE8900'}],
        ha="center", color="#000000"
    )

    fig3.text(
        0.515, 0.942,
        "Player Percentile Ranking Comparison",
        size=15,
        ha="center", color="#000000"
    )

    # add credits
    CREDIT_1 = "Data: Pro Football Focus"
    CREDIT_2 = "Webapp developed by Chandler Davis"
    CREDIT_3 = 'https://www.linkedin.com/in/chandler-a-davis/'

    fig3.text(
        0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=9,
        color="#000000",
        ha="right"
    )
    pnames = player1 + ' and ' + player2 
    st.pyplot(fig3)
    st.write('#### Download Graph as Image Below:')
    download_filename = st.text_input('Choose File Name:', value=pnames)
    
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    
    file_name1 = download_filename + '.jpg'
    
    st.download_button(
        label="Download Graph as PNG",
        data=img_bytes,
        file_name=file_name1,
        mime='image/png',
    )
    
   

tabs = ['Home Screen','Passing']

st.sidebar.title('Menu')
selected_tab = st.sidebar.radio('Select Page', tabs)


if selected_tab == 'Home Screen':
    st.title('Pro Football Focus Player Comparison Webapp')
    st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0Jz4nqpr7AJFcwQCdD_FNwYV1vKhdfNhNEYg6w_l0yA&s')
    st.subheader('Developed by Chandler Davis: Data by Pro Football Focus')
    
    st.write("This webapp was developed to help coaches and fans understand the strengths and weaknesses of NFL Players. " 
             "This webapp takes data provided by Pro Football Focus and turns key statistics into percentile rankings. "
             "For each category (Passing, rushing, receiving, etc.) there are minumum snap count requirements to preserve the integrity of the percentile rankings. "
             "The percentile rankings are then charted on a radar chart to easily visualize where a player is thriving and struggling compared to their position averages. "
             "Below will be an example radar chart. ")
    
    
    st.image('https://imgur.com/a/VGm1DJz', output_format='JPEG')
    st.write('Using the above graph, we can see that Josh Allen excels in the following categories: Pass Grade, Offense Grade, Depth of Target, Completions, etc. '
             'Using the same graph, we can see that Josh Allen struggles with: Interceptions, Turnover Worthy Plays, and he has a high receiver drop rate compared to other QBs. ')
    
    st.write('Use the sidepane on the left to select what position group you would like to view.')
    
    st.write('Note: Rushing and Receiving to be added at a later date.')
    
    st.markdown('Link to GitHub: https://github.com/cdav15/Portfolio')




elif selected_tab == 'Passing':
    st.title('PFF Passer Stats and Grades Percentile Rankings')
    
    df = get_data()
    
    
    st.write("I've created this web app to help fans, analysts, and coaches better understand the strengths and weaknesses of a NFL QB.")
    st.write("The data is filtered to Quarterbacks who have attempted 100 passes or more during the 2023 Regular Season.")
    st.write("                  ")
    st.write('Original Data Provided Below')
    st.dataframe(df)

    

    st.write("## QB Strengths and Weaknesses")
    player_select = st.selectbox("Choose a player:", list(df.index))
    
    if not player_select:
        st.error("Please Select a Player.")
    else:
        df2 = df.drop(['player_id', 'position', 'bats', 'team_name', 'player_game_count', 
                         'declined_penalties', 'def_gen_pressures', 'first_downs', 'franchise_id',
                        'hit_as_threw','penalties', 'spikes',
                        'thrown_aways'], axis=1)
        
        
        df2.rename(columns={df2.columns[0]: 'Adjusted Completion %',
                             df2.columns[1]: 'Aimed Passes',
                             df2.columns[2]: 'Attempts',
                             df2.columns[3]: 'Depth of Target',
                             df2.columns[4]: 'Average Time to Throw',
                             df2.columns[5]: 'Big Time Throws',
                             df2.columns[6]: 'Big Time Throw Rate',
                             df2.columns[7]: 'Completion %',
                             df2.columns[8]: 'Completions',
                             df2.columns[9]: 'Receiver Drop Rate',
                             df2.columns[10]: 'Dropbacks',
                             df2.columns[11]: 'Receiver Drops',
                             df2.columns[12]: 'Fumble Grade',
                             df2.columns[13]: 'Offense Grade',
                             df2.columns[14]: 'Pass Grade',
                             df2.columns[15]: 'Run Grade',
                             df2.columns[16]: 'Interceptions',
                             df2.columns[17]: 'Passing Snaps',
                             df2.columns[18]: 'Pressure to Sack Rate',
                             df2.columns[19]: 'QB Rating',
                             df2.columns[20]: 'Sack %',
                             df2.columns[21]: 'Total Sacks',
                             df2.columns[22]: 'Scrambles',
                             df2.columns[23]: 'Touchdowns',
                             df2.columns[24]: 'Turnover Worthy Plays',
                             df2.columns[25]: 'Turnover Worthy Play Rate',
                             df2.columns[26]: 'Total Yards',
                             df2.columns[27]: 'Yards Per Attempt'}, inplace=True)
        
        data = df2.loc[[player_select]]
        
        st.write("###### Player Stats", data)

        df2['Interceptions'] *= -1
        df2['Pressure to Sack Rate'] *= -1
        df2['Turnover Worthy Plays'] *= -1
        df2['Turnover Worthy Play Rate'] *= -1
        df2['Receiver Drop Rate'] *= -1
        df2['Receiver Drops'] *= -1
        df2['Sack %'] *= -1
        df2['Total Sacks'] *= -1

        fields = st.multiselect(
            "Choose stats to view in the graph:", list(df2.columns), ["Adjusted Completion %", "Big Time Throw Rate",
                                                           "Pass Grade", "Interceptions", "Touchdowns", "Yards Per Attempt",
                                                           "Turnover Worthy Play Rate", "Offense Grade", "Depth of Target",]
  )
        
        parameters = fields
        
        params = parameters
                        
        p1 = player_select
        
        df3 = df2[params]
        player = df3.loc[[p1]].reset_index()
        player = list(player.loc[0])    
        player = player[1:]

        values = []
        for x in range(len(params)):
            values.append(math.floor(stats.percentileofscore(df3[params[x]],player[x])))
            

        single_graph(params, p1, values)
        
#####################

        df2['Interceptions'] *= -1
        df2['Pressure to Sack Rate'] *= -1
        df2['Turnover Worthy Plays'] *= -1
        df2['Turnover Worthy Play Rate'] *= -1
        df2['Receiver Drop Rate'] *= -1
        df2['Receiver Drops'] *= -1
        df2['Sack %'] *= -1
        df2['Total Sacks'] *= -1


        st.write("# Comparison Chart")
        st.write('Choose two players in the drop down boxes below to compare their percentile rankings in your selected stat categories')
        
        players = st.selectbox(
            "## Choose a player:", list(df.index), index=16)
        
        players1 = st.selectbox(
            "## Choose a player to compare to:", list(df.index), index=3)
        
        datas_1 = df2.loc[[players, players1]]
        
        st.write(datas_1)
        
        
        p2 = players
        p3 = players1
        
        player2 = df3.loc[[p2]].reset_index()
        player2 = list(player2.loc[0])    
        player2 = player2[1:]
         
        player3 = df3.loc[[p3]].reset_index()
        player3 = list(player3.loc[0])
        player3 = player3[1:]
        
        values2 = []
        for x in range(len(params)):
            values2.append(math.floor(stats.percentileofscore(df3[params[x]],player2[x])))
         
        values3 = []
        for x in range(len(params)):
            values3.append(math.floor(stats.percentileofscore(df3[params[x]],player3[x])))


        comparison_graph(params, players, values2, players1, values3)
