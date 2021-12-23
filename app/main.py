from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter()

@app.get("/")
async def root():
    return {"message": "hey bitch"}
