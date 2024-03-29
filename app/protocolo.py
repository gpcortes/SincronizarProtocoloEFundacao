import os
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from dotenv import load_dotenv


class Protocolo():

    def __init__(self):
        import envconfiguration as config

        self.host = config.PROTO_HOST_DB 
        self.port = config.PROTO_PORT_DB
        self.user = config.PROTO_USER_DB
        self.passwd = config.PROTO_PASSWD_DB
        self.database_name = config.PROTO_DB

    # def __load_env(self):
    #     if os.getenv('ENV') != 'production':
    #         from os.path import join, dirname
    #         from dotenv import load_dotenv
    #         dotenv_path = join(dirname(__file__), 'proto.env')
    #         load_dotenv(dotenv_path)

    #     PROTO_USER_DB = os.getenv('PROTO_USER_DB')
    #     PROTO_PASSWD_DB = os.getenv('PROTO_PASSWD_DB')
    #     PROTO_HOST_DB = os.getenv('PROTO_HOST_DB')
    #     PROTO_PORT_DB = os.getenv('PROTO_PORT_DB')
    #     PROTO_DB = os.getenv('PROTO_DB')

    #     return PROTO_HOST_DB, PROTO_PORT_DB, PROTO_USER_DB, PROTO_PASSWD_DB, PROTO_DB

    def __get_engine(self):
        return create_engine('mysql+pymysql://'+self.user+':'+self.passwd+'@'+self.host+':'+self.port+'/'+self.database_name)

    def get_ticket(self, ticketid):
        engine = self.__get_engine()
        conn = engine.connect()
        query = conn.execute("SELECT * FROM atendimento_js_ticket_tickets where UPPER(ticketid) = UPPER('{}')".format(ticketid))
        return query.fetchall()
    
    def update_ticket(self, ticketid, params):
        engine = self.__get_engine()
        conn = engine.connect()
        conn.execute("UPDATE atendimento_js_ticket_tickets SET {} WHERE UPPER(ticketid) = UPPER('{}')".format(params, ticketid))
        return True