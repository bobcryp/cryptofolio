import streamlit as st
import streamlit.components.v1 as com
import numpy as np
import lib_cryptofolio.get_price as gp
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

if 'data_price' not in st.session_state:
    st.session_state['data_price'] = gp.load_price()

with st.sidebar:
    st.session_state['data'].to_csv('tmp.csv',sep=';',index=False)
    st.download_button('Download .criptofolio',data=Path('tmp.csv').read_text(),file_name='mydata.criptofolio',key='uke-1')

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
            res=gp.get_price(pp, value='usd',data=st.session_state['data_price'])
            nb_value=nb_coin*res
            
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

    st.header('Summary for '+tk)

    if 'icon' not in os.listdir('.'):
        # open file
        file = tarfile.open('icon.tar.xz')
        # extracting file
        file.extractall('.')
        file.close()

    if tk.lower()+'.png' in os.listdir('icon'):
        st.image('icon/'+tk.lower()+'.png',width=50)
    

    df_tmp=pd.DataFrame(dict)
    st.dataframe(df_tmp)

    res_now=gp.get_price(tk, value='usd',data=st.session_state['data_price'])

    df_tk=st.session_state['data'].loc[st.session_state['data']['Pair1']==tk]
    
    df_tk=df_tk.sort_values(by=['Date'])
    
    cs=np.cumsum(df_tk['Quantities'])
    df_tk.insert(0,'Amont',cs.to_list())


    st.header('Trailing stop')
    c1,c2,c3 = st.columns(3)

    with c1 :    
        min_price=st.number_input("Minimum selling price",min_value=0.0,value=np.max([0.0,float(df_tmp['Average Token Buying Price'].astype('string')[0].split(' ')[0])*2.1]),format='%f')

    with c2:
        d_pc=st.number_input("Delta %",min_value=0.0,value=5.0)

    with c3:
        amt=st.number_input("Quantity to sell",min_value=0.0,value=float(df_tmp.Quantity.astype('string')[0].split(' ')[0])/2)

    c1b,c2b = st.columns(2)

    with c1b:
        value = min_price/(1-d_pc/100)
        st.metric('Trigger', value)

    with c2b:
        st.metric('Minimum income', amt*min_price)

    if len(cs)!=1:
        st.header('Quantity evolution')
        fig_amount = px.line(df_tk, x="Date", y="Amont", title='Evolution of the amont of '+tk)
        st.plotly_chart(fig_amount)

    st.header('Trading view chart')
    TW_html="""<!-- TradingView Widget BEGIN --><div class="tradingview-widget-container"><div id="tradingview_77c5b"></div><div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/"""+tk+"""USDT/?exchange=BINANCE" rel="noopener" target="_blank"><span class="blue-text">"""+tk+"""USDT Chart</span></a> by TradingView</div><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">new TradingView.widget({"width": 1500,"height": 700,"symbol": "BINANCE:"""+tk+"""USDT","interval": "D","timezone": "Etc/UTC","theme": "light","style": "1","locale": "en","toolbar_bg": "#f1f3f6","enable_publishing": false,"allow_symbol_change": true,"show_popup_button": true,"hide_side_toolbar": false,"container_id": "tradingview_77c5b"});</script></div><!-- TradingView Widget END -->"""    

    com.html(TW_html,width=1500,height=700)
