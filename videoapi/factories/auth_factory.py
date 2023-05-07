from typing import Protocol
from pathlib import Path
import sys

src = Path(__file__).parent.parent
sys.path.append(str(src))

from services.azure_active_directory import AAD

class AutherizationService(Protocol):
    def __init__(self,tenant_id: str, client_id: str, client_secret: str ,scope: str, api_url: str) -> None:
        ...
    def get_access_token(self, code: str) -> str:
        ...
    def get_login_url(self) -> dict:
        ...



autherization_service: AutherizationService

FACTORY = {
    'microsoft': AAD
}

def set_autherization_service(tenant_id: str, 
                                client_id: str, 
                                client_secret: str,
                                scope: str,
                                api_url: str, 
                                service: str = 'microsoft'):
    '''
    Method to create autherization service. so far there is only AAD
    '''
    global autherization_service
    autherization_service = FACTORY[service](tenant_id=tenant_id,
                                            client_id=client_id,
                                            client_secret=client_secret,
                                            scope=scope,
                                            api_url=api_url)