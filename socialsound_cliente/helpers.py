import requests
import environ
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()


# def crear_cabecera():
#     return {'Authorization': f'Bearer {settings.OAUTH_TOKENS[1]}'}

class helper:
    
    def obtener_token_session(usuario,password):
        token_url = 'http://127.0.0.1:8000/oauth2/token/'
        data = {
            'grant_type': 'password',
            'username': usuario,
            'password': password,
            'client_id': 'musicapp',
            'client_secret': 'musicapp',
        }
        response = requests.post(token_url, data=data)
        respuesta = response.json()
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get("error_description"))