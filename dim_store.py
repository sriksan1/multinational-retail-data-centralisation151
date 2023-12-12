import yaml
from sqlalchemy import create_engine
import pandas as pd
from data_cleaning import DataCleaning
from data_extraction import DataExtractor
from database_utils import DatabaseConnector

#Task 5
db_connector = DatabaseConnector()
store_engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))
header_details = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
number_stores_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
retrieve_stores_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'

extractor = DataExtractor()
cleaner = DataCleaning()
stores_df = extractor.retrieve_stores_data(number_stores_url,retrieve_stores_url,header_details)
cleaned_stores_df = cleaner.clean_store_data(stores_df)

home_engine = db_connector.init_db_engine(db_connector.read_db_creds('localdb_cred.yaml'))
db_connector.upload_to_db(stores_df, 'dim_store_details', home_engine)
