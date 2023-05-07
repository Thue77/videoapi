'''Module for handling secrets. In the development environment all secrets are derived
from enviroment variables. In production, it may be setup to use Azure Key Vault
'''
from dotenv import load_dotenv
import os
from pathlib import Path

class Secret:
    '''Class to represent secrets
    '''
    
    def __init__(self, s) -> None:
        self.s = s
    
    def __str__(self) -> str:
        return 'REDACTED'

class SecretScope:
    '''Class to deliver secrets based on the back-end provided
    '''
    
    def __init__(self, back_end: str, secret_scope_name: str = None) -> None:
        self.back_end = back_end
        self.secret_scope_name = secret_scope_name
        self.__connect_to_secret_scope()
        
    
    def __connect_to_secret_scope(self) -> Secret:
        if self.back_end == "Development":
            load_dotenv(Path(__file__).parent.parent / '.env.shared')    
        
        
    def get_secret(self, secret_name: str) -> Secret:
        if self.back_end == "Development":
            return Secret(os.environ[secret_name])
        


