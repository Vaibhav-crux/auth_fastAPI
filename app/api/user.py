from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserCreateResponse
from app.utils.hashing import hash_password
from app.utils.auth import create_access_token, create_refresh_token, get_current_user, refresh_access_token
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger()

@router.post("/users/", response_model=UserCreateResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"New user creation attempt for username: {user.username}")
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        logger.warning(f"Username {user.username} already exists")
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.username})
    refresh_token = create_refresh_token(data={"sub": new_user.username})
    new_user.refresh_token = refresh_token
    db.commit()

    logger.info(f"User {user.username} created successfully")
    return {"user": UserResponse.from_orm(new_user), "access_token": access_token, "token_type": "bearer"}

@router.post("/token/refresh")
async def refresh_token(hashed_refresh_token: str, db: Session = Depends(get_db)):
    logger.info("Attempting to refresh access token")
    try:
        result = refresh_access_token(db, hashed_refresh_token)
        logger.info("Access token refreshed successfully")
        return result
    except HTTPException as e:
        logger.error(f"Failed to refresh token: {str(e.detail)}")
        raise

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the user_id matches the id of the authenticated user
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this user's information"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/token/refresh")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    return refresh_access_token(db, refresh_token)