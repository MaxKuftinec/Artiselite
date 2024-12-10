import models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from table.test import router as test_router
from table.inventory import router as inventory_router
from table.user import router as user_router
from table.inbound import router as inbound_router
from table.outbound import router as outbound_router

app = FastAPI()
models.Base.metadata.create_all(bind=engine) # This line creates the table in the database

# Define CORS settings
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],  # Allows all methods
	allow_headers=["*"]  # Allows all headers
)

app.include_router(test_router, tags=["Test"])
app.include_router(inventory_router, tags=["Inventory"])
app.include_router(user_router, tags=["User"])
app.include_router(inbound_router, tags=["Inbound"])
app.include_router(outbound_router, tags=["Outbound"])