from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()


@app.post("/files/")
def create_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files],
            "content-types": [file.content_type for file in files]}


@app.get("/")
def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

if __name__ == '__main__':
    uvicorn.run("test_upload:app",port=8000,host="127.0.0.1",reload=True)