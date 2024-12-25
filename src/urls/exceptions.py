import fastapi
from fastapi import responses


class ShortUriAlreadyExists(Exception):
    def __init__(self, short_uri: str):
        self.short_uri = short_uri


async def short_uri_already_exists_handler(request: fastapi.Request, exc: ShortUriAlreadyExists):
    return responses.JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content={
            'message': f'Short URI `{exc.short_uri}` is already used for another long URL'
        }
    )


class ShortUriDoesNotExist(Exception):
    def __init__(self, short_uri: str):
        self.short_uri = short_uri


async def short_uri_does_not_exist_handler(request: fastapi.Request, exc: ShortUriDoesNotExist):
    return responses.JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content= {
            'message': f'Short URI `{exc.short_uri}` does not exist'
        }
    )
