import streamlit as st
import lib_cryptofolio.get_price as gp
import datetime
import pandas as pd
from pathlib import Path

if 'data_price' not in st.session_state:
    st.session_state['data_price'] = gp.load_price()

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date','Type','Pair1','Pair2','Price','Quantities','Change_Dollar','Balance_Dollar'])

st.set_page_config(
    page_title="Add Transaction",
    page_icon="➕",
)

with st.sidebar:
    st.session_state['data'].to_csv('tmp.csv',sep=';',index=False)
    st.download_button('Download .criptofolio',data=Path('tmp.csv').read_text(),file_name='mydata.criptofolio',key='uke-1')

st.title('Add a Transaction')
st.header('Select Pair')
tr_type=st.radio('Type',['Buy','Sell'],horizontal=True)

if tr_type=='Buy':
    tr_type2='From'
    coeff=1
elif tr_type=='Sell':
    tr_type2='To'
    coeff=-1

pair1=st.text_input(tr_type)
pair2=st.text_input(tr_type2)

st.header('Transaction date')

t_date=st.date_input('Transaction date')
t_time=st.time_input('Transaction time')

full_time=datetime.datetime.combine(t_date, t_time)

res=gp.get_price(pair1.upper(), value=pair2,data=st.session_state['data_price'])

if res == -1 :
    st.warning('Transaction Pair not available !')
elif pair1!='' and pair2!='':
    st.header('Adjust transaction price')
    TP=st.number_input('True Price', value=res,format='%f')
    Q=st.number_input('Quantities',format='%f')
    
    if pair2.upper() in ['EUR','USDC','USDT','BUSD','TUSD','FDUSD']:
        if pair2.upper()=='EUR':
            change=gp.get_price('EUR',data=st.session_state['data_price'])
        else:
            change=1
        
        if st.button('Add Transaction'):
            st.success('You '+tr_type.lower()+' '+str(Q)+' '+pair1.upper()+' for '+str(Q*TP)+' '+pair2.upper()+' or '+str(Q*TP*change)+'$ !')
            dict= {'Date':[full_time],
                'Type':[tr_type],
                'Pair1':[pair1.upper()],
                'Pair2':[pair2.upper()],
                'Price':[TP],
                'Quantities':[coeff*Q],
                'Change_Dollar':[change],
                'Balance_Dollar':[coeff*TP*Q*change]}
            
            ne=pd.DataFrame(dict)
            st.session_state['data']=pd.concat([st.session_state['data'],ne])
    else:
        if st.button('Add Transaction'):
            st.success('You '+tr_type.lower()+' '+str(Q)+' '+pair1.upper()+' for '+str(Q*TP)+' '+pair2.upper()+' !')
                
            change=gp.get_price(pair1,data=st.session_state['data_price'])
            dict= {'Date':[full_time],
                'Type':[tr_type],
                'Pair1':[pair1.upper()],
                'Pair2':['USDT'],
                'Price':[change],
                'Quantities':[coeff*Q],
                'Change_Dollar':[1],
                'Balance_Dollar':[coeff*Q*change]}
            ne=pd.DataFrame(dict)
            st.session_state['data']=pd.concat([st.session_state['data'],ne])
            a=['Buy','Sell']
            a.remove(tr_type)
            tmp_tr=a[0]
            change2=gp.get_price(pair2,data=st.session_state['data_price'])
            tQ=-1*coeff*Q*change/change2
            dict= {'Date':[full_time],
                'Type':[tmp_tr],
                'Pair1':[pair2.upper()],
                'Pair2':['USDT'],
                'Price':[change2],
                'Quantities':[tQ],
                'Change_Dollar':[1],
                'Balance_Dollar':[tQ*change2]}
            ne=pd.DataFrame(dict)
            st.session_state['data']=pd.concat([st.session_state['data'],ne])
