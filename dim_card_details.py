import yaml
from sqlalchemy import create_engine
import pandas as pd
from data_cleaning import DataCleaning
from data_extraction import DataExtractor
from database_utils import DatabaseConnector

db_connector = DatabaseConnector()
data_extractor = DataExtractor()
data_cleaner = DataCleaning()
engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))
# # Retrieve data from PDF
pdf_url = 'card_details.pdf'  # Replace with the actual PDF URL
df_card_data = data_extractor.retrieve_pdf_data(pdf_url)

# Clean data
df_cleaned_card_data = data_cleaner.clean_user_data(df_card_data)

#Upload to database
home_engine = db_connector.init_db_engine(db_connector.read_db_creds('localdb_cred.yaml'))
db_connector.upload_to_db(df_cleaned_card_data, 'dim_card_details', home_engine)