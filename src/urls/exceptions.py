import fastapi
from fastapi import responses


class ShortenUriAlreadyExists(Exception):
    def __init__(self, short_url: str):
        self.short_url = short_url


async def shorten_uri_already_exists_handler(request: fastapi.Request, exc: ShortenUriAlreadyExists):
    return responses.JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content={
            'message': f'Short URI `{exc.short_url}` is already used for another long URL'
        }
    )


class ShortenUriDoesNotExist(Exception):
    def __init__(self, short_url: str):
        self.short_url = short_url


async def shorten_uri_does_not_exist_handler(request: fastapi.Request, exc: ShortenUriDoesNotExist):
    return responses.JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content= {
            'message': f'Short URI `{exc.short_url}` does not exist'
        }
    )
