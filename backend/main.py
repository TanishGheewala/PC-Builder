from fastapi import FastAPI

# Check pylance:
from app.routes.auth import router as auth_router
from app.routes.builds import router as builds_router

app = FastAPI(title="PC Builder Backend")

app.include_router(auth_router)
app.include_router(builds_router)


@app.get("/")
def root():
    return {"message": "PC Builder backend running"}
