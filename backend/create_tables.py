import requests
import datetime
# import sklearn
from datetime import datetime
import boto3
import random


"""
Tables are created here using Dynamo DB to store coin information.
"""
ddb = boto3.resource('dynamodb',
                     endpoint_url='http://localhost:8000',
                     region_name='dummy',
                     aws_access_key_id='dummy',
                     aws_secret_access_key='dummy')

def create_tables():
    ddb.create_table(TableName='CoinData',
                     AttributeDefinitions=[
                         {
                             'AttributeName': 'CoinId',
                             'AttributeType': 'N'
                         },
                     ],
                     KeySchema=[
                         {
                             'AttributeName': 'CoinId',
                             'KeyType': 'HASH'
                         },
                     ],
                     ProvisionedThroughput={
                         'ReadCapacityUnits': 100,
                         'WriteCapacityUnits': 100
                     }
                     )
    print("Successfully created Table")


def retrieve_and_store(mock_hashmap, coin):
    table = ddb.Table('CoinData')
    coin_name = coin
    for open_date, price in mock_hashmap.items():
        random_number = random.randint(1,10000)
        table.put_item(
            TableName='CoinData',
            Item= {
                'CoinId':random_number,
                'OpenDate': open_date.strftime("%Y-%m-%d"),
                'Price':str(price),
                'CoinName': coin_name
            }
        )
        print(f"Open Date inserted: ", open_date, "Price inserted: ", price)
    print("Data input complete.")


    response = table.scan(TableName='CoinData')

    return response


"""
Rest API utilised to retrieve coin information.
"""
def fetch_ohlcv(coin):
    #[:46] [53:]
    url = "https://rest.coinapi.io/v1/ohlcv/BINANCE_SPOT_/history?period_id=1MTH&time_start=2023-03-01T00:00:00"
    url = url[: 46] + coin + "/history?period_id=1MTH&time_start=2023-03-01T00:00:00"
    headers = {"X-CoinAPI-Key": "EE231F2F-3F8E-46FA-8F89-2EC4DA572061"}  # Replace with your API key

    print(url)
    response = requests.get(url, headers=headers)


    #Check if the response is successful
    if response.status_code == 200:
        if response.content:
            prices_by_date = {
                datetime.strptime(entry['time_open'], "%Y-%m-%dT%H:%M:%S.%f0Z").date(): entry['price_open'] for entry in
                response.json()}
            return prices_by_date, coin

        else:
            print("Response is empty.")
            return None
    else:
        # Handle other HTTP status codes
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None




if __name__ == '__main__':

    create_tables()
    qtm_map, qtm_coin = fetch_ohlcv("QTUM_BTC")
    retrieve_and_store(qtm_map, qtm_coin)
    eth_map, eth_coin = fetch_ohlcv("ETH_BTC")
    response = retrieve_and_store(eth_map, eth_coin)


    #retrieve_and_store(fetch_ohlcv())
    # mock_hashmap = {
    #     datetime.date(2023, 3, 1): 0.002007,
    #     datetime.date(2023, 4, 1): 0.001705,
    #     datetime.date(2023, 5, 1): 0.001522,
    #     datetime.date(2023, 6, 1): 0.001388,
    #     datetime.date(2023, 7, 1): 0.001393,
    #     datetime.date(2023, 8, 1): 0.001387,
    #     datetime.date(2023, 9, 1): 0.00131,
    #     datetime.date(2023, 10, 1): 0.001337,
    #     datetime.date(2023, 11, 1): 0.001743,
    #     datetime.date(2023, 12, 1): 0.001472,
    #     datetime.date(2024, 1, 1): 0.001637,
    #     datetime.date(2024, 2, 1): 0.00124,
    # }
