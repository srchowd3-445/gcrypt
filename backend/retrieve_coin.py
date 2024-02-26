import os

import requests
import datetime
# import sklearn
from datetime import datetime
import boto3
import random
import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

ddb = boto3.resource('dynamodb',
                     endpoint_url='http://localhost:8000',
                     region_name='dummy',
                     aws_access_key_id='dummy',
                     aws_secret_access_key='dummy')


def retrieve_coin(response, coin_name):
    print(response)
    dates = []
    prices = []
    for item in response['Items']:
        if(item['CoinName'] == coin_name):
            open_prices = item.get('Price', 'N/a')
            open_date = item.get('OpenDate', 'N/a')
            if open_prices is not None and open_date is not None:
                dates.append(open_date)
                prices.append(float(open_prices))


            print(open_prices)
    data = pd.DataFrame({'Date': dates, 'Price': prices})
    data['Date'] = pd.to_datetime(data['Date'])

    data['DateNumeric'] = (data['Date'] - data['Date'].min()).dt.days


    data = data.sort_values(by='Date').reset_index(drop=True)

    X = data[['DateNumeric']]
    y = data['Price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)


    y_pred = model.predict(X_test)

    plt.scatter(X_test, y_test, color='black', label='Actual prices')
    plt.plot(X_test, y_pred, color='blue', linewidth=3, label='Predicted prices')
    plt.xlabel('Date (Numeric)')
    plt.ylabel('Price')
    plt.title('Coin Price Prediction')
    plt.legend()
    # plt.show()
    current_script_path = os.path.dirname(__file__)
    target_directory = os.path.join(current_script_path, '..', 'frontend', 'static','js', 'images')
    os.makedirs(target_directory, exist_ok=True)
    file_name = 'coin_predict.png'
    full_path = os.path.join(target_directory, file_name)
    plt.savefig(full_path)


if __name__ == '__main__':
    table = ddb.Table('CoinData')
    response = table.scan(TableName='CoinData')

    coin_name = sys.argv[1]
    retrieve_coin(response, coin_name)
