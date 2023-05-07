# from http.client import HTTPException
import asyncio
import azure.storage.blob.aio as blobstorage
import azure.storage.blob as blobstorage_sync
import azure.core.exceptions as blobstorage_exception
import fastapi
from urllib.parse import unquote
from  typing import Callable, Optional
from datetime import datetime, timedelta
from pathlib import Path
import sys
code_dir = Path(__file__).parent.parent.absolute()

sys.path.insert(0,str(code_dir))
from models import files


class BlobStorage:
    def __init__(self,connection_string: str) -> None:
        self.connection_string = connection_string
        # blob_service_client = blobstorage.BlobServiceClient(account_url=url, credential=access_key)
        self.blob_service_client = blobstorage.BlobServiceClient.from_connection_string(self.connection_string)

    def generate_sas_token(self,access_type: str = 'read', foldername: str = 'video', filename: str = "test") -> str:
        access_dict = {t: t == access_type for t in ('read','write')}
        blob = self.blob_service_client.get_blob_client(foldername,filename)
        sas_token = blobstorage_sync.generate_account_sas(
                    blob.account_name,
                    account_key=blob.credential.account_key,
                    resource_types=blobstorage_sync.ResourceTypes(object=True),
                    permission=blobstorage_sync.AccountSasPermissions(**access_dict),
                    expiry=datetime.utcnow() + timedelta(hours=1)
                    )   
        return sas_token#self.url + '?' + sas_token
    
    def get_url(self, filename: str, foldername: Optional[str]) -> str:
        sas_token = self.generate_sas_token(foldername=foldername,filename=filename)
        return self.blob_service_client.url + foldername + '/' + filename + '?' + sas_token

    async def list_folder_content(self,folder="video") -> list[files.file]:
        blob_service_client = blobstorage.BlobServiceClient.from_connection_string(self.connection_string)
        async with blob_service_client:
            container = blob_service_client.get_container_client(folder)
            blobs = []
            async for blob in container.list_blobs():
                blobs += [files.file(name=blob.name,url='',size=blob.size)]
        return  blobs
    
    async def list_folders(self) -> list[str]:
        blob_service_client = blobstorage.BlobServiceClient.from_connection_string(self.connection_string)
        print('IN Function!')
        async with blob_service_client:
            folders = []
            async for folder in blob_service_client.list_containers(include_metadata=True):
                folders += [folder]
        return [folder['name'] for folder in folders]
            

    def download_file(self,container_name,blob_name):
        blob_service_client = blobstorage.BlobServiceClient.from_connection_string(self.connection_string)
        blob = blob_service_client.get_blob_client(container_name,blob_name)


        with open(f"./Blobdestination.txt", "wb") as my_blob:
            blob_data = blob.download_blob()
            blob_data.readinto(my_blob)
       
             
    def upload_all_files(self,files: list[fastapi.UploadFile],folder: str):
        processes = [self.upload_file(file,folder) for file in files]
        out = asyncio.gather(*processes)
        return {file.filename:d for d,file in zip(out,files)}##{'done':'yes'}#{file.filename: self.upload_file(file,folder=folder) for file in files}

    def upload_file(self, file: fastapi.UploadFile, folder: str) -> dict:
        blob_service_client = blobstorage.BlobServiceClient.from_connection_string(self.connection_string)
        try:
            with blob_service_client:
                container_client = blob_service_client.get_container_client(folder)
                print('container client created')
                print(file.filename)
                with container_client:
                    f = file.read()
                    blob_client = container_client.upload_blob(name=file.filename,data=f,overwrite=True)
                    with blob_client:
                        properties = blob_client.get_blob_properties()
        except blobstorage_exception.ResourceExistsError as e:
            print(e.message)
            raise fastapi.HTTPException(status_code=402,detail= 'File already exists')
        except Exception as e:
            raise e
        finally:
            file.close()
        return {'Success': 'Yes', 'properties': properties.name}
    
    def create_folder(self,container_name: str) -> dict:
        blob_service_client = blobstorage.BlobServiceClient.from_connection_string(self.connection_string)
        # try:
        with blob_service_client:
            try:
                container = blob_service_client.create_container(container_name)
            except:
                return {'Success': 'No'}#HTTPException('401','Something went wrong')
        return {'Success': 'Yes'}
    
    def delete_folder(self,container_name: str) -> dict:
        blob_service_client = blobstorage.BlobServiceClient.from_connection_string(self.connection_string)
        blob_service_client.delete_container(container_name)
        return {"Success":"Yes"}
    
    def delete_file(self,folder_name: str, file_name: str) -> dict:
        blob_service_client = blobstorage.BlobServiceClient.from_connection_string(self.connection_string)
        try:
            with blob_service_client:
                blob = blob_service_client.get_blob_client(folder_name,file_name)##.get_blob_client(file_name)
                d = blob.delete_blob()    # blob.de
        except blobstorage_exception.ResourceNotFoundError as e:
            raise fastapi.HTTPException(status_code=404,detail = 'File not found')
        return {"Success":"Yes"}
    
    def move_file(self, from_folder_name: str, to_folder_name: str, file_name: str):
        blob_service_client = blobstorage.BlobServiceClient.from_connection_string(self.connection_string)
        try:
            with blob_service_client:
                url = self.get_url(filename=file_name,foldername=from_folder_name)
                # url = blob_service_client.make_blob_url(from_folder_name,file_name)
                copied_blob = blob_service_client.get_blob_client(to_folder_name,file_name)#blob_service_client.copy_blob(to_folder_name,file_name)
                copy = copied_blob.start_copy_from_url(url)
                props = copied_blob.get_blob_properties()
                try:
                    original_blob = blob_service_client.get_blob_client(from_folder_name,file_name)  
                    original_blob.delete_blob()
                except Exception as e:
                    print('Problem with deletion of file')
                    raise e
                
        except Exception as e:
            print('Problem with copiyng blob')
            raise e

        return {"Copy status": props.copy.status}
            