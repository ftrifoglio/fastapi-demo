from typing import Any

from api_utils.api_v1 import api_router_v1
from api_utils.api_v2 import api_router_v2
from fastapi import APIRouter, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from loguru import logger

app = FastAPI(title="Titanic API")
root_router = APIRouter()


@root_router.get("/")
def index(request: Request) -> Any:
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the Titanic API</h1>"
        "<div>"
        "<p>Click <a href='/docs'>here</a> to access the Swagger UI where you can call"
        "and test the API endpoints directly from the browser.</p>"
        "<p>Check out the source code at <a href='https://github.com/fedassembly/"
        "fastapi-demo'>https://github.com/fedassembly/fastapi-demo</a></p>"
        "</div>"
        "</body>"
        "</html>"
    )
    return HTMLResponse(content=body)


app.include_router(api_router_v1, prefix="/v1")
app.include_router(api_router_v2, prefix="/v2")
app.include_router(api_router_v2, prefix="/latest")
app.include_router(root_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> Any:
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")
