from typing import Any

from api_utils.api_v1 import api_router_v1
from api_utils.api_v2 import api_router_v2
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

root_router = APIRouter()


@root_router.get("/")
def index(request: Request) -> Any:
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )
    return HTMLResponse(content=body)


app.include_router(api_router_v1, prefix="/v1")
app.include_router(api_router_v2, prefix="/v2")
app.include_router(api_router_v2, prefix="/latest")
app.include_router(root_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")
