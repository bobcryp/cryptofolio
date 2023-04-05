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
    page_title="Trailing stop",
    page_icon="⬆️",
    layout="wide"
)

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date','Type','Pair1','Pair2','Price','Quantities','Change_Dollar','Balance_Dollar'])

if 'data_price' not in st.session_state:
    st.session_state['data_price'] = gp.load_price()

with st.sidebar:
    st.session_state['data'].to_csv('tmp.csv',sep=';',index=False)
    st.download_button('Download .criptofolio',data=Path('tmp.csv').read_text(),file_name='mydata.criptofolio',key='uke-1')

st.title('Trailing Stop !')


c1,c2,c3 = st.columns(3)

with c1 :    
    min_price=st.number_input("Minimum selling price")

with c2:
    d_pc=st.number_input("Delta %",min_value=0.0,value=5.0)

with c3:
    amt=st.number_input("Quantity to sell",min_value=0.0)

c1b,c2b = st.columns(2)

with c1b:
    value = min_price/(1-d_pc/100)
    st.metric('Trigger', value)

with c2b:
    st.metric('Minimum income', amt*min_price)