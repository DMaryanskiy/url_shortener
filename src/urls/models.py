import pydantic


class ShortenUriRequest(pydantic.BaseModel):
    original_url: str
    shorten_uri: str | None = None


class ShortenUriResponse(pydantic.BaseModel):
    shorten_uri: str


class ErrorMessage(pydantic.BaseModel):
    message: str
