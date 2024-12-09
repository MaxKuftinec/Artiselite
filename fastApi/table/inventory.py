from fastapi import APIRouter, Depends, Path, HTTPException
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from models import Product

router = APIRouter()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class ProductRequest(BaseModel):
	name: str = Field(min_length=1)
	quantity: int

@router.get("/products")
async def get_products(db: db_dependency):
	return (db.query(Product).all())

@router.post("/products")
async def create_product(db: db_dependency, product_request: ProductRequest):
	new_product = Product(name=product_request.name, quantity=product_request.quantity)
	db.add(new_product)
	db.commit()
	db.refresh(new_product)
	return (new_product)

@router.delete("/products/{product_id}")
async def delete_product(db: db_dependency, product_id: int = Path(gt=0)): # I have no idea what gt=0 means
	product_result = db.query(Product).filter(Product.id == product_id).first()
	
	if product_result is None:
		raise HTTPException(status_code=404, detail="Product not found")
	else:
		db.delete(product_result)
		db.commit()
		return {"message": "Product successfully deleted"}
	
@router.put("/products/{product_id}")
async def update_product(db: db_dependency, product_id: int, product_request: ProductRequest):
	product_result = db.query(Product).filter(Product.id == product_id).first()

	if product_result is None:
		raise HTTPException(status_code=404, detail="Product not found")
	
	product_result.name = product_request.name
	product_result.quantity = product_request.quantity

	db.add(product_result)
	db.commit()
	return {"message": "Product successfully updated"}
  
	
    