import streamlit as st
from CryptoPrice import get_default_retriever
import datetime
import pandas as pd
from pathlib import Path


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

retriever = get_default_retriever()

timestamp = int(full_time.timestamp())

# will return the first price price found close to the timestamp
res=retriever.get_closest_price(pair1.upper(), pair2.upper(), timestamp)

if res is None :
    st.warning('Transaction Pair not available !')
elif pair1!='' and pair2!='':
    st.header('Adjust transaction price')
    TP=st.number_input('True Price', value=res.value,format='%f')
    Q=st.number_input('Quantities',format='%f')
    
    if pair2.upper() in ['EUR','USDC','USDT','BUSD']:
        if pair2.upper()=='EUR':
            change=retriever.get_closest_price(pair2.upper(),'BUSD', timestamp).value
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
                
            change=retriever.get_closest_price(pair1.upper(),'BUSD', timestamp).value 
            dict= {'Date':[full_time],
                'Type':[tr_type],
                'Pair1':[pair1.upper()],
                'Pair2':['BUSD'],
                'Price':[change],
                'Quantities':[coeff*Q],
                'Change_Dollar':[1],
                'Balance_Dollar':[coeff*Q*change]}
            ne=pd.DataFrame(dict)
            st.session_state['data']=pd.concat([st.session_state['data'],ne])
            a=['Buy','Sell']
            a.remove(tr_type)
            tmp_tr=a[0]
            change2=retriever.get_closest_price(pair2.upper(),'BUSD', timestamp).value 
            tQ=-1*coeff*Q*change/change2
            dict= {'Date':[full_time],
                'Type':[tmp_tr],
                'Pair1':[pair2.upper()],
                'Pair2':['BUSD'],
                'Price':[change2],
                'Quantities':[tQ],
                'Change_Dollar':[1],
                'Balance_Dollar':[tQ*change2]}
            ne=pd.DataFrame(dict)
            st.session_state['data']=pd.concat([st.session_state['data'],ne])
