import yaml
from sqlalchemy import create_engine
import pandas as pd
from data_cleaning import DataCleaning
from data_extraction import DataExtractor
from database_utils import DatabaseConnector

db_connector = DatabaseConnector()
sales_data_engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))
cleaner = DataCleaning()
# #Use DataCleaning class to clean the data
url = 's3://data-handling-public/products.csv' 
extractor = DataExtractor()
df = extractor.extract_from_s3(url)
product_weight_df = cleaner.convert_product_weights(df)
cleaned_product_weight_df = cleaner.clean_products_data(product_weight_df)
home_engine = db_connector.init_db_engine(db_connector.read_db_creds('localdb_cred.yaml'))
db_connector.upload_to_db(cleaned_product_weight_df, 'dim_products', home_engine)