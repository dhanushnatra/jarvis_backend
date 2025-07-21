from fastapi import FastAPI
from router import user
from router import answer


app = FastAPI()


app.include_router(user.router,tags=["user"])
app.include_router(answer.router, tags=["answer"])