from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI


from app.router import router
from app.llm_engine import setup_llm

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    setup_llm()  # Load model + embedding
