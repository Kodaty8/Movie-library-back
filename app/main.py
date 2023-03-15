from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routers import movies

app = FastAPI()

app.include_router(movies.router)
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
