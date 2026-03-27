from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    user_id: int


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True
