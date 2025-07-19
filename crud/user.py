
from db.model import User
from auth.security import check_pwd,hash_pwd
from schemas.user import UserCreate
from sqlmodel import Session,select

def create_user(user: UserCreate, session: Session): 
    new_usr=User(username=user.username,password=hash_pwd(user.password),isadmin=user.isadmin)
    session.add(new_usr)
    session.commit()
    return user

def read_user(user:UserCreate,session:Session):
    
    user_read=session.exec(select(User).where(User.username==user.username))
    print(user_read)
    return user_read

def read_users(session:Session):
    session.exec(select(User))