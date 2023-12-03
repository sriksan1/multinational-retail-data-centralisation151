import yaml
from sqlalchemy import create_engine
import pandas as pd
from data_cleaning import DataCleaning
from data_extraction import DataExtractor
class DatabaseConnector:
    def read_db_creds(self, file_path):
        with open(file_path, 'r') as file:
            credentials = yaml.safe_load(file)
        return credentials
    def init_db_engine(self, creds):
        connection_string = f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
        return create_engine(connection_string)
    def list_db_tables(self, engine):
        return engine.table_names()
    def upload_to_db(self,df,table_name,engine):
        df.to_sql(table_name,engine,if_exists='replace',index=False)

# db_connector = DatabaseConnector()
# sales_data_engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))
# # #Use DataCleaning class to clean the data
# # cleaned_sales_data = DataCleaning().clean_user_data(sales_data)
# # db_connector.upload_to_db(cleaned_sales_data, 'dim_users', sales_data_engine)

# # Assuming db_connector and engine are already set up
# data_extractor = DataExtractor()
# data_cleaner = DataCleaning()

# # Retrieve data from PDF
# pdf_url = 'card_details.pdf'  # Replace with the actual PDF URL
# df_card_data = data_extractor.retrieve_pdf_data(pdf_url)

# # Clean data
# df_cleaned_card_data = data_cleaner.clean_user_data(df_card_data)

# Upload to database
#db_connector.upload_to_db(df_cleaned_card_data, 'dim_card_details', sales_data_engine)

#Task 5
# db_connector = DatabaseConnector()
# store_engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))
# header_details = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
# number_stores_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
# retrieve_stores_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/store_number'

# extractor = DataExtractor()
# cleaner = DataCleaning()
# stores_df = extractor.retrieve_stores_data(number_stores_url,retrieve_stores_url,header_details)
# cleaned_stores_df = cleaner.clean_store_data(stores_df)
# db_connector.upload_to_db(cleaned_stores_df, 'dim_store_details', store_engine)

# #Task 6 
# db_connector = DatabaseConnector()
# product_engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))

# extractor = DataExtractor()
# cleaner = DataCleaning()

# df = extractor.extract_from_s3("s3://data-handling-public/products.csv")
# df = cleaner.convert_product_weights(df)
# df = cleaner.clean_products_data(df)
# db_connector.upload_to_db(df, 'dim_products', product_engine)

# #Task 7
# db_tables = db_connector.list_db_tables(product_engine)
# orders_df = extractor.read_rds_table(db_connector,db_tables)
# cleaned_orders_df = cleaner.clean_orders_data(orders_df)
# db_connector.upload_to_db(cleaned_orders_df, 'orders_table', product_engine)
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
db_connector.upload_to_db(cleaned_json_df, 'dim_date_times', json_engine)
