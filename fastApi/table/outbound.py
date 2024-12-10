from fastapi import APIRouter, Depends, Path, HTTPException
from database import SessionLocal
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from models import OutboundProduct
from models import Product

router = APIRouter()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# class InboundRequest(BaseModel):
# 	name: str = Field(min_length=1)
# 	supplier_information: Optional[str] = None
# 	location: Optional[str] = None
# 	quantity: int

class OutboundRequest(BaseModel):
	name: str = Field(min_length=1)
	quantity: int
	remarks: Optional[str] = None
	destination: str = Field(min_length=1)

class ProductRequest(BaseModel):
	name: str = Field(min_length=1)
	quantity: int

@router.get("/outbound-products")
async def get_outbound_products(db: db_dependency):
	return (db.query(OutboundProduct).all())

@router.post("/outbound-products")
async def deliver_product(db: db_dependency, deliver_request: OutboundRequest):
	existing_product = db.query(Product).filter(Product.name == deliver_request.name).first()
	delivering_product = OutboundProduct(name=deliver_request.name, quantity=deliver_request.quantity, remarks=deliver_request.remarks, destination=deliver_request.destination)
	
	if existing_product:
		if (existing_product.quantity < deliver_request.quantity):
			return {"message": "We don't have that many product", existing_product.name: existing_product.quantity}
		else:
			existing_product.quantity -= deliver_request.quantity
			db.add(delivering_product)
			db.add(existing_product)
			db.commit()
			db.refresh(delivering_product)
			db.refresh(existing_product)
			return (delivering_product)
	else:
		return {"message": "Product not found"}


@router.delete("/outbound-products/{product_id}")
async def delete_product(db: db_dependency, product_id: int = Path(gt=0)): # I have no idea what gt=0 means
	product_result = db.query(OutboundProduct).filter(OutboundProduct.id == product_id).first()
	
	if product_result is None:
		raise HTTPException(status_code=404, detail="Product not found")
	else:
		existing_product = db.query(Product).filter(Product.name == product_result.name).first()
		existing_product.quantity += product_result.quantity
		db.delete(product_result)
		db.commit()
		return {"message": "Product successfully deleted"}

@router.put("/outbound-products/{product_id}")
async def update_product(db: db_dependency, product_id: int, product_request: OutboundRequest):
	product_result = db.query(OutboundProduct).filter(OutboundProduct.id == product_id).first()
	existing_product = db.query(Product).filter(Product.name == product_result.name).first()

	if product_result is None:
		raise HTTPException(status_code=404, detail="Product not found")
	
	gradient = product_request.quantity - product_result.quantity
	existing_product.quantity -= gradient
	product_result.name = product_request.name
	product_result.quantity = product_request.quantity
	product_result.remarks = product_request.remarks
	product_result.destination = product_request.destination

	db.add(product_result)
	db.commit()
	return {"message": "Product successfully updated"}
