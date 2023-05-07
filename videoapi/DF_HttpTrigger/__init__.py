import logging
import azure.functions as func
import fastapi
import json

from pathlib import Path
import sys

src = Path(__file__).parent.parent
sys.path.append(str(src))

from api import video_api
from factories import source_factory,auth_factory


app = fastapi.FastAPI()

rootPath = Path("videoapi").absolute() 

def configure(api_url: str = 'http://127.0.0.1:8000'):
    configure_router()
    configure_storage_type()
    # configure_identity(api_url=api_url)

def configure_router():
    '''
    Include the routers from "api"
    '''
    app.include_router(video_api.router)


def configure_storage_type():
    '''
    This allows different users to use different storage. By standard the storage is configured to be
    Azure Blob Storage
    '''
    source_factory.storage_type = 'blob'

def configure_identity(api_url: str):
    '''
    Method to set up identity
    '''
    with open(rootPath/'settings.json','r') as file:
        data = json.load(file)
        client_id = data['client_id']
        tenant_id = data['tenant_id']
        client_secret = data['client_secret']
        scope = data['read_scope']
        auth_factory.set_autherization_service(tenant_id, 
                                                client_id, 
                                                client_secret,
                                                scope,
                                                api_url)




# if __name__ == "__main__":
#     uvicorn.run("main:app",port=8080,host="127.0.0.1",reload=True)
#     configure()
# else:
#     configure()


@app.get("/sample")
async def index():
    return {
        "info": "Try /hello/Shivani for parameterized route.",
    }

async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    configure()
    return await func.AsgiMiddleware(app).handle_async(req,context)
