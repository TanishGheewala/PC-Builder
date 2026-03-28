from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    user_id: int


class CategoryUpdate(BaseModel):
    name: str | None = None


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True
