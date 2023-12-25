from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}