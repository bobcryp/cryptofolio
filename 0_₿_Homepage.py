import streamlit as st
import pandas as pd
from pathlib import Path
import lib_cryptofolio.get_price as gp

st.set_page_config(
    page_title="CryptoFolio",
    page_icon="₿",
)

st.title('Welcome to CryptoFolio')

if 'data_price' not in st.session_state:
    st.session_state['data_price'] = gp.load_price()

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date','Type','Pair1','Pair2','Price','Quantities','Change_Dollar','Balance_Dollar'])
st.write('This web app is meant to follow the state of your crypto currency investment.')

st.header('Data policy')
st.write('The app is open source and does not keep any track of our crypto folio. Feel free to check the source code if you have any doubt !')

st.header('Upload your data')
st.write('As no data are track you need to upload your record if you have one otherwise start using the app.')
uploaded_file = st.file_uploader("Choose a file",type='criptofolio')
with st.spinner():
    if uploaded_file is not None:
        st.session_state['data'] = pd.read_csv(uploaded_file,sep=';')
        st.success('Data downloaded')

#st.header('Update data from exchange')
#ex_op=st.selectbox('Exchange',['Binance','Coinbase Pro'])
#uploaded_Ex = st.file_uploader("Choose csv from "+ex_op,type='csv')
#with st.spinner():    
#    if uploaded_Ex is not None:
#        if ex_op=='Binance':
#            data_new=fc.load_binance(uploaded_Ex)
#            st.session_state['data']=pd.concat([st.session_state['data'],data_new])
#        elif ex_op=='Coinbase Pro':
#            data_new=fc.load_coinbasepro(uploaded_Ex)
#            st.session_state['data']=pd.concat([st.session_state['data'],data_new])


with st.sidebar:
    st.session_state['data'].to_csv('tmp.csv',sep=';',index=False)
    st.download_button('Download .criptofolio',data=Path('tmp.csv').read_text(),file_name='mydata.criptofolio',key='uke-1')
