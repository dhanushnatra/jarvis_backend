from datetime import datetime, timedelta,UTC
from jose import JWTError, jwt
from dotenv import load_dotenv

if load_dotenv():
    with open(".env","r") as file:
        content : list[str] = file.read().split("\n")
        SECRET_KEY :str = content[0]
        del file
else: 
    print("create a file .env in the work space with first line containing SECRET KEY")
    exit()



ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES : int  = 30
    

print(SECRET_KEY,ALGORITHM)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    try:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        print(f"failed to create a user auth token {e} ")
        
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]),True
    except JWTError as e:
        print("error")
        return {"error":"falied to decode"},False























# test functions
if __name__ == "__main__":
    data = {"username":"dhanush","password":"somehashedpass"}
    encoded = create_access_token(data=data,expires_delta=timedelta(minutes=50))
    print(f"\n data : {data}  \n encoded to \n {encoded}\n")
    authkey=input()
    decoded = decode_token(authkey)     # type: ignore
    if decoded[1]:
        print(f" decoded {decoded}")
        print(" expires at {} ".format(datetime.fromtimestamp(decoded[0]["exp"]))) # type: ignore
    else:
        print(decoded[0])