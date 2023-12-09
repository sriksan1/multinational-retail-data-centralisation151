import yaml
from sqlalchemy import create_engine
import pandas as pd
from data_cleaning import DataCleaning
from data_extraction import DataExtractor
from database_utils import DatabaseConnector

db_connector = DatabaseConnector()
sales_data_engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))
# #Use DataCleaning class to clean the data
extractor = DataExtractor()
db_tables = db_connector.list_db_tables_inspector(sales_data_engine)

sales_data = extractor.read_rds_table(db_connector, db_tables[1])
home_engine = db_connector.init_db_engine(db_connector.read_db_creds('localdb_cred.yaml'))
cleaner = DataCleaning()
cleaned_sales_data = cleaner.clean_user_data(sales_data)
db_connector.upload_to_db(cleaned_sales_data, 'dim_users', home_engine)
