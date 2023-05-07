from models.token import Token
import httpx
import json
import urllib.parse


class AAD:
    '''
    Class for methods to authenticate against Azure Active Directory
    '''
    def __init__(self,tenant_id: str, client_id: str, client_secret: str ,scope: str, api_url: str) -> None:
        self.tenant_id              = tenant_id
        self.client_id              = client_id
        self.scope                  = scope
        self.client_secret          = client_secret
        self.base_url               = 'https://login.microsoftonline.com'
        self.redirect_url           = urllib.parse.quote(api_url+'/api/callback',safe='')
        self.oauth2_url             = f'{self.base_url}/{tenant_id}/oauth2/v2.0/token'
        self.token:   Token         = None

    def generate_access_token(self, code: str) -> None:
        '''
        Method for generating access token based on access code obtained by user logging into AAD.
        The token can be tested on https://jwt.ms/
        '''
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type':'authorization_code',
            'client_secret': self.client_secret,
            'code': code,
            'client_id': self.client_id
        }
        url = self.oauth2_url + f'?scope={self.scope}&redirect_url=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Fcallback'
        response = httpx.post(url=url, headers=headers, data=data)
        print(response.json)
        self.token = Token(**json.loads(response.content))
    
    def get_access_token(self, code: str):
        '''
        Checks if a new token needs to be generated and returns an active token
        '''
        if self.token == None:
            self.generate_access_token(code= code)
        # elif False:
        #     '''code for expired token'''
        #     pass
        return self.token.access_token
    
    def get_login_url(self) -> dict:
        callback_url = urllib.parse.quote(self.redirect_url,safe='')
        code_url  = f'{self.base_url}/{self.tenant_id}/oauth2/v2.0/authorize?client_id={self.client_id}&response_type=code&response_mode=query&scope={self.scope}&redirect_url={callback_url}'
        return {'url': code_url,
                'params': {'client_id': self.client_id,
                           'response_type': 'code',
                           'response_mode': 'query',
                           'scope': self.scope,
                           'redirect_url': callback_url
                           }
                }

