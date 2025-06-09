from fastapi import FastAPI
from app.routes import router as api_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Initialize any resources or connections here if needed
    pass
app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Messaging System API"}