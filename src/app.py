from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import users
import uvicorn
from exceptions.custom_exceptions import BaseException, MissingParameterException, InvalidParameterException

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(users.router, prefix="/users")


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
    field_string = ".".join(filtered_loc)

    msg = first_error["msg"]
    
    if error_type == "missing":
        raise MissingParameterException(field_string)
    else:
        raise InvalidParameterException(field_string, message=msg)

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, reload_dirs="src")
