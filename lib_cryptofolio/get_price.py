from pycoingecko import CoinGeckoAPI
import datetime

def get_price(sym,date=None,value='usd',data=None):
    cg = CoinGeckoAPI()
    hard_find={'UNI':'uniswap',
           'FLUX':'zelcash',
           'BIT':'bitdao',
           'CHSB':'swissborg',
           'DGB':'digibyte',
           'EUR':'tether-eurt',
           'SOL':'solana',
           'ADA':'cardano',
           'BTC':'bitcoin',
           'ETH':'ethereum',
           'SHIB':'shiba-inu',
           'DOT':'polkadot',
           'AVAX':'avalanche-2',
           'NEAR':'near',
           'DOGE':'dogecoin',
           'GRT':'the-graph',
           'FIL':'filecoin',
           'FTM':'fantom',
           'CHZ':'chiliz',
           'ATOM':'cosmos',
           'HFT':'hashflow',
           'EGLD':'elrond-erd-2',
           'CSPR':'casper-network',
           'LTC':'litecoin',
           'FTT':'ftx-token',
           'MANA':'decentraland',      
           'JASMY':'jasmycoin',
           'BURGER':'burger-swap',
           'BNB':'binancecoin',
           'XRP':'ripple',
           'MATIC':'matic-network',
           'TRX':'tron',
           'UNI':'uniswap',
           'LINK':'chainlink',
           'ETC':'ethereum-classic',
           'ALGO':'algorand',
           'QNT':'quant-network',
           'AAVE':'aave',
           'SAND':'the-sandbox',
           'CAKE':'pancakeswap-token',
           'CRO':'crypto-com-chain',
           'BAT':'basic-attention-token',
           'ENJ':'enjincoin',
           'SUCHI':'sushi',
           'ERN':'ethernity-chain',
           'ONE':'harmony',
           'XTZ':'tezos'
          }

    if data is not None:
        if sym.upper() in hard_find:
            if value.lower() not in ['btc','eth','usd','eur','busd','usdt','usdc']:
                return -1
            if value.lower() in ['busd','usdt','usdc']:
                value='usd'
            if date is None:
                res=data[hard_find[sym]][value.lower()]
            else:
                return -1
        else:
            return -1
    else:    
        if value.lower() not in ['btc','eth','usd','eur','busd','usdt','usdc']:
            return -1
        if value in ['busd','usdt','usdc']:
            value='usd'

        if sym.upper() in hard_find:
            id=hard_find[sym]
        else:
            ll=cg.search(query=sym)
            if len(ll['coins'])!=0:
                id=ll['coins'][0]['id']
            else:
                return -1

        if date is not None:    
            data = cg.get_coin_history_by_id(id=id,date=datetime.datetime.fromtimestamp(int(date)).date().strftime('%d-%m-%Y'), localization='false')
            res=data['market_data']['current_price'][value]
        else:
            res=cg.get_price(ids=id, vs_currencies=value.lower())[id][value.lower()]
            
    return res

def load_price():
    cg = CoinGeckoAPI()
    hard_find={'UNI':'uniswap',
           'FLUX':'zelcash',
           'BIT':'bitdao',
           'CHSB':'swissborg',
           'DGB':'digibyte',
           'EUR':'tether-eurt',
           'SOL':'solana',
           'ADA':'cardano',
           'BTC':'bitcoin',
           'ETH':'ethereum',
           'SHIB':'shiba-inu',
           'DOT':'polkadot',
           'AVAX':'avalanche-2',
           'NEAR':'near',
           'DOGE':'dogecoin',
           'GRT':'the-graph',
           'FIL':'filecoin',
           'FTM':'fantom',
           'CHZ':'chiliz',
           'ATOM':'cosmos',
           'HFT':'hashflow',
           'EGLD':'elrond-erd-2',
           'CSPR':'casper-network',
           'LTC':'litecoin',
           'FTT':'ftx-token',
           'MANA':'decentraland',      
           'JASMY':'jasmycoin',
           'BURGER':'burger-swap',
           'BNB':'binancecoin',
           'XRP':'ripple',
           'MATIC':'matic-network',
           'TRX':'tron',
           'UNI':'uniswap',
           'LINK':'chainlink',
           'ETC':'ethereum-classic',
           'ALGO':'algorand',
           'QNT':'quant-network',
           'AAVE':'aave',
           'SAND':'the-sandbox',
           'CAKE':'pancakeswap-token',
           'CRO':'crypto-com-chain',
           'BAT':'basic-attention-token',
           'ENJ':'enjincoin',
           'SUCHI':'sushi',
           'ERN':'ethernity-chain',
           'ONE':'harmony',
           'XTZ':'tezos'
          }
    id_cg=[]
    for i in list(hard_find):
        id_cg.append(hard_find[i])

    return cg.get_price(ids=id_cg, vs_currencies=['usd','eur','btc','eth'])
