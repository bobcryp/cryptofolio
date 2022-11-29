import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="CryptoFolio",
    page_icon="₿",
)

st.title('Welcome to CryptoFolio')
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

with st.sidebar:
    st.session_state['data'].to_csv('tmp.csv',sep=';',index=False)
    st.download_button('Download .criptofolio',data=Path('tmp.csv').read_text(),file_name='mydata.criptofolio',key='uke-1')
