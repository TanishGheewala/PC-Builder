from fastapi import FastAPI
from app.routes.builds import router as builds_router

app = FastAPI(title="PC Builder Backend")

app.include_router(builds_router)


@app.get("/")
def root():
    return {"message": "PC Builder backend running"}
