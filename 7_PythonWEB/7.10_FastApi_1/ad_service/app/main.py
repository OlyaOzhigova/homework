from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/advertisement/", response_model=schemas.Advertisement)
def create_advertisement(
    advertisement: schemas.AdvertisementCreate, db: Session = Depends(get_db)
):
    db_ad = models.Advertisement(**advertisement.model_dump())
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

@app.get("/advertisement/{advertisement_id}", response_model=schemas.Advertisement)
def read_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    db_ad = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_ad

@app.patch("/advertisement/{advertisement_id}", response_model=schemas.Advertisement)
def update_advertisement(
    advertisement_id: int, 
    advertisement: schemas.AdvertisementUpdate, 
    db: Session = Depends(get_db)
):
    db_ad = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    update_data = advertisement.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ad, key, value)
    
    db.commit()
    db.refresh(db_ad)
    return db_ad

@app.delete("/advertisement/{advertisement_id}")
def delete_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    db_ad = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    db.delete(db_ad)
    db.commit()
    return {"message": "Advertisement deleted successfully"}

@app.get("/advertisement/")
def search_advertisements(
    title: str | None = None,
    description: str | None = None,
    price: int | None = None,
    author: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Advertisement)
    
    if title:
        query = query.filter(models.Advertisement.title.contains(title))
    if description:
        query = query.filter(models.Advertisement.description.contains(description))
    if price:
        query = query.filter(models.Advertisement.price == price)
    if author:
        query = query.filter(models.Advertisement.author.contains(author))
    
    return query.all()