import streamlit as st
import numpy as np
import lib_cryptofolio.get_price as gp
import datetime
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="CryptoFolio Summary",
    page_icon="📈",
    layout="wide"
)

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date','Type','Pair1','Pair2','Price','Quantities','Change_Dollar','Balance_Dollar'])

if 'data_price' not in st.session_state:
    st.session_state['data_price'] = gp.coingecko_data()

with st.sidebar:
    st.session_state['data'].to_csv('tmp.csv',sep=';',index=False)
    st.download_button('Download .criptofolio',data=Path('tmp.csv').read_text(),file_name='mydata.criptofolio',key='uke-1')

st.title('CrypoFolio visualisation !')

if len(st.session_state['data'])==0:
    st.warning('No transaction record yet !')
else:    
    total_invest=np.sum(st.session_state['data']['Balance_Dollar'])

    df_total=pd.DataFrame(columns=['Coin','Amount','Cost','Price'])
    
    balance_usdt=0
    balance_eur=0
    
    for i in range(len(st.session_state['data'])):
        if (list(st.session_state['data']['Pair1'])[i]=='USDT'):
            balance_usdt+=list(st.session_state['data']['Balance_Dollar'])[i]
        if (list(st.session_state['data']['Pair2'])[i]=='EUR'):
            balance_eur+=-1*list(st.session_state['data']['Balance_Dollar'])[i]/list(st.session_state['data']['Price'])[i]
        if (list(st.session_state['data']['Pair2'])[i]=='USDT'):
            balance_usdt+=-1*list(st.session_state['data']['Balance_Dollar'])[i]
        
    for pp in set(list(st.session_state['data']['Pair1'])):
        tmp_c=[pp,0]
        df=st.session_state['data'].query("Pair1 == @pp")
        nb_coin=np.sum(df['Quantities'])
        nb_price=np.sum(df['Balance_Dollar'])
        res=gp.get_price(pp,st.session_state['data_price'])
        nb_value=nb_coin*res
        
        if pp not in ['EUR','USDT']:
            dict={'Coin':[pp],
                'Amount':[nb_coin],
                'Cost':[nb_price],
                'Price':[nb_value]}

            tmp_c=pd.DataFrame(dict)
            df_total=pd.concat([df_total,tmp_c])

    st.header('Total')
    df_total=df_total.sort_values(by=['Price'],ascending=False)
    if np.sum(df_total['Cost'])<=0:
        delta_all='G: '+str(-1*round(np.sum(df_total['Cost']),1))+' $'
    else:
        delta_all=str(round(((np.sum(df_total['Price']))/np.sum(df_total['Cost'])-1)*100,1))+' %'
    
    col = st.columns(3)
    tmp=col[0]
    tmp.metric('Crypto', str(round(np.sum(df_total['Price'])))+' $', delta=delta_all, delta_color="normal", help=None)
    tmp=col[1]
    tmp.metric('USDT', str(round(balance_usdt))+' $', delta=None, delta_color="normal", help=None)
    tmp=col[2]
    tmp.metric('EUR', str(round(balance_eur))+' €', delta=None, delta_color="normal", help=None)



    st.header('Token')
    col = st.columns(5)
    for i in range(len(df_total)):
        tmp=col[i%5]
        if np.sum(df_total['Cost'].iloc[i])<=0:
            delta_tmp_all='G: '+str(-1*round(np.sum(df_total['Cost'].iloc[i]),1))+' $'
        else:
            delta_tmp_all=str(round((df_total['Price'].iloc[i]/df_total['Cost'].iloc[i]-1)*100,1))+' %'
        
        tmp.metric(df_total['Coin'].iloc[i], str(round(df_total['Price'].iloc[i]))+' $', delta=delta_tmp_all, delta_color="normal", help=None)

    col = st.columns(2)
    fig_invest = px.pie(df_total, values='Cost', names='Coin', color='Coin')
    fig_value = px.pie(df_total, values='Price', names='Coin', color='Coin')
    col[0].subheader('Buying price')
    col[0].plotly_chart(fig_invest)
    col[1].subheader('Actual value')
    col[1].plotly_chart(fig_value)

    