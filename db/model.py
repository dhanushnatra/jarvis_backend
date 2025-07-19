from sqlmodel import Field, SQLModel


class User(SQLModel, table = True): #type: ignore
    id: int | None= Field(default=None, primary_key=True)
    username : str
    password : str
    isadmin : bool


