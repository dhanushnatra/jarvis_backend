from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from schemas.request import Request



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.post("/get_res")
async def get_res(req:Request):
    print(req.message)
    return JSONResponse(content={"message": "Hello, world!"})
