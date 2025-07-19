from fastapi import APIRouter, Depends, Header
from crud.user import create_user,read_user
from db.session import get_session
from schemas.user import UserCreate
from auth.auth import decode_token
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/user"
)

@router.post("/")
async def createUser(user:UserCreate,auth:str=Header(),session=Depends(get_session)):
    if decode_token(auth)[1]:
        create_user(user = user,session=session)
        print("user created")
        return user
    else:
        return JSONResponse({"error":"auth header mismatch"})
    
@router.post("/login")
async def loginUser(user:UserCreate,session=Depends(get_session)):
    return(read_user)