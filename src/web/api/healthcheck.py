from fastapi.routing import APIRouter
from fastapi.requests import Request
from starlette import status

router = APIRouter(prefix="/health")

@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def healthcheck(request: Request):
    return "OK"

