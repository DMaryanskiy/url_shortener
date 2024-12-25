import fastapi
from fastapi import responses


class ShortenUrlAlreadyExists(Exception):
    def __init__(self, short_url: str):
        self.short_url = short_url


async def shorten_url_already_exists_handler(request: fastapi.Request, exc: ShortenUrlAlreadyExists):
    return responses.JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content={
            'message': f'Short URI `{exc.short_url}` is already used for another long URL'
        }
    )


class ShortenUrlDoesNotExist(Exception):
    def __init__(self, short_url: str):
        self.short_url = short_url


async def shorten_url_does_not_exist_handler(request: fastapi.Request, exc: ShortenUrlDoesNotExist):
    return responses.JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content= {
            'message': f'Short URI `{exc.short_url}` does not exist'
        }
    )
