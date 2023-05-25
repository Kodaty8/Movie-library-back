from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers.movies import router
from routers.users import router

app = FastAPI()

app.include_router(router)
app.include_router(router)


origins = [
    "http://localhost",
    "http://localhost:5174",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)