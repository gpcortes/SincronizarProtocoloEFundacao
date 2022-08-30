import os
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from tunnelossh import SSHTunnel
from dotenv import load_dotenv

class Protocolo():

    def __init__(self):
        self.host, self.port, self.user, self.passwd, self.database_name = self.__load_env()

    def __load_env(self):
        if os.getenv('ENV') != 'production':
            from os.path import join, dirname
            from dotenv import load_dotenv
            dotenv_path = join(dirname(__file__), 'proto.env')
            load_dotenv(dotenv_path)

        PROTO_USER_DB = os.getenv('PROTO_USER_DB')
        PROTO_PASSWD_DB = os.getenv('PROTO_PASSWD_DB')
        PROTO_HOST_DB = os.getenv('PROTO_HOST_DB')
        PROTO_PORT_DB = os.getenv('PROTO_PORT_DB')
        PROTO_DB = os.getenv('PROTO_DB')

        return PROTO_HOST_DB, PROTO_PORT_DB, PROTO_USER_DB, PROTO_PASSWD_DB, PROTO_DB

    def __get_engine(self):
        return create_engine('mysql+pymysql://'+self.user+':'+self.passwd+'@'+self.host+':'+self.port+'/'+self.database_name)

    @SSHTunnel('sites', 3306, 3306)
    def get_ticket(self, ticketid):
        engine = self.__get_engine()
        conn = engine.connect()
        query = conn.execute("SELECT * FROM atendimento_js_ticket_tickets where UPPER(ticketid) = UPPER('{}')".format(ticketid))
        return query.fetchall()
    
    @SSHTunnel('sites', 3306, 3306)
    def update_ticket(self, ticketid, params):
        engine = self.__get_engine()
        conn = engine.connect()
        conn.execute("UPDATE atendimento_js_ticket_tickets SET {} WHERE UPPER(ticketid) = UPPER('{}')".format(params, ticketid))
        return True