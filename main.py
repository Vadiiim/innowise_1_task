

import json
import sys
from dotenv import load_dotenv
import psycopg2
import os
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import logging




def get_data_users_dbname():
    load_dotenv()
    return os.getenv('database_name'),os.getenv('user_name'),os.getenv('password'),os.getenv('host'),os.getenv('port'),os.getenv('res_type')

# start func of reading json files
def read_json_files(path_to_file):
    try:
        with open(path_to_file, 'r') as f:
            result = json.load(f)
        logging.info(path_to_file+" was readed")
        return result
    except IOError as e:
        logging.error(f"Error: {e}")
        logging.warning("Json files wasn't readed! It can be dangerous for program")
#end






#  class that help work with db
class DataBase:
    __database_name=''
    __user_name=''
    __password=''
    __host=''
    __port=''



    def __init__(self,database_name,user_name,password,host,port) -> None:
        self.__database_name=database_name
        self.__user_name=user_name
        self.__password=str(password)
        self.__host=host
        self.__port=str(port)

    def creating_table(self):
        try:
            conn = psycopg2.connect(f"dbname={self.__database_name} user={self.__user_name} password={self.__password} host={self.__host} port={self.__port}")

            cur = conn.cursor()

            cur.execute("""
                CREATE TYPE mood AS ENUM('M','F');
                CREATE TABLE IF NOT EXISTS students (
                    id INT PRIMARY KEY,
                    birthday timestamp,
                    name TEXT,
                    room INT,
                    sex mood
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INT PRIMARY KEY,
                    name TEXT
                )
            """)
            logging.info("Tables successfuly created!")
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.Error as e:

                if e.pgcode == '42P07':
                    logging.warning("Table is already exist")
                else:
                    logging.warning(f"Error: {e}")
                return "Error" ;

        except :

            logging.error("Check that the database exists, the user exists, and the password is correct.")
            logging.warning("Tabels wasn't created! It can be dangerous for program")
            return "Error" ;







    def filling_table(self,students,rooms):
        try:
            conn = psycopg2.connect(f"dbname={self.__database_name} user={self.__user_name} password={self.__password} host={self.__host} port={self.__port}")
            cur = conn.cursor()
            for item in students :
               cur.execute(f"INSERT INTO students (id, birthday, name, room, sex) VALUES ({item['id']},'{item['birthday']}','{item['name']}',{item['room']},'{item['sex']}')")
            for item in rooms :
               cur.execute(f"INSERT INTO rooms (id, name) VALUES ({item['id']},'{item['name']}')")
            logging.info("Tables successfuly filled!")
            conn.commit()
            cur.close()
            conn.close()
        except psycopg2.OperationalError as e:

            logging.error(f"Error: {e}")
            return "Error" ;
        except :

            logging.error("Check that the database exists, the user exists, and the password is correct.")
            return "Error" ;


    def make_queries(self,queries_directory,type_of_result_file):

            conn = psycopg2.connect(f"dbname={self.__database_name} user={self.__user_name} password={self.__password} host={self.__host} port={self.__port}")
            cur = conn.cursor()
            for file in os.listdir(queries_directory):
                path_to_quaery=os.path.join(queries_directory, file)
                if os.path.isfile(path_to_quaery):

                    with open(path_to_quaery,'r') as f:
                        content_in_file=f.read()
                    cur.execute(content_in_file)
                    results1 = cur.fetchall()
                    keys=[]
                    results = []
                    for colum in cur.description:
                        keys.append(colum[0])
                    for row in results1:
                        results.append(dict(zip(keys, row)))
                    if   type_of_result_file=='json':
                        results_json = json.dumps(results)
                        with open('./results/'+os.path.splitext(file)[0]+'.json', 'w') as j:
                            j.write(results_json)
                    elif  type_of_result_file=='xml':
                        results_xml = dicttoxml(results)
                        dom = parseString(results_xml)
                        with open('./results/'+os.path.splitext(file)[0]+'.xml', 'w') as x:
                            x.write(dom.toprettyxml())
                    else:
                        results_json = json.dumps(results)
                        with open('./results/'+os.path.splitext(file)[0]+'.json', 'w') as j:
                            j.write(results_json)
                        results_xml = dicttoxml(results)
                        dom = parseString(results_xml)
                        with open('./results/'+os.path.splitext(file)[0]+'.xml', 'w') as x:
                            x.write(dom.toprettyxml())

            logging.info("Quaeries successfuly passed!")
            conn.commit()
            cur.close()
            conn.close()



# end class



#main start
logger = logging.getLogger('dicttoxml')

# Установите уровень логирования на ERROR (или любой другой уровень, который вы хотите)
logger.setLevel(logging.ERROR)

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",encoding='UTF-8')


path_to_file_students = './jsonfiles/students.json'
path_to_file_rooms='./jsonfiles/rooms.json'
queries_directory='./quaeries'

#type_of_result_file='xml'
# database_name=input('Input DB ')
# user_name='postgres'
# password='1'
#type_of_result_file='json'
# database_name='TASK1'
# user_name='postgres'
# password='1'



database_name,user_name,password,host,port,type_of_result_file=get_data_users_dbname()


database=DataBase(database_name,user_name,str(password),host,str(port))

students=read_json_files(path_to_file_students)
rooms=read_json_files(path_to_file_rooms)

database.creating_table()
database.filling_table(students,rooms)




database.make_queries(queries_directory,type_of_result_file)

#main end
