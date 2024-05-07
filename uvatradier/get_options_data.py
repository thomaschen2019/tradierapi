from options_data import OptionsData
token ='YKg3baGH2qF8dGfB79xt1Uxntb2l'
account = 'VA90020557'

if __name__ == '__main__':
    opt = OptionsData(account, token)
    #data = opt.get_expiry_dates('AAPL')
    #print("DATA is ", data)
    data = opt.get_chain_day('AAPL', expiry='2024-04-19')
    print(data)
    print(data.columns)