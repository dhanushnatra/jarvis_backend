from pydantic import BaseModel


class UserCreate(BaseModel):
    username : str 
    password : str # plain password
    isadmin : bool




class UserRead(BaseModel):
    username:str
    isadmin : bool
    
    class Config:
        orm_mode=True