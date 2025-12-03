from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, series, feedback, contracts

app = FastAPI(title="MovieHub API")

# Allow GitHub Pages frontend
origins = [
    "https://aryaman911.github.io",          # root
    "https://aryaman911.github.io/moviehub", # repo pages
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(series.router)
app.include_router(feedback.router)
app.include_router(contracts.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "MovieHub API is running"}

