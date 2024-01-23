from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Request
from config import settings
import typing as t
import uvicorn
import os


from qdrant_engine import QdrantIndex
# from sentence_transformers import SentenceTransformer


app = FastAPI(
    title="backend API", docs_url="/docs"
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Load embedding model
# embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device='cpu')

# Load the Qdrant index
qdrant_index = QdrantIndex(settings.qdrant_host, settings.qdrant_api_key, False)



class UserQuery(BaseModel):
    query: str




@app.get("/")
async def root(request: Request):
    return {"message": "Server is up and running!"}



@app.post("/upload-file")
async def upload_file(request: Request, file: UploadFile):
    filename = file.filename
    status = "success"
    print(file.size)
    try:
        filepath = os.path.join('app','documents', os.path.basename(filename))
        contents = await file.read()
        with open(filepath, 'wb') as f:
            f.write(contents)
        
        qdrant_index.insert_into_index(filepath, filename)
        
    except Exception as ex:
        print(str(ex))
        status = "error"
        if filepath is not None and os.path.exists(filepath):
            os.remove(filepath)
        # raise HTTPException(status_code=500, detail="Your file received but couldn't be stored!")

    if filepath is not None and os.path.exists(filepath):
        os.remove(filepath)
    return {"filename": filename, "status": status}
    


@app.post("/query")
async def query_index(request: Request, input_query: UserQuery):
    print(input_query)
    generated_response, relevant_docs = qdrant_index.generate_response(question=input_query.query)
    print(generated_response)
    return {"response": generated_response, "relevant_docs": relevant_docs}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
