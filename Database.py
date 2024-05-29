import psycopg2
import logging
import os
import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

class DataBase:
    def __init__(self,database_name,user_name,password,host,port) -> None:
        self.__database_name=database_name
        self.__user_name=user_name
        self.__password=str(password)
        self.__host=host
        self.__port=str(port)
    def connect_to_db(self):
        self.__conn = psycopg2.connect(f"dbname={self.__database_name} user={self.__user_name} password={self.__password} host={self.__host} port={self.__port}")
        self.__cur=self.__conn.cursor()
        return  self.__cur
    def commit_con(self):
        self.__conn.commit()
    def __del__(self):
        self.__cur.close()
        self.__conn.close()


class DDL_Queries:
    def __init__(self,db) -> None:
        self.__db=db
    def creating_table(self):
        try:
            cur=self.__db.connect_to_db()
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
            self.__db.commit_con()
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







class DML_Queries:
    def __init__(self,db) -> None:
        self.__db=db
    def filling_table(self,students,rooms):
        try:
            cur=self.__db.connect_to_db()
            for item in students :
               cur.execute(f"INSERT INTO students (id, birthday, name, room, sex) VALUES ({item['id']},'{item['birthday']}','{item['name']}',{item['room']},'{item['sex']}')")
            for item in rooms :
               cur.execute(f"INSERT INTO rooms (id, name) VALUES ({item['id']},'{item['name']}')")
            logging.info("Tables successfuly filled!")
            self.__db.commit_con()
        except psycopg2.OperationalError as e:

            logging.error(f"Error: {e}")
            return "Error" ;
        except :

            logging.error("Check that the database exists, the user exists, and the password is correct.")
            return "Error" ;



    def make_queries(self,queries_directory,type_of_result_file):

        try:
            cur=self.__db.connect_to_db()
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
            self.__db.commit_con()
        except psycopg2.OperationalError as e:

            logging.error(f"Error: {e}")
            return "Error" ;
        except :

            logging.error("Check that the database exists, the user exists, and the password is correct.")
            return "Error" ;
