from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

from constants import SystemTypes
from schemas.signed_api_data import SignedAPIData
from utils.base64_utils import encode_bytes_base64
from utils.hash_utils import sha256_hash

class SignedAPIRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            if request.method != "POST":
                return await original_route_handler(request)

            request_body = await request.body()
            signed_api_request = SignedAPIData.model_validate_json(request_body)
            request._body = signed_api_request.data

            response: Response = await original_route_handler(request)

            signed_api_response = SignedAPIData(
                data=encode_bytes_base64(response.body),
                sign=encode_bytes_base64(sha256_hash(response.body)),
                signer_cert=encode_bytes_base64(SystemTypes.SYSTEM_B.encode("utf-8")),
            )
            response.body = signed_api_response.model_dump_json().encode("utf-8")
            response.headers.update({"Content-Length": str(len(response.body))})

            return response

        return custom_route_handler
