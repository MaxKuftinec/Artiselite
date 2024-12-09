from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import User
from pydantic import BaseModel, Field
from passlib.context import CryptContext

router = APIRouter()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRequest(BaseModel):
	username: str = Field(min_length=1)
	password: str = Field(min_length=1)
	role_id: int

SECRET_KEY = "123123123" # Might wanna put this in .env
ALGORITHM = "HS256"

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
	access_token: str
	token_type: str

# Function to authenticate user
def authenticate_user(username: str, password: str, db):
	user = db.query(User).filter(User.username == username).first()
	if not user:
		return False
	if password != user.password:
		return False
	return user

# Function to create access token
from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt

# This function defines what can be extracted from the token particularly the username and the id
def create_access_token(username: str,
												id: int,
												expires_delta: timedelta):
	encode = {
		"sub": username,
    "user_id": id
	}

	expires = datetime.now(timezone.utc) + expires_delta
	encode.update({"exp": expires})
	return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def	get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub") # Why sub? Because that's how we define that in create_access_token
		id: int = payload.get("user_id")
		if username is None or id is None:
			raise HTTPException(status_code=401, detail=f"Inside get_current_user: Could not validate user {username} {id}")
		return {"username": username, "user_id": id}
	except JWTError:
		raise HTTPException(status_code=401, detail="Inside get_current_user: Could not validate user(2)")

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post('/users')
async def create_user(user: user_dependency, db: db_dependency, user_request: UserRequest):
	if user is None:
		raise HTTPException(status_code=401, detail="Not authenticated(Inside create_user)")
	new_user = User(username=user_request.username, password=user_request.password, role_id=user_request.role_id)
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return (new_user)

@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
	user = authenticate_user(form_data.username, form_data.password, db)
	
	if not user:
		raise HTTPException(status_code=401, detail="Login: Could not validate user")
	else:
		token = create_access_token(user.username, user.id, timedelta(minutes=20))
		return {"access_token": token, "token_type": "bearer"}

@router.get('/me')
async def get_me(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
		try:
				payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
				username: str = payload.get("sub")
				user_id: int = payload.get("user_id")

				if username is None or user_id is None:
						raise HTTPException(status_code=401, detail="Could not validate credentials")

				user = db.query(User).filter(User.id == user_id).first()
				if not user:
						raise HTTPException(status_code=404, detail="User not found")

				return {"username": user.username, "user_id": user.id, "role_id": user.role_id}

		except JWTError:
				raise HTTPException(status_code=401, detail="Could not validate credentials")
		except Exception as e:
				raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")