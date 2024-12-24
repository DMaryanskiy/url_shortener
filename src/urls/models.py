import pydantic


class ShortenUrlRequest(pydantic.BaseModel):
    original_url: str
    shorten_url: str | None = None


class ShortenUrlResponse(pydantic.BaseModel):
    shorten_url: str


class ErrorMessage(pydantic.BaseModel):
    message: str
