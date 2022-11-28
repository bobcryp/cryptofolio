import streamlit as st
import streamlit.components.v1 as com
import numpy as np
from CryptoPrice import get_default_retriever
import datetime
import pandas as pd
import plotly.express as px
from pathlib import Path
import os
import tarfile

st.set_page_config(
    page_title="Token Analysis",
    page_icon="💰",
    layout="wide"
)

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date','Type','Pair1','Pair2','Price','Quantities','Change_Dollar','Balance_Dollar'])

with st.sidebar:
    st.session_state['data'].to_csv('tmp.csv',sep=';')
    st.download_button('Download .criptofolio',data=Path('tmp.csv').read_text(),file_name='mydata.criptofolio',key='uke-1')

retriever = get_default_retriever()
st.title('Token analysis !')

if len(st.session_state['data'])==0:
    st.warning('No transaction record yet !')
else:
    df_total=pd.DataFrame(columns=['Coin','Amount','Cost','Price'])
    
    with st.spinner('Wait for it ...'):
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
                'Price':[nb_value]
            }

            tmp_c=pd.DataFrame(dict)
            tmp_c=tmp_c.round(4)
            df_total=pd.concat([df_total,tmp_c])
    

    list_token=sorted(list(set(list(df_total['Coin']))))
    tk=st.selectbox('Token',list_token)
    id_tk=df_total['Coin']==tk

    if float(df_total['Cost'].loc[id_tk])<=0:
        tmp_G='G: '+str(round(-float(df_total['Cost'].loc[id_tk]),1))+' $'
    else:
        tmp_G=str(round((float(df_total['Price'].loc[id_tk])/float(df_total['Cost'].loc[id_tk])-1)*100,2))+' %'

    dict={'Quantity':[str(round(float(df_total['Amount'].loc[id_tk]),2))+' '+tk],
          'Actual Value':[str(round(float(df_total['Price'].loc[id_tk]),2))+' $'],
          'Average Token Buying Price':[str(round(float(df_total['Cost'].loc[id_tk])/float(df_total['Amount'].loc[id_tk]),4))+' $'],
          'Actual Token Value':[str(round(float(df_total['Price'].loc[id_tk])/float(df_total['Amount'].loc[id_tk]),4))+' $'],
          'Gain/loss': [tmp_G]
    }
    
    df_tmp=pd.DataFrame(dict)
    st.dataframe(df_tmp)

    period=st.radio('Period :',['Year','Month','Week','Day','Hour'],horizontal=True,index=3)

    if period=='Year':
        delta_t=365.24*24*3600
    elif period=='Month':
        delta_t=30.44*24*3600
    elif period=='Week':
        delta_t=7*24*3600
    elif period=='Day':
        delta_t=24*3600
    elif period=='Hour':
        delta_t=3600
        
    
    timestamp=datetime.datetime.today().timestamp()
    res_now=retriever.get_closest_price(tk, 'BUSD', int(timestamp))
    res_delta=retriever.get_closest_price(tk, 'BUSD', int(timestamp-delta_t))

    df_tk=st.session_state['data'].loc[st.session_state['data']['Pair1']==tk]
    
    df_tk=df_tk.sort_values(by=['Date'])
    
    cs=np.cumsum(df_tk['Quantities'])
    df_tk.insert(0,'Amont',cs.to_list())

    if 'icon' not in os.listdir('.'):
        # open file
        file = tarfile.open('icon.tar.xz')
        # extracting file
        file.extractall('.')
        file.close()

    if tk.lower()+'.png' in os.listdir('icon'):
        st.image('icon/'+tk.lower()+'.png',width=50)
    
    #st.image(response,width=50)

    st.metric(tk, str(round(res_now.value,4))+' $', delta=str(round(res_now.value/res_delta.value-1,4)*100)+' %', delta_color="normal", help=None)

    if len(cs)!=1:
        fig_amount = px.line(df_tk, x="Date", y="Amont", title='Evolution of the amont of '+tk)
        st.plotly_chart(fig_amount)

    TW_html="""<!-- TradingView Widget BEGIN --><div class="tradingview-widget-container"><div id="tradingview_77c5b"></div><div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/"""+tk+"""BUSD/?exchange=BINANCE" rel="noopener" target="_blank"><span class="blue-text">"""+tk+"""BUSD Chart</span></a> by TradingView</div><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">new TradingView.widget({"width": 1500,"height": 700,"symbol": "BINANCE:"""+tk+"""BUSD","interval": "D","timezone": "Etc/UTC","theme": "light","style": "1","locale": "en","toolbar_bg": "#f1f3f6","enable_publishing": false,"allow_symbol_change": true,"show_popup_button": true,"container_id": "tradingview_77c5b"});</script></div><!-- TradingView Widget END -->"""    

    com.html(TW_html,width=1500,height=700)