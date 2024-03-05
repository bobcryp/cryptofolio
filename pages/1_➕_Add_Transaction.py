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

print(st.session_state['data'])

# List of crypto available
symbol_list = [d['symbol'] for d in st.session_state['data_price']]
symbol_list_2 = []
symbol_list_2.append('eur')
symbol_list_2.append('usdt')

if tr_type=='Buy':
    tr_type2='From'
    coeff=1
elif tr_type=='Sell':
    tr_type2='To'
    coeff=-1

pair1=st.selectbox(tr_type,symbol_list)
pair2=st.selectbox(tr_type2,symbol_list_2,index=0)

st.header('Transaction date')

t_date=st.date_input('Transaction date')
t_time=st.time_input('Transaction time')

full_time=datetime.datetime.combine(t_date, t_time)

res=st.session_state['data_price'][symbol_list.index(pair1)]['current_price']
if pair2=='eur':
    res=res/st.session_state['change']
if res == -1 :
    st.warning('Transaction Pair not available !')
elif pair1!='' and pair2!='':
    st.header('Adjust transaction price')
    TP=st.number_input('True Price', value=res,format='%f')
    Q=st.number_input('Quantities',format='%f')
    


        
if st.button('Add Transaction'):
    
    if pair2.upper() in ['EUR']:
        change=st.session_state['change']
    else:
        change=1

    dict= {'Date':[full_time],
        'Type':[tr_type],
        'Pair1':[pair1.upper()],
        'Pair2':['USDT'],
        'Price':[TP*change],
        'Quantities':[coeff*Q],
        'Balance_Dollar':[coeff*TP*Q*change]}
    
    ne=pd.DataFrame(dict)
    st.session_state['data']=pd.concat([st.session_state['data'],ne])

    if pair2.upper() in ['EUR']:
        dict= {'Date':[full_time],
        'Type':[tr_type],
        'Pair1':['USDT'],
        'Pair2':['EUR'],
        'Price':[change],
        'Quantities':[coeff*TP*Q*change],
        'Balance_Dollar':[coeff*TP*Q*change]}
    
        ne=pd.DataFrame(dict)
        st.session_state['data']=pd.concat([st.session_state['data'],ne])

    st.success('You '+tr_type.lower()+' '+str(Q)+' '+pair1.upper()+' for '+str(Q*TP)+' '+pair2.upper()+' or '+str(Q*TP*change)+'$ !')

        