import yaml
from sqlalchemy import create_engine,inspect
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
        return engine.get_tables() 
    def list_db_tables_inspector(self, engine):
        inspector = inspect(engine)
        return inspector.get_table_names()
    def upload_to_db(self,df,table_name,engine):
        df.to_sql(table_name,engine,if_exists='replace',index=False)






