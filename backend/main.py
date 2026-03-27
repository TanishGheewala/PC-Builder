import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.builds import router as builds_router
from app.routes.category import router as category_router
from app.routes.transaction import router as transaction_router
from app.routes.user import router as user_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PC Builder Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(
        "%s %s - %s - %.4fs",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )
    return response


app.include_router(auth_router)
app.include_router(builds_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(transaction_router)


@app.get("/")
def root():
    return {"message": "PC Builder backend running"}
