from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware


def register_middleware(app: FastAPI):
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"])

    app.add_middleware(SlowAPIMiddleware)