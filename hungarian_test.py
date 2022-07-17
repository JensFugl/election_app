# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:31:58 2022

@author: jensr
"""

import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as stats
import streamlit as st
from datetime import datetime



st.header("Hungarian election data 2022")


def benford_checker(df, column, data_name):
    df = df[df[column] != 0 ]
    df['First digit'] = df[column].apply(lambda x : int(str(x)[0]))
    df['Second digit'] = df[column].apply(lambda x : int(str(x)[1]))

    distribution = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

    group = df.groupby('First digit').count()
    group['Benford distribution'] = distribution
    group[data_name] = group['votes']/sum(group['votes'])*100
    group1 = group[['Benford distribution', data_name]]

    #perform Chi-Square Goodness of Fit Test
    result1 = stats.chisquare(f_obs=group1[data_name].array, f_exp=group1['Benford distribution'].array)

    distribution = [12.00,11.40,10.90,10.40, 10.00, 9.70, 9.30, 9.00, 8.80, 8.50]


    group = df.groupby('Second digit').count()
    group['Benford distribution'] = distribution
    group[data_name] = group['votes']/sum(group['votes'])*100
    group2 = group[['Benford distribution', data_name]]

    #perform Chi-Square Goodness of Fit Test
    result2 = stats.chisquare(f_obs=group2[data_name].array, f_exp=group2['Benford distribution'].array)

    return result1, result2,  group1, group2


@st.cache
def load_data():
    
    df = pd.read_pickle('election_data.pkl')
    df_agg = df
    df_agg = df_agg.groupby('affiliation').sum().drop(columns= 'relative').sort_values('votes', ascending =False)
    return df, df_agg

df, df_agg = load_data()


option = st.sidebar.selectbox(
     'Menu',
     ('Raw data', 'Party votes', 'BL chisquare'))

#st.write('You selected:', option)

if option == 'Raw data':
    st.dataframe(df)
if option == 'Party votes':    
    st.bar_chart(df_agg.sort_values('votes', ascending =False))
    st.dataframe(df_agg)

if option == 'BL chisquare':
    result1, result2, group1, group2 = benford_checker(df, 'votes','Hungarian Election')
    st.write('## First digit analysis')
    st.write('\u03C72 = {} p-value = {}'.format( result1.statistic, result1.pvalue))
    st.bar_chart(data=group1['Hungarian Election'])
    
    st.write('## Second digit analysis')
    st.write('\u03C72 = {} p-value = {}'.format( result2.statistic, result2.pvalue))    
    st.bar_chart(data=group2['Hungarian Election'])

    