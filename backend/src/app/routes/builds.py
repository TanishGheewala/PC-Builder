from fastapi import APIRouter

router = APIRouter(prefix="/builds", tags=["builds"])


@router.get("/test")
def test_builds():
    return {"message": "Build routes working"}
