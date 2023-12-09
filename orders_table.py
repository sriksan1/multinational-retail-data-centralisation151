import yaml
from sqlalchemy import create_engine
import pandas as pd
from data_cleaning import DataCleaning
from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from sqlalchemy.types import Integer, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Initialize your classes
db_connector = DatabaseConnector()
extractor = DataExtractor()
cleaner = DataCleaning()

# Task 6: Extract, Clean, and Upload Product Data
product_engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))
df = extractor.extract_from_s3("s3://data-handling-public/products.csv")
df = cleaner.convert_product_weights(df)
df = cleaner.clean_products_data(df)

#db_connector.upload_to_db(df, 'dim_products', product_engine)

# Task 7: Extract, Clean, Modify DataTypes, and Upload Orders Data
db_tables = db_connector.list_db_tables_inspector(product_engine)

orders_df = extractor.read_rds_table(db_connector, db_tables[2])
cleaned_orders_df = cleaner.clean_orders_data(orders_df)

# Determine max lengths for VARCHAR columns
max_length_card_number = cleaned_orders_df['card_number'].astype(str).map(len).max()
max_length_store_code = cleaned_orders_df['store_code'].astype(str).map(len).max()
max_length_product_code = cleaned_orders_df['product_code'].astype(str).map(len).max()

# Modify data types
cleaned_orders_df['date_uuid'] = cleaned_orders_df['date_uuid'].apply(lambda x: uuid.UUID(x))
cleaned_orders_df['user_uuid'] = cleaned_orders_df['user_uuid'].apply(lambda x: uuid.UUID(x))
cleaned_orders_df['card_number'] = cleaned_orders_df['card_number'].astype(str)
cleaned_orders_df['store_code'] = cleaned_orders_df['store_code'].astype(str)
cleaned_orders_df['product_code'] = cleaned_orders_df['product_code'].astype(str)
cleaned_orders_df['product_quantity'] = cleaned_orders_df['product_quantity'].astype('int16')
print(cleaned_orders_df.head())
# Mapping for SQLAlchemy datatypes
dtype_mapping = {
    'date_uuid': UUID(),
    'user_uuid': UUID(),
    'card_number': String(max_length_card_number),
    'store_code': String(max_length_store_code),
    'product_code': String(max_length_product_code),
    'product_quantity': Integer
}
print(cleaned_orders_df.dtypes)
# Upload to database
home_engine = db_connector.init_db_engine(db_connector.read_db_creds('localdb_cred.yaml'))
db_connector.upload_to_db(cleaned_orders_df, 'orders_table', home_engine)
