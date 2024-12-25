import contextlib

import fastapi
from fastapi.openapi import utils

from src import database
from src.urls import router as urls_services
from src.urls import exceptions as urls_excs


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    database.init_db()
    yield

app = fastapi.FastAPI(
    title="URL Shortener",
    description="Web application to get shorten URL",
    lifespan=lifespan,
    version="0.1.0",
)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = utils.get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema

app.openapi = custom_openapi

api_router = fastapi.APIRouter(prefix='/api/v1')
api_router.include_router(urls_services.URLS_ROUTER)

app.include_router(api_router)
app.add_exception_handler(urls_excs.ShortenUriAlreadyExists, urls_excs.shorten_uri_already_exists_handler)
app.add_exception_handler(urls_excs.ShortenUriDoesNotExist, urls_excs.shorten_uri_does_not_exist_handler)
