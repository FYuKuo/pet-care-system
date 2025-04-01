from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import users, pets, records
from exceptions.custom_exceptions import (
    BaseException,
    MissingParameterException,
    InvalidParameterException,
)
import uvicorn
import logging
import time
import json

app = FastAPI()

logger = logging.getLogger("uvicorn")


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(pets.router, prefix="/pets", tags=["pets"])
app.include_router(records.router, prefix="/records", tags=["records"])


@app.middleware("http")
async def log_api_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    log = {
        "method": request.method,
        "url": str(request.url),
        "responseStatus": response.status_code,
        "processTime": f"{process_time:.4f}s"
    }

    logger.info(json.dumps(log))

    return response


@app.exception_handler(BaseException)
async def base_exception_handler(request: Request, exc: BaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error": exc.error},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    first_error = exc.errors()[0]
    error_type = first_error.get("type")

    loc = first_error["loc"]
    filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
    field_string = ".".join(map(str, filtered_loc))

    msg = first_error["msg"]

    if error_type == "missing":
        raise MissingParameterException(field_string)
    else:
        raise InvalidParameterException(field_string, message=msg)


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, reload_dirs="src")
