import requests
import pandas as pd
token = 'WPvbz4499sNKh533AL7S0TAcr1qP'

def get_option_chain(symbol, expiry, greeks=False):

    response = requests.get('https://api.tradier.com/v1/markets/options/chains',
        params={'symbol': symbol, 'expiration': expiry, 'greeks': 'true'},
        headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
    )
    options = response.json()['options']['option']
    if greeks:
        lst = []
        for option in options:
            lst.append({**option, **option['greeks']})
        df = pd.DataFrame(lst)
    else:
        df = pd.DataFrame(response.json()['options']['option'])
    return df
def get_trades(symbol, start, end):
    response = requests.get('https://api.tradier.com/v1/markets/timesales',
    params={'symbol': symbol, 'interval': 'tick', 'start': start, 'end': end, 'session_filter': 'all'},
    headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
)
    return pd.DataFrame(response.json()['series']['data'])

def get_option_expirations(symbol):
    response = requests.get('https://api.tradier.com/v1/markets/options/expirations',
    params={'symbol': symbol, 'includeAllRoots': 'true', 'strikes': 'true', 'contractSize': 'true', 'expirationType': 'true'},
    headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
)
    return [x['date'] for x in response.json()['expirations']['expiration']]

def get_quote(symbol, start, end):
    response = requests.get('https://api.tradier.com/v1/markets/history',
        params={'symbol': symbol, 'interval': 'daily', 'start': start, 'end': end, 'session_filter': 'all'},
        headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
    )
    json_response = response.json()
    print(json_response)

def get_all_options(symbol):
    expirations = get_option_expirations(symbol)
    lst = []
    for exp in expirations:
        chain = get_option_chain(symbol, exp, greeks=True)
        lst.append(chain)
    return pd.concat(lst)
if __name__ == '__main__':
    ticker = 'ENPH'
    odf = get_all_options(ticker)
    odf.to_csv(f'{ticker}_options.csv', index=False)
    print(odf.sort_values('volume', ascending=False).head(10))
    # end = '2024-02-29 16:00'
    # start = '2024-02-28 16:00'
    # trades = get_trades('DQ240315C00022500', start, end)
    # print(trades.sort_values('volume', ascending=False).head(20))
    # print(trades.groupby('time').volume.sum().sort_values(ascending=False).head(10))
    # chain = get_option_chain('JOBY', '2025-01-17', greeks=True)
    # columns = ['symbol', 'option_type', 'bid', 'ask', 'volume',  'open_interest', 'strike', 'underlying', 'delta', 'gamma', 'theta', 'vega', 'bid_iv', 'mid_iv', 'ask_iv', 'smv_vol']
    # chain = chain[abs(chain['delta']) > 0.05]
    # chain = chain[abs(chain['delta']) < 0.95]
    # print(chain[columns])
    # print(chain.columns)
    #get_quote('AAPL240419C00200000', '2024-01-19', '2024-02-19')
