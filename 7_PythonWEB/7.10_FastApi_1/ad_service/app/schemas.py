from pydantic import BaseModel
from datetime import datetime

class AdvertisementBase(BaseModel):
    title: str
    description: str | None = None
    price: int
    author: str

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author: str | None = None

class Advertisement(AdvertisementBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True