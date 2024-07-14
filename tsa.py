"""
Time Series Analysis
@author:Raynell Rajeev

"""

class TimeSeries:
    def __init__(self, data:str):
        self.data=data
    
    
    def forecast(self, start_year:str, end_year:str):

        import pandas as pd
        import matplotlib.pyplot as plt
        from statsmodels.tsa.statespace.sarimax import SARIMAX
    
        self.start_year = start_year
        self.end_year = end_year

        df = pd.read_excel(self.data)
        df['Date of Auction'] = pd.to_datetime(df['Date of Auction'])
        #df.set_index('Date of Auction', inplace=True)
        subset = df.reset_index()[['Date of Auction', 'MaxPrice (Rs./Kg)']]
        subset['firstdiff'] = subset['MaxPrice (Rs./Kg)'].diff()
        subset['diff12'] = subset['MaxPrice (Rs./Kg)'].diff(12)
        subset = subset.sort_values(by='Date of Auction', ascending=True).reset_index(drop=True)
        
        train = subset[:round(len(subset) * 70 / 100)]
        test = subset[round(len(subset) * 70 / 100):]

        model = SARIMAX(
            train['MaxPrice (Rs./Kg)'],
            order=(1, 1, 2),
            seasonal_order=(1, 1, 1, 12)
        )
        
        futureDate=pd.DataFrame(pd.date_range(start=self.start_year,end=self.end_year,freq='D'),columns=['Dates'])
        
        # # Convert start and end dates to timestamps
        start_date = futureDate.index[0]
        end_date = futureDate.index[-1]

        prediction = model.fit(disp=False).predict(
            start=start_date,
            end=end_date
        )

        subset['prediction'] = prediction
        
        plt.plot(subset.index, subset['MaxPrice (Rs./Kg)'], label='existing data', color='blue')
        plt.plot(subset.index, subset['prediction'], label='predicted data', color='red')
        plt.xlabel('Date')
        plt.ylabel('Price (Rs./Kg)')
        plt.title('Price Forecast')
        plt.legend()
        plt.grid(True)
        plt.show()

 
test=TimeSeries('cardamom data.xlsx')
test.forecast('2025-01-01',
              '2025-12-01')