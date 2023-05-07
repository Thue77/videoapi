from fastapi import UploadFile
from typing import Callable, Protocol, Optional
import os
from pathlib import Path
import sys

src = Path(__file__).parent.parent
sys.path.append(str(src))

from services import blob_storage
from models import files

class SourceService(Protocol):
    '''
    Represents a service from the "services" folder
    '''

    def get_url(filename: str, foldername: Optional[str]) -> str:
        ...
    
    def list_folder_content(folder: Optional[str]) -> list[files.file]:
        ...
    
    def download_file(folder: str, filename: str) -> None:
        ...
    def upload_all_files( file: list[UploadFile], folder: str) -> dict:
        ...
    def create_folder(container_name: str) -> dict:
        ...

    def list_folders() -> list[str]:
        ...
    def delete_folder() -> dict:
        ...
    def delete_file() -> dict:
        ...
    def move_file() -> dict:
        ...

SourceFactory = Callable[[str,Optional[str]],SourceService]

FACTORY = {
    'blob': blob_storage.BlobStorage
}

storage_type: str = 'blob'

def source_factory() -> SourceService:
    '''
    Factory function to return the right service-object based on the storage type that is used
    '''
    # with open('videoapi/settings.json','r') as f:
    #     data = dict(json.load(f))
    
    source_service = FACTORY[storage_type](connection_string=os.getenv("AzureWebJobsStorage"))

    return source_service


