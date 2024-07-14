import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

class TimeSeries:
    def __init__(self, data):
        self.data = data

    def forecast(self, start_year: str, end_year: str):
        self.start_year = start_year
        self.end_year = end_year

        # Load data
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

        model_fit = model.fit(disp=False)

        # Create future date range
        future_dates = pd.date_range(start=self.start_year, end=self.end_year, freq='D')
        future_df = pd.DataFrame(index=future_dates, columns=subset.columns)

        # Concatenate train, test, and future data
        combined_df = pd.concat([subset, future_df])

        # Make predictions
        predictions = model_fit.predict(start=len(train), end=len(train) + len(test) + len(future_dates) - 1)
        combined_df['prediction'] = predictions.values
        # Calculate evaluation metrics
        # test_predictions = combined_df.loc[test.index, 'prediction']
        # mae = mean_absolute_error(test['MaxPrice (Rs./Kg)'], test_predictions)
        # mse = mean_squared_error(test['MaxPrice (Rs./Kg)'], test_predictions)
        # mape = np.mean(np.abs((test['MaxPrice (Rs./Kg)'] - test_predictions) / test['MaxPrice (Rs./Kg)'])) * 100
        # r2 = r2_score(test['MaxPrice (Rs./Kg)'], test_predictions)

        # print(f'MAPE: {mape}%')
        # print(f'R²: {r2}')
        # print(f'MAE: {mae}, MSE: {mse}')

        # Plot existing data and predictions
        plt.plot(subset.index, subset['MaxPrice (Rs./Kg)'], label='Existing data', color='blue')
        plt.plot(combined_df.index, combined_df['prediction'], label='Predicted data', color='red')
        plt.xlabel('Date')
        plt.ylabel('Price (Rs./Kg)')
        plt.title('Price Forecast')
        plt.legend()
        plt.grid(True)
        plt.show()

# Example usage
test = TimeSeries('cardamom data.xlsx')
test.forecast('2025-01-01', '2025-12-01')
