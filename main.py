
import logging
from Service import Service


logger = logging.getLogger('dicttoxml')
logger.setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",encoding='UTF-8')
service=Service()
service.creating_table()
service.filling_table()
service.make_queries()



# docker-compose build
# $env:res_type="json"; docker-compose up
