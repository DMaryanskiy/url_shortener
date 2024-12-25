import pydantic


class ShortUriRequest(pydantic.BaseModel):
    original_url: str
    short_uri: str | None = None


class ShortUriResponse(pydantic.BaseModel):
    short_uri: str


class ErrorMessage(pydantic.BaseModel):
    message: str
