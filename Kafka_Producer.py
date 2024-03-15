import pandas as pd
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json
import requests
from datetime import datetime, timedelta

def get_data_from_api(report_datetime, offset=0, limit=200):
    # Format the report datetime as required by the API
    report_datetime_str = report_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    # Calculate the datetime one day ago
    one_day_ago = report_datetime - timedelta(days=1)
    one_day_ago_str = one_day_ago.strftime('%Y-%m-%dT%H:%M:%S')

    # API endpoint URL with report_datetime parameter
    url = f'https://data.seattle.gov/resource/tazs-3rd5.json?$offset={offset}&$limit={limit}&$where=report_datetime>="{one_day_ago_str}"'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Convert the response JSON data to a DataFrame
        df = pd.DataFrame(response.json())

        # Print the first few rows of the DataFrame
        return df
    else:
        # Print an error message if the request was not successful
        print('Failed to retrieve data from the API. Status code:', response.status_code)
        return None


producer = KafkaProducer(bootstrap_servers=['<domain>:9092'], #change ip here
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))


while True:
    current_datetime = datetime.now()
    df = get_data_from_api(current_datetime)
    # Select specific columns
    df = df[['report_number', 'offense_id', 'offense_start_datetime',
             'offense_end_datetime', 'report_datetime', 
             'crime_against_category', 'offense_parent_group', 'offense',
             'offense_code', 'precinct', 'sector', 'mcpp',
             '_100_block_address', 'longitude', 'latitude']]

    # Rename the column
    df.rename(columns={'_100_block_address': 'block_address'}, inplace=True)

    # Convert datetime columns to datetime format
    datetime_columns = ['offense_start_datetime', 'offense_end_datetime', 'report_datetime']
    df[datetime_columns] = df[datetime_columns].apply(pd.to_datetime)
    df[datetime_columns] = df[datetime_columns].apply(lambda x: x.dt.strftime('%Y-%m-%d %H:%M:%S'))
    dict_list = df.to_dict(orient="records")

    for incident in dict_list:
        producer.send('seattle_911_crime', value=incident)
        sleep(1)
        
    