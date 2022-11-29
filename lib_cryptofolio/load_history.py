import pandas as pd
import datetime
from CryptoPrice import get_default_retriever
import re

def load_coinbasepro(adr):
    '''
    Coinbase Pro loading function from csv export
    '''
    tr_cp=pd.read_csv(adr)

    fd_cfolio=pd.DataFrame(columns=['Date','Type','Pair1','Pair2','Price','Quantities','Change_Dollar','Balance_Dollar'])

    retriever = get_default_retriever()

    for i in range(len(tr_cp)):
        time=datetime.datetime.fromisoformat(tr_cp.loc[i]['created at'][0:-5])
        pair1,pair2=tr_cp.loc[i]['product'].split('-')
        if pair1 != 'EUR':
            if pair2 in ['EUR','BUSD','USDC','USDT']:
                if pair2=='EUR':
                    res=retriever.get_closest_price(pair2, 'BUSD', int(time.timestamp()))
                    change=res.value
                else:
                    change=1

                tr_type=tr_cp.loc[i]['side']
                if tr_type=='SELL':
                    coeff=-1
                elif tr_type=='BUY':
                    coeff=1

                TP=float(tr_cp.loc[i]['price'])
                Q=float(coeff*tr_cp.loc[i]['size'])
                balance=float(-1*change*tr_cp.loc[i]['total'])

                dict= {'Date':[str(time)],
                        'Type':[tr_type],
                        'Pair1':[pair1.upper()],
                        'Pair2':[pair2.upper()],
                        'Price':[TP],
                        'Quantities':[Q],
                        'Change_Dollar':[change],
                        'Balance_Dollar':[balance]}
                ne=pd.DataFrame(dict)
                fd_cfolio=pd.concat([fd_cfolio,ne])
            else:
                change=retriever.get_closest_price(pair1.upper(),'BUSD', int(time.timestamp())).value 
                tr_type=tr_cp.loc[i]['side']
                if tr_type=='SELL':
                    coeff=-1
                elif tr_type=='BUY':
                    coeff=1
                Q=float(coeff*tr_cp.loc[i]['size'])
                dict= {'Date':[str(time)],
                    'Type':[tr_type],
                    'Pair1':[pair1.upper()],
                    'Pair2':['BUSD'],
                    'Price':[change],
                    'Quantities':[Q],
                    'Change_Dollar':[1],
                    'Balance_Dollar':[Q*change]}
                ne=pd.DataFrame(dict)
                fd_cfolio=pd.concat([fd_cfolio,ne])
                a=['BUY','SELL']
                a.remove(tr_type)
                tmp_tr=a[0]
                change2=retriever.get_closest_price(pair2.upper(),'BUSD', int(time.timestamp())).value 
                tQ=-1*Q*change/change2
                dict= {'Date':[str(time)],
                    'Type':[tmp_tr],
                    'Pair1':[pair2.upper()],
                    'Pair2':['BUSD'],
                    'Price':[change2],
                    'Quantities':[tQ],
                    'Change_Dollar':[1],
                    'Balance_Dollar':[tQ*change2]}
                ne=pd.DataFrame(dict)
                fd_cfolio=pd.concat([fd_cfolio,ne])

    return fd_cfolio

def load_binance(adr):
    '''
    Load Binance csv
    '''
    tr_cp=pd.read_csv(adr)

    fd_cfolio=pd.DataFrame(columns=['Date','Type','Pair1','Pair2','Price','Quantities','Change_Dollar','Balance_Dollar'])

    retriever = get_default_retriever()

    for i in range(len(tr_cp)):
        time=datetime.datetime.fromisoformat(tr_cp.loc[i]['Date(UTC)'])
        res1=re.split('(\d+)', tr_cp.loc[i]['Executed'].replace(',',''))
        pair1=res1[-1]
        v1=float(res1[1])+float('0.'+res1[3])
        res2=re.split('(\d+)', tr_cp.loc[i]['Amount'].replace(',',''))
        pair2=res2[-1]
        v2=float(res1[1])+float('0.'+res1[3])
        if pair1!='EUR':
            if pair2 in ['EUR','BUSD','USDC','USDT']:
                if pair2=='EUR':
                    res=retriever.get_closest_price(pair2, 'BUSD', int(time.timestamp()))
                    change=res.value
                else:
                    change=1

                tr_type=tr_cp.loc[i]['Side']
                if tr_type=='SELL':
                    coeff=-1
                elif tr_type=='BUY':
                    coeff=1

                TP=float(float(tr_cp.loc[i]['Price'].replace(',','')))
                Q=float(coeff*v1)
                balance=float(change*Q*TP)

                dict= {'Date':[str(time)],
                        'Type':[tr_type],
                        'Pair1':[pair1.upper()],
                        'Pair2':[pair2.upper()],
                        'Price':[TP],
                        'Quantities':[Q],
                        'Change_Dollar':[change],
                        'Balance_Dollar':[balance]}
                ne=pd.DataFrame(dict)
                fd_cfolio=pd.concat([fd_cfolio,ne])
            else:
                change=retriever.get_closest_price(pair1.upper(),'BUSD', int(time.timestamp())).value 
                tr_type=tr_cp.loc[i]['Side']
                if tr_type=='SELL':
                    coeff=-1
                elif tr_type=='BUY':
                    coeff=1
                Q=float(coeff*v1)
                dict= {'Date':[str(time)],
                    'Type':[tr_type],
                    'Pair1':[pair1.upper()],
                    'Pair2':['BUSD'],
                    'Price':[change],
                    'Quantities':[Q],
                    'Change_Dollar':[1],
                    'Balance_Dollar':[Q*change]}
                ne=pd.DataFrame(dict)
                fd_cfolio=pd.concat([fd_cfolio,ne])
                a=['BUY','SELL']
                a.remove(tr_type)
                tmp_tr=a[0]
                change2=retriever.get_closest_price(pair2.upper(),'BUSD', int(time.timestamp())).value 
                tQ=-1*Q*change/change2
                dict= {'Date':[str(time)],
                    'Type':[tmp_tr],
                    'Pair1':[pair2.upper()],
                    'Pair2':['BUSD'],
                    'Price':[change2],
                    'Quantities':[tQ],
                    'Change_Dollar':[1],
                    'Balance_Dollar':[tQ*change2]}
                ne=pd.DataFrame(dict)
                fd_cfolio=pd.concat([fd_cfolio,ne])

    return fd_cfolio