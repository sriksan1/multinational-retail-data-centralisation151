import yaml
from sqlalchemy import create_engine
import pandas as pd
from data_cleaning import DataCleaning
from data_extraction import DataExtractor
from database_utils import DatabaseConnector
#Task 8
# Initialize your DatabaseConnector and DataExtractor
db_connector = DatabaseConnector()
extractor = DataExtractor()
cleaner = DataCleaning()

# Extract JSON data from S3
json_url = "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
json_df = extractor.extract_from_s3_json(json_url)

# Clean the data
cleaned_json_df = cleaner.clean_user_data(json_df)

# Initialize database engine
json_engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))

# Upload the cleaned data to the database
home_engine = db_connector.init_db_engine(db_connector.read_db_creds('localdb_cred.yaml'))
db_connector.upload_to_db(cleaned_json_df, 'dim_date_times', home_engine)