from fastapi import FastAPI

from app.routes.builds import router as builds_router
from app.routes.user import router as user_router
from app.routes.category import router as category_router
from app.routes.transaction import router as transaction_router

app = FastAPI(title="PC Builder Backend")

# include all routers
app.include_router(builds_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(transaction_router)


@app.get("/")
def root():
    return {"message": "PC Builder backend running"}
