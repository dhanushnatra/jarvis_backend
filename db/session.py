from .model import User
from sqlmodel import Session, SQLModel , create_engine


engine = create_engine("sqlite:///jarvis.db",echo=True)


def get_session():
    with Session(engine) as session:
        yield session
        
        

if __name__=="__main__":
    SQLModel.metadata.create_all(engine)
    print("!!... db created ....!!")