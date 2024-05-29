
from dotenv import load_dotenv
import os
import json
import logging
from Database import DataBase,DDL_Queries,DML_Queries
class Service:
    def __init__(self) -> None:
        database_name,user_name,password,host,port,self.type_of_result_file,path_to_file_students,path_to_file_rooms,self.queries_directory=self.get_data_env()
        self.database=DataBase(database_name,user_name,str(password),host,str(port))
        self.students=self.read_json_files(path_to_file_students)
        self.rooms=self.read_json_files(path_to_file_rooms)
        self.ddl=DDL_Queries(self.database)
        self.dml=DML_Queries(self.database)
    def get_data_env(self):
        load_dotenv()
        return os.getenv('database_name'),os.getenv('user_name'),os.getenv('password'),os.getenv('host'),os.getenv('port'),os.getenv('res_type'),os.getenv('path_to_file_students'),os.getenv('path_to_file_rooms'),os.getenv('queries_directory')


    def read_json_files(self,path_to_file):
        try:
            with open(path_to_file, 'r') as f:
                result = json.load(f)
            logging.info(path_to_file+" was readed")
            return result
        except IOError as e:
            logging.error(f"Error: {e}")
            logging.warning("Json files wasn't readed! It can be dangerous for program")
    def creating_table(self):
        self.ddl.creating_table()
    def filling_table(self):
        self.dml.filling_table(self.students,self.rooms)
    def make_queries(self):
        self.dml.make_queries(self.queries_directory,self.type_of_result_file)
