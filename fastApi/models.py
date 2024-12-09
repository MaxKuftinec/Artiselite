from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func # What is ForeignKey?
from sqlalchemy.orm import relationship # What is this relationship?
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # We are not applyting this yet. Trying to see if the user model even work. After that, then we will implement this hashing

class Product(Base):
	__tablename__ = "products"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	quantity = Column(Integer)

class InboundProduct(Base):
	__tablename__ = "inbound-products"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	supplier_information = Column(String)
	location = Column(String)
	quantity = Column(Integer)

class OutboundProduct(Base):
	__tablename__ = "outbound-products"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	supplier_information = Column(String)
	quantity = Column(Integer)

class Role(Base):
	__tablename__ = "roles"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, nullable=False)
	permissions = relationship("Permission", back_populates="role")

class Permission(Base):
	__tablename__ = "permissions"
	id = Column(Integer, primary_key=True, index=True)
	role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
	resource = Column(String, nullable=False)
	action = Column(String, nullable=False)
	role = relationship("Role", back_populates="permissions")

class User(Base): # Not finished
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, nullable=False)
	password = Column(String, nullable=False)
	# email = Column(String, unique=True, nullable=False) # I think no need email
	created_at =Column(DateTime, default=func.now())
	role_id = Column(Integer, ForeignKey("roles.id"), nullable=False) # Without this, there would be no way to link user to their role in database
	role = relationship("Role")
	