from fastapi import FastAPI , Header
from auth.auth import decode_token

app = FastAPI()


@app.post("/check")
async def check_token(auth:str = Header()):
    return "token {}".format(decode_token(auth))