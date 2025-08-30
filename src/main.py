import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


app = FastAPI(title="Bookly", default_response_class=ORJSONResponse)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
