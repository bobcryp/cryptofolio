import streamlit as st
import numpy as np
from CryptoPrice import get_default_retriever
import datetime
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Data Visualisation",
    page_icon="🗠",
)

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date','Type','Pair1','Pair2','Price','Quantities','Change_Dollar','Balance_Dollar'])

with st.sidebar:
    st.session_state['data'].to_csv('tmp.csv',sep=';')
    st.download_button('Download .criptofolio',data=Path('tmp.csv').read_text(),file_name='mydata.criptofolio',key='uke-1')

retriever = get_default_retriever()
st.title('CrypoFolio visualisation !')

if len(st.session_state['data'])==0:
    st.warning('No transaction record yet !')
else:    
    total_invest=np.sum(st.session_state['data']['Balance_Dollar'])

    df_total=pd.DataFrame(columns=['Coin','Amount','Cost','Price'])
    df_total=df_total.sort_values(by=['Price'])
    
    for pp in set(list(st.session_state['data']['Pair1'])):
        tmp_c=[pp,0]
        df=st.session_state['data'].query("Pair1 == @pp")
        nb_coin=np.sum(df['Quantities'])
        nb_price=np.sum(df['Balance_Dollar'])
        timestamp=datetime.datetime.today().timestamp()
        res=retriever.get_closest_price(pp, 'BUSD', int(timestamp))
        nb_value=nb_coin*res.value
        
        dict={'Coin':[pp],
            'Amount':[nb_coin],
            'Cost':[nb_price],
            'Price':[nb_value]}

        tmp_c=pd.DataFrame(dict)
        df_total=pd.concat([df_total,tmp_c])

    st.header('Total')

    st.metric('All crypto', str(round(np.sum(df_total['Price'])))+' $', delta=str(round((np.sum(df_total['Price'])/np.sum(df_total['Cost'])-1)*100,4))+' %', delta_color="normal", help=None)

    st.header('Token')
    col = st.columns(3)
    for i in range(len(df_total)):
        tmp=col[i%3]
        tmp.metric(df_total['Coin'].iloc[i], str(round(df_total['Price'].iloc[i]))+' $', delta=str(round((df_total['Price'].iloc[i]/df_total['Cost'].iloc[i]-1)*100,4))+' %', delta_color="normal", help=None)

    col = st.columns(2)
    fig_invest = px.pie(df_total, values='Cost', names='Coin')
    fig_value = px.pie(df_total, values='Price', names='Coin')
    col[0].subheader('Buying price')
    col[0].plotly_chart(fig_invest)
    col[1].subheader('Actual value')
    col[1].plotly_chart(fig_value)

    st.header('Info about one token')
    tk=st.selectbox('Token',set(list(st.session_state['data']['Pair1'])))
    i=list(set(list(st.session_state['data']['Pair1']))).index(tk)
    st.metric(df_total['Coin'].iloc[i], str(round(df_total['Price'].iloc[i]))+' $', delta=str(round((df_total['Price'].iloc[i]/df_total['Cost'].iloc[i]-1)*100,4))+' %', delta_color="normal", help=None)

    df_tk=st.session_state['data'].loc[st.session_state['data']['Pair1']==tk]
    df_tk=df_tk.sort_values(by=['Date'])
    cs=np.cumsum(df_tk['Quantities'])
    df_tk.insert(0,'Amont',cs.to_list())
    st.success('You have: '+str(cs.to_numpy()[-1])+' '+tk)
    if len(cs)!=1:
        fig_amount = px.line(df_tk, x="Date", y="Amont", title='Evolution of the amont of '+tk)
        st.plotly_chart(fig_amount)
