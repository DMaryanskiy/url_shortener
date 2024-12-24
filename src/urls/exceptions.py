import fastapi
from fastapi import responses


class ShortenUrlAlreadyExists(Exception):
    def __init__(self, short_url: str):
        self.short_url = short_url


async def shorten_url_already_exists_handler(request: fastapi.Request, exc: ShortenUrlAlreadyExists):
    return responses.JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content={
            'message': f'Short URL `{exc.short_url}` is already used for another long URL'
        }
    )
