import os
import requests


class RTVE():

    def __init__(self):
        self.host, self.user, self.passwd, self.covenant = self.__load_env()
        self.token = self.__get_token()

    def __load_env(self):
        if os.getenv('ENV') != 'production':
            from os.path import join, dirname
            from dotenv import load_dotenv
            dotenv_path = join(dirname(__file__), 'rtve.env')
            load_dotenv(dotenv_path)

        RTVE_HOST = os.getenv('RTVE_HOST')
        RTVE_USER = os.getenv('RTVE_USER')
        RTVE_PASSWD = os.getenv('RTVE_PASSWD')
        RTVE_COVENANT = os.getenv('RTVE_COVENANT')

        return RTVE_HOST, RTVE_USER, RTVE_PASSWD, RTVE_COVENANT

    def __gen_token(self):
            body = {'Login': self.user, 'Senha': self.passwd}
            self.token = requests.post(self.host + '/usuario/loginAPI', json=body).text.split(':')[1].strip()
            return self.token
    
    def __get_token(self):
        if 'token' not in self.__dict__:
            return self.__gen_token()
        
        response = requests.get(
            self.host + '/privado/requisicoes_projeto?numconv=1&login=' + self.user + '&token=' + self.token)

        if response.status_code == 200 and response.json() == []:
            return self.token
        else:
            return self.__gen_token()

    def get_requisicoes(self):
        return requests.get(self.host + '/privado/requisicoes_projeto?numconv=' + self.covenant + '&login=' + self.user +
                            '&token=' + self.__get_token()).json()

    def get_requisicao(self, requisicao):
        return requests.get(self.host + '/privado/processo_requisicao?id=' + str(requisicao) + '&login=' + self.user + '&token=' +
                            self.__get_token()).json()
