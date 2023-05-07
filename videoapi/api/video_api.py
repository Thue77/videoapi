import fastapi
from urllib.parse import unquote
from typing import Optional
from pathlib import Path
import sys

src = Path(__file__).parent.parent
sys.path.append(str(src))


from factories import source_factory,auth_factory
# from models import files
# import fastapi_microsoft_identity as auth
# from jose import jwt


router = fastapi.APIRouter(prefix='/api')

service = source_factory.source_factory()

@router.get('/item/{folder_name}')
# @auth.requires_auth
def get_video_url(video_name: str, folder_name: str, request: fastapi.Request):
    '''
    Returns a url for the specified video, which is given by writing ?video_name={name of the video}. 

    Note that if the video is contained in nested folders, then the remaining folders should be part of "video_name":

    ?video_name=\<subfolder>/\<subsubfolder>/\<video name>.\<extension>
    '''
    # try:

        # auth.validate_scope(required_scope=expected_scope,request=request)
    return {'url': service.get_url(filename=video_name,foldername=folder_name)}
    # except auth.AuthError as ae:
        # return fastapi.Response(content=ae.error_msg, status_code=ae.status_code)

@router.get('/item/{folder_name}/')
async def list_videos(request: fastapi.Request,folder_name: str):
    '''List folder content'''
    service = source_factory.source_factory()
    file_list = await service.list_folder_content(folder = folder_name)
    return {'videos': [{key:value for key,value in file.dict().items()} for file in file_list]}



@router.get('/folder/list/')
# @auth.requires_auth
async def list_folders(request: fastapi.Request):
    '''List all folders'''
    # try:
        # auth.validate_scope(required_scope=expected_scope,request=request)
    folders = await service.list_folders()
    return {'folders':folders}
    # except auth.AuthError as ae:
        #return fastapi.Response(content=ae.error_msg, status_code=ae.status_code)
        # raise fastapi.HTTPException(status_code=ae.status_code, detail = ae.error_msg)

# @router.get('/callback')
# def generate_oauth2_token2(code: str) -> dict[str,str]:
#     '''
#     Url to which the user is redirected after login
#     '''
#     return {'token':auth_factory.autherization_service.get_access_token(code=code)}

# @router.post('/token/{code}')
# def generate_oauth2_token(code: str) -> dict[str,str]:
#     '''
#     Url to which the user is redirected after login
#     '''
#     return {'token':auth_factory.autherization_service.get_access_token(code=code)}

# @router.get('/login')
# def login_url(redirect_url: str = None) -> dict[str,str]:
#     '''
#     Returns the url needed for the user to login
#     '''
#     if redirect_url is not None:
#         auth_factory.autherization_service.redirect_url = redirect_url
#     return auth_factory.autherization_service.get_login_url()
        


## Post methods

# @router.post('/folder/create')
# def create_folder(request: fastapi.Request,folder: str = fastapi.Form()):
#     '''Create folder'''
#     return service.create_folder(folder.lower())

# @router.delete('/folder/delete')
# def delete_folder(request: fastapi.Request,folder: str):
#     '''Delete folder'''
#     return service.delete_folder(folder.lower())

# @router.delete('/folder/delete/video')
# def delete_video(request: fastapi.Request,folder: str, file: str):
#     '''Delete video'''
#     return service.delete_file(folder.lower(),file)


# @router.post('/folder/upload/{folder_name}')
# def upload_video(files: list[fastapi.UploadFile], folder_name: str) -> dict:
#     '''Uploas files'''
#     print([file.filename for file in files])
#     return service.upload_all_files(files,folder=folder_name)#service.upload_file(files, folder_name)
    
# @router.put('/folder/move_file/{from_folder_name}/{to_folder_name}/{file_name}')
# def move_file(request: fastapi.Request,from_folder_name: str, to_folder_name: str, file_name: str):
#     return service.move_file(from_folder_name,to_folder_name,file_name)