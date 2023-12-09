import pandas as pd
import tabula
import requests
import boto3
from io import BytesIO
'''Develop a method called read_rds_table in your DataExtractor class which will extract the database table to a pandas DataFrame.

It will take in an instance of your DatabaseConnector class and the table name as an argument and return a pandas DataFrame.
Use your list_db_tables method to get the name of the table containing user data.
Use the read_rds_table method to extract the table containing user data and return a pandas DataFrame.'''
class DataExtractor:
    def read_rds_table(self, db_connector, table_name):
        engine = db_connector.init_db_engine(db_connector.read_db_creds('db_cred.yaml'))
        tables = db_connector.list_db_tables_inspector(engine)
        if table_name in tables:
            return pd.read_sql(table_name, engine)
        else:
            print(f'Table {table_name} not found in database.')
        return None 
    def retrieve_pdf_data(self, pdf_url):
        # Extract data from PDF
        df_list = tabula.read_pdf(pdf_url, pages='all', multiple_tables=True)

        # Combine all tables in a single DataFrame
        return pd.concat(df_list, ignore_index=True)
    def list_number_of_stores(self, number_stores_url,header_details):
        response = requests.get(number_stores_url, headers=header_details)
        if response.status_code == 200:
            try:
                data = response.json()
                return data.get('number_of_stores', 0)
            except ValueError:
                print("Failed to parse JSON response")
                return 0
        else:
            print(f"Failed to retrieve data, status code: {response.status_code}")
            return 0
    def retrieve_stores_data(self,number_stores_url,retrieve_stores_url,header_details):
        num_stores = self.list_number_of_stores(number_stores_url,header_details)
        all_stores = []
        for store_num in range(1,num_stores+1):
            format_url = retrieve_stores_url.format(store_number=store_num)
            response = requests.get(format_url,headers=header_details)
            if response.status_code == 200:
                try:
                    store_data = response.json()
                    all_stores.append(store_data)
                except ValueError:
                    print("Failed to parse JSON response")
            else:
                print(f"Failed to retrieve data, status code: {response.status_code}")
        return pd.DataFrame(all_stores)
    def extract_from_s3(self, s3_uri):
            bucket_name = s3_uri.split('/')[2]
            object_key = '/'.join(s3_uri.split('/')[3:])

            s3 = boto3.client('s3')
            csv_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
            body = csv_obj['Body'].read()

            data_frame = pd.read_csv(BytesIO(body))
            return data_frame
    def extract_from_s3_json(self, s3_uri):
        # Split the URL to get the bucket name and object key
        parts = s3_uri.replace("https://", "").split('/')
        bucket_name = parts[0].replace(".s3.eu-west-1.amazonaws.com", "")
        object_key = '/'.join(parts[1:])

        print(f"Bucket Name: {bucket_name}")
        print(f"Region Name: eu-west-1")
        print(f"Object Key: {object_key}")

        s3 = boto3.client('s3', region_name='eu-west-1')
        json_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        body = json_obj['Body'].read()

        data_frame = pd.read_json(BytesIO(body))
        return data_frame







    

