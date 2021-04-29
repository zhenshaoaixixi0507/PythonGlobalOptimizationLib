from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np

def GetYahooFinanceData(ticker:str,startdate:str,enddate:str,timeinterval:str,datatype:str)->np.ndarray:
 yahoo_financials = YahooFinancials(ticker)
 data = yahoo_financials.get_historical_price_data(start_date=startdate, 
                                                  end_date=enddate, 
                                                  time_interval=timeinterval)
 df = pd.DataFrame(data[ticker]['prices'])
 return df[datatype].to_numpy()
